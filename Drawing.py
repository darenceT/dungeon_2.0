import pygame

from GuiSettings import *

class Drawing: 
    def __init__(self, screen) -> None:
        self.screen = screen
        self.textures = {'ceiling': pygame.image.load('img/ceiling.jfif').convert(),
                         'floor': pygame.image.load('img/floor.jpg').convert(),
                        }
    
    def background(self, angle):
        # Ceiling
        ceiling_offset = -5 * math.degrees(angle) % SCREEN_HEIGHT
        self.screen.blit(self.textures['ceiling'], (ceiling_offset, 0))
        self.screen.blit(self.textures['ceiling'], (ceiling_offset - SCREEN_HEIGHT, 0))
        self.screen.blit(self.textures['ceiling'], (ceiling_offset + SCREEN_HEIGHT, 0))
        pygame.draw.rect(self.screen, (100, 100, 100), (0, SCREEN_HEIGHT / 2, SCREEN_HEIGHT, SCREEN_HEIGHT))
        
        # Floor
        pygame.draw.rect(self.screen, (200, 200, 200), (0, -SCREEN_HEIGHT / 2, SCREEN_HEIGHT, SCREEN_HEIGHT))