import pygame
import sys

## Constants 
# Screen dimensions
WIDTH = 800
HEIGHT = 600
FPS = 60

# UI Margins
UI_LEFT_MARGIN = 150
UI_RIGHT_MARGIN = 150

# Colors
SKY_COLOR = (180, 220, 255)
EARTH_COLOR = (170, 140, 110)
ROOM_COLOR = (230, 190, 255)
GROUND_COLOR = (100, 80, 50)
BUTTON_COLOR = (200, 240, 200)
TEXT_COLOR = (0, 0, 0)

# World
WORLD_HORIZON_Y = 0

# Room dimensions
ROOM_WIDTH = 120
ROOM_HEIGHT = 40
ROOM_SPACING = 1

# Font
pygame.init()
FONT = pygame.font.SysFont(None, 24)
##

class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, surface):
        pygame.draw.rect(surface, BUTTON_COLOR, self.rect)
        label = FONT.render(self.text, True, TEXT_COLOR)
        surface.blit(label, (self.rect.x + 5, self.rect.y + 10))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Initialize Pygame
pygame.init()

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wizard Tower Builder")
clock = pygame.time.Clock()

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

    def handle_mouse_scroll(self, event, tower):
        scroll_amount = (0.5 / self.zoom) * -event.y
        self.offset_y += scroll_amount

        # World Y positions
        top_y = tower.get_peak()        # e.g. -120
        bottom_y = tower.get_bottom()   # e.g. 80
        visible_height = HEIGHT / self.zoom

        # Compute screen edges in world space
        screen_top_world_y = -self.offset_y
        screen_bottom_world_y = screen_top_world_y + visible_height

        # Clamp: don’t let screen show above top of tower
        if screen_top_world_y < top_y:
            self.offset_y = -top_y
        # Clamp: don’t let screen show below bottom of tower
        elif screen_bottom_world_y > bottom_y:
            self.offset_y = -(bottom_y - visible_height)


# Initialize camera
camera = Camera()
camera.reset()

class Room:
    def __init__(self, x=0, y=0, width=120, height=40, room_type="Empty room", cost=0, color=(200, 200, 200)):
        self.rect = pygame.Rect(x, y, width, height)
        self.type = room_type
        self.cost = cost
        self.color = color

    @property
    def x(self):
        return self.rect.x

    @x.setter
    def x(self, value):
        self.rect.x = value

    @property
    def y(self):
        return self.rect.y

    @y.setter
    def y(self, value):
        self.rect.y = value

    @property
    def width(self):
        return self.rect.width

    @property
    def height(self):
        return self.rect.height

    def draw(self, surface, camera):
        """
        Draw the room with current camera zoom and offset applied.
        """
        offset_y, zoom = camera.get()

        scaled_rect = self.rect.copy()
        scaled_rect.x = int(self.rect.x * zoom)
        scaled_rect.y = int((self.rect.y - WORLD_HORIZON_Y + offset_y) * zoom)
        scaled_rect.width = int(self.rect.width * zoom)
        scaled_rect.height = int(self.rect.height * zoom)

        pygame.draw.rect(surface, self.color, scaled_rect)

        if FONT and self.type:
            text = FONT.render(self.type, True, (0, 0, 0))
            text_rect = text.get_rect(center=scaled_rect.center)
            surface.blit(text, text_rect)

class Resources:
    def __init__(self):
        self.mana = 0
        self.earth = 0
        self.wood = 0
        self.stone = 0
        self.gold = 0

    def add(self, resource, amount):
        if hasattr(self, resource):
            setattr(self, resource, getattr(self, resource) + amount)

    def spend(self, resource, amount):
        if hasattr(self, resource) and getattr(self, resource) >= amount:
            setattr(self, resource, getattr(self, resource) - amount)
            return True
        return False

    def to_dict(self):
        return {
            "mana": self.mana,
            "earth": self.earth,
            "wood": self.wood,
            "stone": self.stone,
            "gold": self.gold
        }
        
    def draw(self, surface, x=20, y=20):
        for resource, amount in self.to_dict().items():
            label = FONT.render(f"{resource}: {amount}", True, TEXT_COLOR)
            surface.blit(label, (x, y))
            y += 30


class Tower:
    def __init__(self):
        self.rooms = []        # Rooms above the horizon
        self.basements = []    # Rooms below the horizon
        self.resources = Resources()

    def add_room(self, room):
        self.rooms.append(room)

    def add_basement(self, room):
        self.basements.append(room)

    @property
    def height(self):
        return sum(room.height for room in self.rooms)

    @property
    def depth(self):
        return -sum(room.height for room in self.basements)

    def get_peak(self):
        return self.rooms[-1].y if self.rooms else WORLD_HORIZON_Y

    def get_bottom(self):
        last = self.basements[-1] if self.basements else None
        return last.y + last.height if last else WORLD_HORIZON_Y


# UI Buttons
build_button    = Button(WIDTH - 150, 100, 120, 40, "Build Room")
dig_button      = Button(WIDTH - 150, 160, 120, 40, "Dig Basement")

def draw_base(surface, camera):
    offset_y, zoom = camera.get()
    scaled_w = int(200 * zoom)
    scaled_h = int(50 * zoom)
    x = (WIDTH // 2) - (scaled_w // 2)
    screen_y = int((WORLD_HORIZON_Y + offset_y) * zoom)
    pygame.draw.rect(surface, GROUND_COLOR, (x, screen_y, scaled_w, scaled_h))

def draw_horizon(surface, camera):
    offset_y, zoom = camera.get()
    y = int((WORLD_HORIZON_Y + offset_y) * zoom)
    pygame.draw.line(surface, GROUND_COLOR, (0, y), (WIDTH, y), 4)

def draw_background(surface, camera):
    offset_y, zoom = camera.get()
    horizon_y = int((WORLD_HORIZON_Y + offset_y) * zoom)
    pygame.draw.rect(surface, SKY_COLOR, (0, 0, WIDTH, horizon_y))
    pygame.draw.rect(surface, EARTH_COLOR, (0, horizon_y, WIDTH, HEIGHT - horizon_y))

def draw_debug_info(surface, camera):
    offset_y, zoom = camera.get()
    text = FONT.render(f"offset_y: {offset_y:.1f}, zoom: {zoom:.2f}", True, (255, 0, 0))
    surface.blit(text, (10, HEIGHT - 30))

def main():
    running = True

    # Initialize the tower
    tower = Tower()

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if build_button.is_clicked(event.pos):
                    if tower.rooms:
                        new_y = tower.rooms[-1].y - (ROOM_HEIGHT + ROOM_SPACING)
                    else:
                        new_y = WORLD_HORIZON_Y - ROOM_HEIGHT - ROOM_SPACING
                    tower.add_room(Room(x=WIDTH // 2 - ROOM_WIDTH // 2, y=new_y, width=ROOM_WIDTH, height=ROOM_HEIGHT, color=(200, 200, 200), room_type="Room"))

                elif dig_button.is_clicked(event.pos):
                    if tower.basements:
                        new_y = tower.basements[-1].y + (ROOM_HEIGHT + ROOM_SPACING)
                    else:
                        new_y = WORLD_HORIZON_Y + ROOM_SPACING
                    tower.add_basement(Room(x=WIDTH // 2 - ROOM_WIDTH // 2, y=new_y, width=ROOM_WIDTH, height=ROOM_HEIGHT, color=(100, 100, 100), room_type="Basement"))
                    tower.resources.add("earth", 10)

            elif event.type == pygame.MOUSEWHEEL:
                camera.handle_mouse_scroll(event, tower)

        # Draw scene
        draw_background(screen, camera)
        for room in tower.rooms:
            room.draw(screen, camera)
        draw_base(screen, camera)
        for room in tower.basements:
            room.draw(screen, camera)
        draw_horizon(screen, camera)
        draw_debug_info(screen, camera)

        # Draw UI
        build_button.draw(screen)
        dig_button.draw(screen)
        tower.resources.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
