import pygame
import sys
from tower_config import (
    WIDTH, HEIGHT, FPS, SKY_COLOR, EARTH_COLOR, ROOM_COLOR, GROUND_COLOR,
    BUTTON_COLOR, TEXT_COLOR, ROOM_WIDTH, ROOM_HEIGHT, ROOM_SPACING, FONT
)
from tower_ui import Button, draw_resources
from tower_cam import (
    apply_zoom,
    calculate_max_zoom,
    calculate_min_zoom_and_scroll,
    handle_mouse_scroll,
    get_camera
)
from tower_config import (  # Import constants from config.py
    WIDTH, HEIGHT, FPS, SKY_COLOR, EARTH_COLOR, ROOM_COLOR, GROUND_COLOR,
    BUTTON_COLOR, TEXT_COLOR, ROOM_WIDTH, ROOM_HEIGHT, ROOM_SPACING
)



# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wizard Tower Builder")
clock = pygame.time.Clock()

# Game Data
tower_rooms = []
basement_rooms = []
resources = {"Earth": 0}

# Constants for screen and room layout
WIDTH = 800
HEIGHT = 600
UI_LEFT_MARGIN = 150
UI_RIGHT_MARGIN = 150
# Colors
BUTTON_COLOR = (200, 240, 200)
TEXT_COLOR = (0, 0, 0)
# Room size
ROOM_WIDTH = 120
ROOM_HEIGHT = 40
ROOM_SPACING = 1

class Room:
    def __init__(self, x, y, width, height, color, label=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.label = label

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

        if FONT and self.label:
            text = FONT.render(self.label, True, (0, 0, 0))
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text, text_rect)

# Buttons
build_button = Button(WIDTH - 150, 100, 120, 40, "Build Room")
dig_button = Button(WIDTH - 150, 160, 120, 40, "Dig Basement")
zoom_in_button = Button(WIDTH - 150, 220, 30, 30, "+")
zoom_out_button = Button(WIDTH - 110, 220, 30, 30, "-")
zoom_max_button = Button(WIDTH - 150, 260, 70, 30, "Max")
zoom_min_button = Button(WIDTH - 75, 260, 70, 30, "Min")

def draw_base(surface):
    camera_offset_y, zoom_level = get_camera()
    scaled_w = int(200 * zoom_level)
    scaled_h = int(50 * zoom_level)
    x = (WIDTH // 2) - (scaled_w // 2)
    y = int((camera_offset_y) * zoom_level)
    pygame.draw.rect(surface, GROUND_COLOR, (x, y, scaled_w, scaled_h))

def draw_horizon(surface):
    camera_offset_y, zoom_level = get_camera()
    y = int((camera_offset_y) * zoom_level)
    pygame.draw.line(surface, GROUND_COLOR, (0, y), (WIDTH, y), 4)

def draw_background(surface):
    camera_offset_y, zoom_level = get_camera()
    horizon_y = int((camera_offset_y) * zoom_level)
    pygame.draw.rect(surface, SKY_COLOR, (0, 0, WIDTH, horizon_y))
    pygame.draw.rect(surface, EARTH_COLOR, (0, horizon_y, WIDTH, HEIGHT - horizon_y))

def main():
    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                camera_offset_y, zoom_level = get_camera()
                horizon_y = int(camera_offset_y * zoom_level)

                if build_button.is_clicked(event.pos):
                    # Position new room above the horizon
                    new_grid_y = tower_rooms[-1].rect.y - (ROOM_HEIGHT + ROOM_SPACING) if tower_rooms else horizon_y - ROOM_HEIGHT - ROOM_SPACING
                    tower_rooms.append(Room(WIDTH // 2 - ROOM_WIDTH // 2, new_grid_y, ROOM_WIDTH, ROOM_HEIGHT, (200, 200, 200), "Room"))

                elif dig_button.is_clicked(event.pos):
                    # Position new basement below the horizon
                    new_grid_y = basement_rooms[-1].rect.y + (ROOM_HEIGHT + ROOM_SPACING) if basement_rooms else horizon_y + ROOM_SPACING
                    basement_rooms.append(Room(WIDTH // 2 - ROOM_WIDTH // 2, new_grid_y, ROOM_WIDTH, ROOM_HEIGHT, (100, 100, 100), "Basement"))
                    resources["Earth"] += 10

                elif zoom_in_button.is_clicked(event.pos):
                    apply_zoom(+0.1, tower_rooms, basement_rooms)
                elif zoom_out_button.is_clicked(event.pos):
                    apply_zoom(-0.1, tower_rooms, basement_rooms)
                elif zoom_max_button.is_clicked(event.pos):
                    calculate_max_zoom()
                elif zoom_min_button.is_clicked(event.pos):
                    calculate_min_zoom_and_scroll(tower_rooms, basement_rooms)

            elif event.type == pygame.MOUSEWHEEL:
                handle_mouse_scroll(event)

        draw_background(screen)

        for room in tower_rooms:
            room.draw(screen)
        draw_base(screen)
        for room in basement_rooms:
            room.draw(screen)

        draw_horizon(screen)
        build_button.draw(screen)
        dig_button.draw(screen)
        zoom_in_button.draw(screen)
        zoom_out_button.draw(screen)
        zoom_max_button.draw(screen)
        zoom_min_button.draw(screen)
        draw_resources(screen, resources)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()