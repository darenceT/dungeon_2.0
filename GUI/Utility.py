import pygame
from .Settings import *


def convert_coords_to_pixel(coord: int):
    adjust_center = 120
    return int(2 * coord * WIDTH / TEXTURE_SCALE + adjust_center)

def direction_of_vision(player_angle: float):
    if 5/4 * PI < player_angle < 7/4 * PI:
        direction = 'north'  
    elif PI/4 < player_angle <= 3/4 * PI:
        direction = 'south'
    elif 3/4 * PI < player_angle <= 5/4 * PI:
        direction = 'west'
    else: # covers range of player_angle <= PI/4 or player_angle >= 7/4
        direction = 'east'
    return direction
    
def create_textline(message, 
                    pos=(HALF_WIDTH, HALF_HEIGHT), 
                    font_type="GUI/font/Damned.ttf", 
                    size=32, 
                    color=DARK_RED,
                    pos_type='center'):
    """
    Create text object for surface.
    Credit: https://www.geeksforgeeks.org/python-display-text-to-pygame-window/
    """
    font = pygame.font.Font(font_type, size)
    text = font.render(message, True, color)
    textRect = text.get_rect()
    if pos_type == 'center':
        textRect.center = pos
    elif pos_type == 'xy':
        textRect.x, textRect.y = pos
    else:
        raise ValueError(f'{pos_type} not recognized or not implemented')
    return text, textRect