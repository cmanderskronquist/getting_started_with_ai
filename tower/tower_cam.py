from tower_config import (
    WIDTH, HEIGHT,
    UI_LEFT_MARGIN, UI_RIGHT_MARGIN,
    ROOM_WIDTH, ROOM_HEIGHT, ROOM_SPACING,
    WORLD_HORIZON_Y
)

class Camera:
    def __init__(self):
        """Initialize camera with default values."""
        self.reset()

    def reset(self):
        """Reset the camera to its default position and zoom."""
        self.offset_y = HEIGHT // 2
        self.zoom = 1.0

    def get(self):
        """Get the current camera state as a tuple (offset_y, zoom)."""
        return self.offset_y, self.zoom

    def set(self, offset, zoom):
        """Set the camera position and zoom level."""
        self.offset_y = offset
        self.zoom = zoom

    def calculate_min_zoom_only(self, tower_rooms, basement_rooms):
        """
        Calculate the minimum zoom level to fit the entire tower and basement.

        Returns:
            float: The minimum zoom level (clamped to max 1.0).
        """
        if not tower_rooms and not basement_rooms:
            return 1.0

        top = tower_rooms[-1].rect.y if tower_rooms else WORLD_HORIZON_Y
        bottom = basement_rooms[-1].rect.y if basement_rooms else WORLD_HORIZON_Y

        total_height = (bottom - top + ROOM_HEIGHT + ROOM_SPACING)
        return min(1.0, (HEIGHT - 100) / total_height)

    def calculate_min_zoom_and_scroll(self, tower_rooms, basement_rooms):
        """
        Auto-adjust zoom and scroll to fit the current tower and basement in view.
        """
        if not tower_rooms and not basement_rooms:
            self.zoom = 1.0
            self.offset_y = HEIGHT // 2
            return

        top = tower_rooms[-1].rect.y if tower_rooms else WORLD_HORIZON_Y
        bottom = basement_rooms[-1].rect.y if basement_rooms else WORLD_HORIZON_Y

        total_height = (bottom - top + ROOM_HEIGHT + ROOM_SPACING)
        self.zoom = min(1.0, (HEIGHT - 100) / total_height)

        mid_world_y = (top + bottom) / 2
        screen_mid_y = HEIGHT / (2 * self.zoom)
        self.offset_y = screen_mid_y - mid_world_y

    def calculate_max_zoom(self):
        """
        Set the maximum zoom level based on usable UI width.
        """
        usable_width = WIDTH - UI_LEFT_MARGIN - UI_RIGHT_MARGIN
        self.zoom = min(2.0, usable_width / ROOM_WIDTH)

    def apply_zoom(self, amount, tower_rooms, basement_rooms):
        """
        Apply a zoom increment while respecting min/max zoom bounds.

        Args:
            amount (float): The zoom increment.
        """
        usable_width = WIDTH - UI_LEFT_MARGIN - UI_RIGHT_MARGIN
        max_zoom = min(2.0, usable_width / ROOM_WIDTH)
        min_zoom = self.calculate_min_zoom_only(tower_rooms, basement_rooms)
        self.zoom = max(min_zoom, min(max_zoom, self.zoom + amount))

    def handle_mouse_scroll(self, event, tower_rooms, basement_rooms):
        """
        Handle vertical camera scrolling with correct bounds:
        - Scroll up: Stop when topmost room bottom is at top of screen.
        - Scroll down: Stop when bottommost room top is at bottom of screen.
        - If no rooms, horizon must remain visible.
        """
        scroll_amount = (30 / self.zoom) * (-event.y)
        visible_height = HEIGHT / self.zoom

        # Get topmost room's bottom (visible edge)
        if tower_rooms:
            top_room_bottom = tower_rooms[-1].rect.y + ROOM_HEIGHT
        else:
            top_room_bottom = WORLD_HORIZON_Y

        # Get bottommost room's top
        if basement_rooms:
            bottom_room_top = basement_rooms[-1].rect.y
        else:
            bottom_room_top = WORLD_HORIZON_Y

        # Calculate bounds:
        # Top of screen must be ≤ top_room_bottom → offset_y ≤ top_room_bottom
        min_offset_y = top_room_bottom

        # Bottom of screen must be ≥ bottom_room_top → offset_y ≥ bottom_room_top - visible_height
        max_offset_y = bottom_room_top - visible_height

        # Prevent flipped bounds if rooms are close together
        if max_offset_y < min_offset_y:
            mid_y = (top_room_bottom + bottom_room_top) / 2 - visible_height / 2
            self.offset_y = mid_y
            return

        # Apply scroll and clamp
        self.offset_y = max(min_offset_y, min(max_offset_y, self.offset_y + scroll_amount))
