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

# Tower and basement data
tower_rooms = []
basement_rooms = []

resources = {"Earth": 0}

camera_offset_y = 0
zoom_level = 1.0

class Room:
    def __init__(self, y):
        self.width = 120
        self.height = 40
        self.x = WIDTH // 2 - self.width // 2
        self.y = y

    def draw(self, surface):
        scaled_x = int(self.x * zoom_level)
        scaled_y = int((self.y + camera_offset_y) * zoom_level)
        scaled_w = int(self.width * zoom_level)
        scaled_h = int(self.height * zoom_level)

        pygame.draw.rect(surface, ROOM_COLOR, (scaled_x, scaled_y, scaled_w, scaled_h))
        label = font.render("Room", True, TEXT_COLOR)
        surface.blit(label, (scaled_x + 10, scaled_y + 10))

class Button:
    def __init__(self, x, y, w, h, text):
        self.base_rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, surface):
        pygame.draw.rect(surface, BUTTON_COLOR, self.base_rect)
        label = font.render(self.text, True, TEXT_COLOR)
        surface.blit(label, (self.base_rect.x + 10, self.base_rect.y + 10))

    def is_clicked(self, pos):
        return self.base_rect.collidepoint(pos)

build_button = Button(WIDTH - 150, 100, 120, 40, "Build Room")
dig_button = Button(WIDTH - 150, 160, 120, 40, "Dig Basement")

def draw_resources(surface):
    x, y = 20, 20
    for resource, amount in resources.items():
        text = f"{resource}: {amount}"
        label = font.render(text, True, TEXT_COLOR)
        surface.blit(label, (x, y))
        y += 30

def draw_base(surface):
    x = WIDTH // 2 - 100
    y = HEIGHT - 50 + camera_offset_y
    w, h = 200, 50

    pygame.draw.rect(surface, TOWER_BASE_COLOR, (
        int(x * zoom_level), int(y * zoom_level),
        int(w * zoom_level), int(h * zoom_level)
    ))

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

            elif event.type == pygame.KEYDOWN:
                # Scroll
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    camera_offset_y += 20
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    camera_offset_y -= 20
                # Zoom
                elif event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                    zoom_level = min(2.0, zoom_level + 0.1)
                elif event.key == pygame.K_MINUS:
                    zoom_level = max(0.5, zoom_level - 0.1)

        screen.fill(BG_COLOR)

        # Draw rooms
        for room in tower_rooms:
            room.draw(screen)
        draw_base(screen)
        for room in basement_rooms:
            room.draw(screen)

        # Draw UI
        build_button.draw(screen)
        dig_button.draw(screen)
        draw_resources(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
