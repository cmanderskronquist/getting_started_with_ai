import pygame
from tower_config import BUTTON_COLOR, TEXT_COLOR, FONT

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

def draw_resources(surface, resources, x=20, y=20):
    for resource, amount in resources.items():
        label = FONT.render(f"{resource}: {amount}", True, TEXT_COLOR)
        surface.blit(label, (x, y))
        y += 30