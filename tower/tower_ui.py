import pygame

# Colors
BUTTON_COLOR = (200, 240, 200)
TEXT_COLOR = (0, 0, 0)

# Font (must be initialized in main file after pygame.init())
font = None  # placeholder

def init_font():
    global font
    font = pygame.font.SysFont(None, 24)

class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, surface):
        pygame.draw.rect(surface, BUTTON_COLOR, self.rect)
        label = font.render(self.text, True, TEXT_COLOR)
        surface.blit(label, (self.rect.x + 5, self.rect.y + 10))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def draw_resources(surface, resources, x=20, y=20):
    for resource, amount in resources.items():
        label = font.render(f"{resource}: {amount}", True, TEXT_COLOR)
        surface.blit(label, (x, y))
        y += 30
