from Settings import *
import pygame
import math

class Player:
    def __init__(self, entrance_loc, screen, world_raw):
        self.x = 120    # constant since x_loc always at 0
        self.y = int(WIDTH / 9 * 2 * entrance_loc[1]) + 120
        self.angle = 0
        self.player_speed = 4
        self.screen = screen
        self.world_raw = world_raw

    def __init__old(self, screen, player_pos, map):
        self.screen = screen
        self.x, self.y = player_pos
        self.angle = 0
        self.player_speed = 4
        self.map = map

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
        if keys[pygame.K_TAB]:
            self.mini_map()

    def map(self):
        pygame.draw.circle(self.screen, 'green', (int(self.x), int(self.y)), 12)
        pygame.draw.line(self.screen, 'green', self.pos, (self.x + WIDTH * math.cos(self.angle),
                                                self.y + WIDTH * math. sin(self.angle)), 2)
        for x,y in self.world_raw:
            pygame.draw.rect(self.screen, 'gray', (x, y, TILE, TILE), 2)

    def mini_map(self):
        """
        Creates map top left corner with player's position and 
        the direction player is facing on map
        Hold Tab during game to view map
        """
        for row in range(MAP_SIZE):
            for col in range(MAP_SIZE):
                index = row*25 + col*3       #TODO improve calculation
                map_color = None
                if self.map[index] == '+' or self.map[index] == '-' or self.map[index] == '|':
                    map_color = 'black'
                else:
                    map_color = 'orange'

                square = TILE_SIZE / 4
                pygame.draw.rect(self.screen, map_color,
                    (col * square, row * square, square, square))
