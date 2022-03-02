import pygame
from random import randint
from .Settings import *

class SpriteObject:
    def __init__(self, object, letter, pos, shift=1.8, scale=0.4):
        self.object = object
        self.letter = letter
        self.x = convert_coords_to_pixel(pos[0]) + randint(1, 20)
        self.y = convert_coords_to_pixel(pos[1]) + randint(1, 20)
        self.shift = shift
        self.scale = scale
        self.visible_health = False
        self.hitpoint = 50 # temporary

class SpritesContainer:
    def __init__(self, screen, game, player):
        """
        Initial loading images of sprites
        Container of sprites for current and nearby rooms 
        images from www.pngegg.com
        """
        self.screen = screen
        self.player = player
        self.weapon_animate = 1
        self.game = game
        self.nearby_sprites = set()
        self.images = {
            'H': pygame.image.load('GUI/img/h_potion.png').convert_alpha(),
            'V': pygame.image.load('GUI/img/v_potion.png').convert_alpha(),
            'X': pygame.image.load('GUI/img/trap.png').convert_alpha(),
            'A': pygame.image.load('GUI/img/pillar.png').convert_alpha(),
            'E': pygame.image.load('GUI/img/pillar.png').convert_alpha(),
            'I': pygame.image.load('GUI/img/pillar.png').convert_alpha(),
            'P': pygame.image.load('GUI/img/pillar.png').convert_alpha(),
            'O': pygame.image.load('GUI/img/exit.png').convert_alpha(),
            'M': pygame.image.load('GUI/img/monster.png').convert_alpha(),
            'S0': pygame.image.load('GUI/img/sword0.png').convert_alpha(),
            'S1': pygame.image.load('GUI/img/sword1.png').convert_alpha(),
            'S2': pygame.image.load('GUI/img/sword2.png').convert_alpha()
            }
        
    def load_sprites(self):
        """
        First, empty list of sprites after entering new location, therefore will not
        load sprites from rooms no longer in view

        Iterate through set of rooms in view to load sprites
        """
        if self.player.room_change:
            self.nearby_sprites = set()
            add = self.nearby_sprites.add
            for room in self.player.rooms_in_sight:
                if room.healing_potions:
                    for _ in range(room.healing_potions):
                        add(SpriteObject(self.images['H'], 'H', room.coords))
                if room.vision_potions:
                    for _ in range(room.vision_potions):
                        add(SpriteObject(self.images['V'], 'V', room.coords))
                        # add(SpriteObject(self.images['M'], 'M', room.coords, scale=0.8, shift=0.2))            
                if room.has_pit:
                    # room.has_pit = False
                    add(SpriteObject(self.images['X'], 'X', room.coords))
                    add(SpriteObject(self.images['M'], 'M', room.coords, scale=0.8, shift=0.2)) 
                if room.pillar:
                    add(SpriteObject(self.images[room.pillar], room.pillar, room.coords))
                if room.is_exit:
                    add(SpriteObject(self.images['O'], 'O', room.coords, scale=1, shift=0))
    
    def obtain_sprites(self, walls):
        """"
        Obtain location of each sprite object in relation to player and nearby walls
        Copy of container used to avoid iteration error from object removal in object_locate
        """
        temp_container = self.nearby_sprites.copy()
        return [self.object_locate(obj, walls) for obj in temp_container]

    def object_locate(self, sprite, walls):
        """
        
        Credit most of algo to: Credit: https://github.com/StanislavPetrovV/Raycasting-3d-game-tutorial/blob/master/part%20%232/ray_casting.py
        """
        fake_walls0 = [walls[0] for _ in range(FAKE_RAYS)]
        fake_walls1 = [walls[-1] for _ in range(FAKE_RAYS)]
        fake_walls = fake_walls0 + walls + fake_walls1

        dx, dy = sprite.x - self.player.x, sprite.y - self.player.y
        distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)
        
        sprite.visible_health = True if distance_to_sprite < 100 and sprite.letter == 'M' else False
            
        # collect objects
        if distance_to_sprite < 20:
            if sprite.letter == 'H' and self.game.room.healing_potions:
                self.game.find_healing_potion()
                self.nearby_sprites.remove(sprite)
            elif sprite.letter == 'V' and self.game.room.vision_potions:
                self.game.find_vision_potion()
                self.nearby_sprites.remove(sprite)
            elif sprite.letter == 'M' and self.player.attacking:
                if sprite.hitpoint <= 0:
                    self.nearby_sprites.remove(sprite)
                    self.game.room.has_pit = False
                    print('you defeated monster')
                sprite.hitpoint -= 5   # TODO substitute for weapon damage

            # insert interaction with PIT and Pillars

        theta = math.atan2(dy, dx)
        gamma = theta - self.player.angle
        if dx > 0 and 180 <= math.degrees(self.player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += DOUBLE_PI

        delta_rays = int(gamma / DELTA_ANGLE)
        current_ray = CENTER_RAY + delta_rays
        distance_to_sprite *= math.cos(HALF_FOV - current_ray * DELTA_ANGLE)

        fake_ray = current_ray + FAKE_RAYS
        if 0 <= fake_ray <= NUM_RAYS - 1 + 2 * FAKE_RAYS and distance_to_sprite < fake_walls[fake_ray][0]:
            if distance_to_sprite == 0: distance_to_sprite = 1      # Fixes bug of 0 division
            proj_height = min(int(PROJ_COEFF / distance_to_sprite * sprite.scale), 2 * HEIGHT)
            half_proj_height = proj_height // 2
            shift = half_proj_height * sprite.shift

            sprite_pos = (current_ray * SCALE - half_proj_height, HALF_HEIGHT - half_proj_height + shift)
            sprite = pygame.transform.scale(sprite.object, (proj_height, proj_height))
            return (distance_to_sprite, sprite, sprite_pos)
        else:
            return (False,)
    
    def weapon(self):
        # TODO change weapon "S" based on hero's class
        wep_pos = (WIDTH *2/5, HEIGHT * 5/8)
        if self.player.attacking and self.weapon_animate < 3:
            weapon = pygame.transform.scale(self.images[f'S{self.weapon_animate}'], wep_pos)
            self.screen.blit(weapon, wep_pos)
            self.weapon_animate += 1
        else:
            weapon = pygame.transform.scale(self.images['S0'], wep_pos)
            self.weapon_animate = 1
            self.player.attacking = False
        self.screen.blit(weapon, wep_pos)