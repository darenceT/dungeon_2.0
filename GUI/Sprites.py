import pygame
from random import randint
from .Settings import *


class Sprites:
    def __init__(self, game_data):
        """
        Pass in game_data primarily for object_coords, and potentially for Room objects also.
        Potion and trap images from www.pngegg.com
        """
        self.game_data = game_data.maze
        # self.object_coords = self.game_data.object_coords
        self.list_of_objects = []
        self.__create_sprites()
    

    def __create_sprites(self):
        # temp coords, will obtain from game_data later
        object_coords = {
            'H': [(0, 1), (2, 1)],
            'V': [(1, 1), (2, 2)],
            'X': [(0, 1), (2, 1)],
            'A': [(1, 1)],
            'E': [(2, 1)],
            'I': [(2, 2)],
            'P': [(0, 3)],
            'O': [self.game_data.egress.coords]
        }

        self.sprite_types = {
            'H': pygame.image.load('GUI/img/h_potion.png').convert_alpha(),
            'V': pygame.image.load('GUI/img/v_potion.png').convert_alpha(),
            'X': pygame.image.load('GUI/img/v_potion.png').convert_alpha(),
            'A': pygame.image.load('GUI/img/pillar.png').convert_alpha(),
            'E': pygame.image.load('GUI/img/pillar.png').convert_alpha(),
            'I': pygame.image.load('GUI/img/pillar.png').convert_alpha(),
            'P': pygame.image.load('GUI/img/pillar.png').convert_alpha(),
            'O': pygame.image.load('GUI/img/exit.png').convert_alpha()
            }

        scale = 0.4
        shift = 1.8
        for letter, coords in object_coords.items():
            for pos in coords:
                if letter == 'O':
                    scale = 1
                    shift = 0
                self.list_of_objects.append(SpriteObject(self.sprite_types[letter], True, pos, shift, scale))

class SpriteObject:
    def __init__(self, object, static, pos, shift, scale):
        self.object = object
        self.static = static        # consider delete
        self.x = convert_coords_pixel(pos[0]) + randint(10, 30)
        self.y = convert_coords_pixel(pos[1]) + randint(10, 30)
        self.shift = shift
        self.scale = scale

        # if not static:
        #     self.sprite_angles = [frozenset(range(i, i + 45)) for i in range(0, 360, 45)]
        #     self.sprite_positions = {angle: pos for angle, pos in zip(self.sprite_angles, self.object)}

    def object_locate(self, player, walls):
        fake_walls0 = [walls[0] for _ in range(FAKE_RAYS)]
        fake_walls1 = [walls[-1] for _ in range(FAKE_RAYS)]
        fake_walls = fake_walls0 + walls + fake_walls1

        dx, dy = self.x - player.x, self.y - player.y
        distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)

        theta = math.atan2(dy, dx)
        gamma = theta - player.angle
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += DOUBLE_PI

        delta_rays = int(gamma / DELTA_ANGLE)
        current_ray = CENTER_RAY + delta_rays
        distance_to_sprite *= math.cos(HALF_FOV - current_ray * DELTA_ANGLE)

        fake_ray = current_ray + FAKE_RAYS
        if 0 <= fake_ray <= NUM_RAYS - 1 + 2 * FAKE_RAYS and distance_to_sprite < fake_walls[fake_ray][0]:
            if distance_to_sprite == 0: distance_to_sprite = 1      # Fixes bug of 0 division
            proj_height = min(int(PROJ_COEFF / distance_to_sprite * self.scale), 2 * HEIGHT)
            half_proj_height = proj_height // 2
            shift = half_proj_height * self.shift

            # if not self.static:
            #     if theta < 0:
            #         theta += DOUBLE_PI
            #     theta = 360 - int(math.degrees(theta))

            #     for angles in self.sprite_angles:
            #         if theta in angles:
            #             self.object = self.sprite_positions[angles]
            #             break

            sprite_pos = (current_ray * SCALE - half_proj_height, HALF_HEIGHT - half_proj_height + shift)
            sprite = pygame.transform.scale(self.object, (proj_height, proj_height))
            return (distance_to_sprite, sprite, sprite_pos)
        else:
            return (False,)