import pygame
import sys

pygame.init()

# Screen
WIDTH, HEIGHT = 800, 600
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wizard Tower Builder")
clock = pygame.time.Clock()

# Colors
BG_COLOR = (180, 220, 255)
ROOM_COLOR = (230, 190, 255)
TOWER_BASE_COLOR = (150, 100, 50)
BUTTON_COLOR = (200, 240, 200)
TEXT_COLOR = (0, 0, 0)

# Fonts
font = pygame.font.SysFont(None, 24)

# Game Data
tower_rooms = []
basement_rooms = []
resources = {"Earth": 0}

# Camera
camera_offset_y = 0
zoom_level = 1.0

# Room size
ROOM_WIDTH = 120
ROOM_HEIGHT = 40
ROOM_SPACING = 5

class Room:
    def __init__(self, y):
        self.width = ROOM_WIDTH
        self.height = ROOM_HEIGHT
        self.y = y  # vertical position only

    def draw(self, surface):
        # Recalculate horizontal centering at draw time, using zoom
        scaled_width = int(self.width * zoom_level)
        scaled_height = int(self.height * zoom_level)
        x = (WIDTH // 2) - (scaled_width // 2)
        y = int((self.y + camera_offset_y) * zoom_level)

        pygame.draw.rect(surface, ROOM_COLOR, (x, y, scaled_width, scaled_height))
        label = font.render("Room", True, TEXT_COLOR)
        surface.blit(label, (x + 10, y + 10))

class Button:
    def __init__(self, x, y, w, h, text, action=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.action = action

    def draw(self, surface):
        pygame.draw.rect(surface, BUTTON_COLOR, self.rect)
        label = font.render(self.text, True, TEXT_COLOR)
        surface.blit(label, (self.rect.x + 5, self.rect.y + 10))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Game Buttons
build_button = Button(WIDTH - 150, 100, 120, 40, "Build Room")
dig_button = Button(WIDTH - 150, 160, 120, 40, "Dig Basement")
zoom_in_button = Button(WIDTH - 150, 220, 30, 30, "+")
zoom_out_button = Button(WIDTH - 110, 220, 30, 30, "-")
zoom_max_button = Button(WIDTH - 150, 260, 70, 30, "Max")
zoom_min_button = Button(WIDTH - 75, 260, 70, 30, "Min")

def draw_resources(surface):
    x, y = 20, 20
    for resource, amount in resources.items():
        label = font.render(f"{resource}: {amount}", True, TEXT_COLOR)
        surface.blit(label, (x, y))
        y += 30

def draw_base(surface):
    scaled_w = int(200 * zoom_level)
    scaled_h = int(50 * zoom_level)
    x = (WIDTH // 2) - (scaled_w // 2)
    y = int((HEIGHT - 50 + camera_offset_y) * zoom_level)
    pygame.draw.rect(surface, TOWER_BASE_COLOR, (x, y, scaled_w, scaled_h))

def calculate_min_zoom_and_scroll():
    global zoom_level, camera_offset_y

    # Calculate full height of the visible tower/dungeon
    top_y = tower_rooms[-1].y if tower_rooms else (HEIGHT - 100)
    bottom_y = basement_rooms[-1].y + ROOM_HEIGHT if basement_rooms else (HEIGHT - 50)

    total_height = bottom_y - top_y
    padding = 100  # extra margin

    # Calculate zoom to fit everything into screen height
    zoom_level = min(1.0, (HEIGHT - padding) / total_height)

    # Center the view vertically
    content_mid_y = (top_y + bottom_y) / 2
    screen_mid_y = HEIGHT / (2 * zoom_level)
    camera_offset_y = screen_mid_y - content_mid_y

def handle_mouse_scroll(event):
    global camera_offset_y
    camera_offset_y += (30 / zoom_level) * (-event.y)

def main():
    global camera_offset_y, zoom_level
    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if build_button.is_clicked(event.pos):
                    top_y = tower_rooms[-1].y - 45 if tower_rooms else HEIGHT - 100
                    tower_rooms.append(Room(top_y))

                elif dig_button.is_clicked(event.pos):
                    next_y = basement_rooms[-1].y + 45 if basement_rooms else HEIGHT - 50 + 45
                    basement_rooms.append(Room(next_y))
                    resources["Earth"] += 10

                elif zoom_in_button.is_clicked(event.pos):
                    zoom_level = min(2.0, zoom_level + 0.1)

                elif zoom_out_button.is_clicked(event.pos):
                    zoom_level = max(0.5, zoom_level - 0.1)

                elif zoom_max_button.is_clicked(event.pos):
                    zoom_level = 1.0  # reset zoom, keep camera position

                elif zoom_min_button.is_clicked(event.pos):
                    calculate_min_zoom_and_scroll()  # reset both zoom and scroll

            elif event.type == pygame.MOUSEWHEEL:
                handle_mouse_scroll(event)

        screen.fill(BG_COLOR)

        # Draw game world
        for room in tower_rooms:
            room.draw(screen)
        draw_base(screen)
        for room in basement_rooms:
            room.draw(screen)

        # Draw UI
        build_button.draw(screen)
        dig_button.draw(screen)
        zoom_in_button.draw(screen)
        zoom_out_button.draw(screen)
        zoom_max_button.draw(screen)
        zoom_min_button.draw(screen)
        draw_resources(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
