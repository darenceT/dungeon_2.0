import pygame
from random import randint
from .Settings import *


class Sprites:
    def __init__(self, rooms):
        """
        images from www.pngegg.com
        """
        self.rooms = rooms
        # self.object_coords = self.game_data.object_coords
        self.sprite_types = {
            'H': pygame.image.load('GUI/img/h_potion.png').convert_alpha(),
            'V': pygame.image.load('GUI/img/v_potion.png').convert_alpha(),
            'X': pygame.image.load('GUI/img/v_potion.png').convert_alpha(),
            'A': pygame.image.load('GUI/img/pillar.png').convert_alpha(),
            'E': pygame.image.load('GUI/img/pillar.png').convert_alpha(),
            'I': pygame.image.load('GUI/img/pillar.png').convert_alpha(),
            'P': pygame.image.load('GUI/img/pillar.png').convert_alpha(),
            'O': pygame.image.load('GUI/img/exit.png').convert_alpha(),
            'M': pygame.image.load('GUI/img/monster.png').convert_alpha()
            }
        self.list_of_sprites = []
    

    def reload_sprites(self, curr_room):
        self.list_of_sprites = []

        def __create_sprite(letter, coords, shift=1.8, scale=0.4):
            self.list_of_sprites.append(SpriteObject(self.sprite_types[letter], coords, shift, scale))

        def peek_room(room):
            if room.healing_potions:
                for _ in range(room.healing_potions):
                    __create_sprite('H', room.coords)
            if room.vision_potions:
                for _ in range(curr_room.healing_potions):
                    __create_sprite('V', room.coords)            
            if room.has_pit:
                __create_sprite('X', room.coords)
            if room.pillar:
                __create_sprite(room.pillar, room.coords)
            if room.is_exit:
                __create_sprite('O', room.coords, scale=1, shift=0)
        
        peek_room(curr_room)

        x1, y1 = curr_room.coords
        x1 += 1
        peek_room(self.rooms[y1][x1])           # make method accept set() of rooms

class SpriteObject:
    def __init__(self, object, pos, shift, scale):
        self.object = object
        # self.static = static        # consider delete
        self.x = convert_coords_pixel(pos[0]) + randint(1, 20)
        self.y = convert_coords_pixel(pos[1]) + randint(1, 20)
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