from tower_config import WIDTH, HEIGHT, UI_LEFT_MARGIN, UI_RIGHT_MARGIN, ROOM_WIDTH, ROOM_HEIGHT, ROOM_SPACING

# Camera state
camera_offset_y = 0
zoom_level = 1.0

def get_camera():
    return camera_offset_y, zoom_level

def set_camera(offset, zoom):
    global camera_offset_y, zoom_level
    camera_offset_y = offset
    zoom_level = zoom

def calculate_min_zoom_only(tower_rooms, basement_rooms):
    if not tower_rooms and not basement_rooms:
        return 1.0
    top = tower_rooms[-1].rect.y if tower_rooms else 0
    bottom = basement_rooms[-1].rect.y if basement_rooms else 0
    total_height = (bottom - top + ROOM_HEIGHT + ROOM_SPACING)
    return min(1.0, (HEIGHT - 100) / total_height)

def calculate_min_zoom_and_scroll(tower_rooms, basement_rooms):
    global zoom_level, camera_offset_y
    if not tower_rooms and not basement_rooms:
        zoom_level = 1.0
        camera_offset_y = 0
        return

    top = tower_rooms[-1].rect.y if tower_rooms else 0
    bottom = basement_rooms[-1].rect.y if basement_rooms else 0
    total_height = (bottom - top + ROOM_HEIGHT + ROOM_SPACING)
    zoom_level = min(1.0, (HEIGHT - 100) / total_height)

    mid_world_y = (top + bottom) / 2
    screen_mid_y = HEIGHT / (2 * zoom_level)
    camera_offset_y = screen_mid_y - mid_world_y

def calculate_max_zoom():
    global zoom_level
    usable_width = WIDTH - UI_LEFT_MARGIN - UI_RIGHT_MARGIN
    zoom_level = min(2.0, usable_width / ROOM_WIDTH)

def apply_zoom(amount, tower_rooms, basement_rooms):
    global zoom_level
    usable_width = WIDTH - UI_LEFT_MARGIN - UI_RIGHT_MARGIN
    max_zoom = min(2.0, usable_width / ROOM_WIDTH)
    min_zoom = calculate_min_zoom_only(tower_rooms, basement_rooms)
    zoom_level = max(min_zoom, min(max_zoom, zoom_level + amount))

def handle_mouse_scroll(event):
    global camera_offset_y
    camera_offset_y += (30 / zoom_level) * (-event.y)
