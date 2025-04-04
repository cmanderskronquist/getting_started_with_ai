import pygame
import sys
from tower_ui import Button, draw_resources, init_font
from tower_cam import (
    apply_zoom,
    calculate_max_zoom,
    calculate_min_zoom_and_scroll,
    handle_mouse_scroll,
    get_camera
)

pygame.init()
init_font()  # Ensure font is initialized after pygame.init()

# Screen
WIDTH, HEIGHT = 800, 600
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wizard Tower Builder")
clock = pygame.time.Clock()

# Colors
SKY_COLOR = (180, 220, 255)
EARTH_COLOR = (170, 140, 110)
ROOM_COLOR = (230, 190, 255)
GROUND_COLOR = (100, 80, 50)

# Game Data
tower_rooms = []
basement_rooms = []
resources = {"Earth": 0}

# Room size
ROOM_WIDTH = 120
ROOM_HEIGHT = 40
ROOM_SPACING = 5

class Room:
    def __init__(self, grid_y):
        self.grid_y = grid_y
        self.width = ROOM_WIDTH
        self.height = ROOM_HEIGHT

    def draw(self, surface):
        camera_offset_y, zoom_level = get_camera()
        scaled_width = int(self.width * zoom_level)
        scaled_height = int(self.height * zoom_level)
        x = (WIDTH // 2) - (scaled_width // 2)
        world_y = self.grid_y * (self.height + ROOM_SPACING)
        screen_y = int((world_y + camera_offset_y) * zoom_level)

        font = pygame.font.SysFont(None, 24)
        pygame.draw.rect(surface, ROOM_COLOR, (x, screen_y, scaled_width, scaled_height))
        label = font.render(f"Room ({self.grid_y})", True, (0, 0, 0))
        surface.blit(label, (x + 10, screen_y + 10))

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
                if build_button.is_clicked(event.pos):
                    new_grid_y = tower_rooms[-1].grid_y - 1 if tower_rooms else -1
                    tower_rooms.append(Room(new_grid_y))

                elif dig_button.is_clicked(event.pos):
                    new_grid_y = basement_rooms[-1].grid_y + 1 if basement_rooms else 1
                    basement_rooms.append(Room(new_grid_y))
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