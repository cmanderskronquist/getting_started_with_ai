import pygame

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