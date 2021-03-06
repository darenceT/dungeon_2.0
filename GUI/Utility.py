import pygame
from .Settings import *

"""
Multiple helper functions for calculations in GUI/View code
Used in Sprites, Drawing, and PlayerControls
"""

def convert_pixel_to_coords(loc: tuple):
    """
    Convert pixel location into room coordinate, opposite of below
    :return: room coordinates (x, y)
    :rtype: tuple (int, int)
    """
    return round((loc[0] - 120) / 160), round((loc[1] - 120) / 160)

def convert_coords_to_pixel(coord: tuple):
    """
    Convert room coordinates into pixel location, opposite of above
    :return: pixel location (x, y)
    :rtype: tuple (float, float)
    """
    adjust_center = 120
    return int(2 * coord[0] * WIDTH / TEXTURE_SCALE + adjust_center), \
    int(2 * coord[1] * HEIGHT / TEXTURE_SCALE + adjust_center)

def convert_coords_to_map(pos: tuple):
    """
    Convert room coordinates into pixel location for map
    :return: map coordinates (x, y)
    :rtype: tuple (int, int)
    """
    coord_x, coord_y = convert_coords_to_pixel(pos) 
    return coord_x // MAP_SCALE - MAP_TILE, coord_y // MAP_SCALE - MAP_TILE

def direction_of_vision(player_angle: float):
    """
    Using some simple trigo for compass direction!
    :return: one direction (NOT the band!)
    :rtype: str
    """
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
    :return: surface object of text and it's coordinates
    :rtype: tuple (pygame.surface(), pygame.rect())
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