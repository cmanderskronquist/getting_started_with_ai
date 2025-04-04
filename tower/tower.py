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

# Tower data
tower_rooms = []

class Room:
    def __init__(self, y):
        self.width = 120
        self.height = 40
        self.x = WIDTH // 2 - self.width // 2
        self.y = y

    def draw(self, surface):
        pygame.draw.rect(surface, ROOM_COLOR, (self.x, self.y, self.width, self.height))
        label = font.render("Room", True, TEXT_COLOR)
        surface.blit(label, (self.x + 30, self.y + 10))

class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, surface):
        pygame.draw.rect(surface, BUTTON_COLOR, self.rect)
        label = font.render(self.text, True, TEXT_COLOR)
        surface.blit(label, (self.rect.x + 10, self.rect.y + 10))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Button instance (right column)
build_button = Button(WIDTH - 150, 100, 120, 40, "Build Room")

def main():
    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if build_button.is_clicked(event.pos):
                    # Stack a new room above existing ones
                    if tower_rooms:
                        top_y = tower_rooms[-1].y - 45
                    else:
                        top_y = HEIGHT - 100
                    tower_rooms.append(Room(top_y))

        screen.fill(BG_COLOR)

        # Draw tower base
        pygame.draw.rect(screen, TOWER_BASE_COLOR, (WIDTH//2 - 100, HEIGHT - 50, 200, 50))

        # Draw rooms
        for room in tower_rooms:
            room.draw(screen)

        # Draw build button
        build_button.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
