import pygame
from .Settings import *


def convert_coords_to_pixel(coord: int):
    adjust_center = 120
    return int(2 * coord * WIDTH / TEXTURE_SCALE + adjust_center)

def create_textline(message, 
                    pos=(HALF_WIDTH, HALF_HEIGHT), 
                    font_type="GUI/font/Damned.ttf", 
                    size=32, 
                    color=DARK_RED):
    """
    Create text object for surface.
    Credit: https://www.geeksforgeeks.org/python-display-text-to-pygame-window/
    """
    font = pygame.font.Font(font_type, size)
    text = font.render(message, True, color)
    textRect = text.get_rect()
    textRect.center = pos
    return text, textRect