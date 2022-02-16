import pygame
import math
from Settings import *
from Drawing import Drawing

class Player:
    def __init__(self, entrance_loc, screen, world_raw):
        self.x = 120    # constant since x_loc always at 0
        self.y = int(WIDTH / 9 * 2 * entrance_loc[1]) + 120
        self.angle = 0
        self.player_speed = 4
        self.screen = screen
        self.world_raw = world_raw

    @property
    def pos(self):
        return (self.x, self.y)

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.x += self.player_speed * cos_a
            self.y += self.player_speed * sin_a
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.x += -self.player_speed * cos_a
            self.y += -self.player_speed * sin_a
        if keys[pygame.K_a]:
            self.x += self.player_speed * sin_a
            self.y += -self.player_speed * cos_a
        if keys[pygame.K_d]:
            self.x += -self.player_speed * sin_a
            self.y += self.player_speed * cos_a
        if keys[pygame.K_LEFT]:
            self.angle -= 0.02
        if keys[pygame.K_RIGHT]:
            self.angle += 0.02
        # if keys[pygame.K_TAB]:
        #     Drawing.

