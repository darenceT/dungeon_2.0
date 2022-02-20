import pygame
from random import randint
from .Settings import *


class Sprites:
    def __init__(self):
        """
        potions from www.pngegg.com
        """
        self.sprite_types = {
            'h_pot': pygame.image.load('GUI/img/h_potion.png').convert_alpha(),
            'v_pot': pygame.image.load('GUI/img/v_potion.png').convert_alpha(),
            'trap': pygame.image.load('GUI/img/trap.png').convert_alpha(),
            }
        #     'devil': [pygame.image.load(f'sprites/devil/{i}.png').convert_alpha() for i in range(8)]
        # }
        self.list_of_objects = [
            SpriteObject(self.sprite_types['h_pot'], True, (1, 3), 1.8, 0.4),
            SpriteObject(self.sprite_types['h_pot'], True, (1, 1), 1.8, 0.4),
            SpriteObject(self.sprite_types['v_pot'], True, (1, 2), 1.6, 0.5),
            SpriteObject(self.sprite_types['v_pot'], True, (1, 0), 1.6, 0.5),
            SpriteObject(self.sprite_types['trap'], True, (2, 2), 1.6, 0.5),
            SpriteObject(self.sprite_types['trap'], True, (1, 2), 1.6, 0.5),
        ]
        #     SpriteObject(self.sprite_types['devil'], False, (7, 4), -0.2, 0.7),
        # ]

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