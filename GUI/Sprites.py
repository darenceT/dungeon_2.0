import pygame
from random import randint, randrange
from collections import deque
from .Settings import *
from .Utility import convert_coords_to_pixel


class SpriteObject:
    def __init__(self, image, name, pos, shift=1.8, scale=0.4,
                 animation=None):
        self.image = image
        self.name = name
        self.x = convert_coords_to_pixel(pos[0]) # + randint(1, 20)
        self.y = convert_coords_to_pixel(pos[1]) # + randint(1, 20)
        self.shift = shift
        self.scale = scale
        self.visible_health = False
        self.animation = animation
        self.animate_count = 0
        self.animate_speed = 6
        # self.sound = True

        # self.hitpoint = 150 # temporary
        # self.attack_damage = 5 # temporary

class SpritesContainer:
    def __init__(self, screen, sound, game, player):
        """
        Initial loading images of sprites
        Container of sprites for current and nearby rooms 
        images from www.pngegg.com
        """
        self.screen = screen
        self.sound = sound
        self.player = player
        self.game = game
        self.nearby_sprites = set()
        self.images = {
            'H': pygame.image.load('GUI/img/h_potion.png').convert_alpha(),
            'V': pygame.image.load('GUI/img/v_potion.png').convert_alpha(),
            'X': pygame.image.load('GUI/img/trap.png').convert_alpha(),
            'pillar': pygame.image.load('GUI/img/pillar.png').convert_alpha(),
            'exit': pygame.image.load('GUI/img/exit.png').convert_alpha(),
        }
        self.monsters = {
            'ogre':{
                'sprite': pygame.image.load('GUI/img/ogre0.png').convert_alpha(),
                'shift': 0.2,
                'scale': 0.8,
                'animation': deque([pygame.image.load(f'GUI/img/ogre{i}.png').convert_alpha() for i in range(1, 4)]),
            },
            'mgirl':{
                'sprite': pygame.image.load('GUI/img/mgirl0.png').convert_alpha(),
                'shift': 0.3,
                'scale': 0.8,
                'animation': deque([pygame.image.load(f'GUI/img/mgirl{i}.png').convert_alpha() for i in range(1, 4)]),
            },
            'gremlin':{
                'sprite': pygame.image.load('GUI/img/gremlin0.png').convert_alpha(),
                'shift': 0.3,
                'scale': 0.8,
                'animation': deque([pygame.image.load(f'GUI/img/gremlin{i}.png').convert_alpha() for i in range(1, 4)]),
            },
            'skeleton':{
                'sprite': pygame.image.load('GUI/img/skeleton0.png').convert_alpha(),
                'shift': 0.3,
                'scale': 0.8,
                'animation': deque([pygame.image.load(f'GUI/img/skeleton{i}.png').convert_alpha() for i in range(1, 4)]),
            },
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
                if room.occupants:
                    for npc in room.occupants:
                        add(SpriteObject(self.monsters[npc.mtype]['sprite'], npc.mtype, room.coords, 
                                        scale=self.monsters[npc.mtype]['scale'], 
                                        shift=self.monsters[npc.mtype]['shift'],
                                        animation=self.monsters[npc.mtype]['animation'].copy(),
                                        )) 
                if room.healing_potions:
                    for _ in range(room.healing_potions):
                        add(SpriteObject(self.images['H'], 'H', room.coords))
                        # types = ('ogre', 'mgirl', 'gremlin')
                        # npc = types[randrange(3)] 
                if room.vision_potions:
                    for _ in range(room.vision_potions):
                        add(SpriteObject(self.images['V'], 'V', room.coords))        
                if room.has_pit:
                    # room.has_pit = False
                    add(SpriteObject(self.images['X'], 'X', room.coords)) 
                if room.pillar:
                    add(SpriteObject(self.images['pillar'], 'pillar', room.coords))
                if room.is_exit:
                    add(SpriteObject(self.images['exit'], 'exit', room.coords, scale=1, shift=0))
    
    def obtain_sprites(self, walls):
        """"
        Obtain location of each sprite object in relation to player and nearby walls
        Copy of container used to avoid iteration error from object removal in object_locate
        """
        temp_container = self.nearby_sprites.copy()
        return [self.object_locate(obj, walls) for obj in temp_container]

    def object_locate(self, sprite, walls):
        """
        Use raycasting to determine distance between hero and sprite objects
        Credit algo to: https://github.com/StanislavPetrovV/Raycasting-3d-game-tutorial/blob/master/part%20%232/ray_casting.py
        """
        fake_walls0 = [walls[0] for _ in range(FAKE_RAYS)]
        fake_walls1 = [walls[-1] for _ in range(FAKE_RAYS)]
        fake_walls = fake_walls0 + walls + fake_walls1

        dx, dy = sprite.x - self.player.x, sprite.y - self.player.y
        distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)
        
        # trigger game events by distance
        self.__interact_sprites(sprite, distance_to_sprite)


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
            sprite = pygame.transform.scale(sprite.image, (proj_height, proj_height))
            return (distance_to_sprite, sprite, sprite_pos)
        else:
            return (False,)
    

    def __interact_sprites(self, sprite, distance):
        """
        Use distance calculated from object_locate() to trigger model & view events
        """
        # display monster health
        sprite.visible_health = True if distance < 80 and sprite.animation else False
            
        # interact with pillars, trap, and monsters
        if distance < 50:
            if sprite.name == 'pillar' and self.game.room.pillar and \
            self.game.room.pillar not in self.game.hero.pillars:
                self.sound.pillar()
                self.player.new_pillar = self.game.room.pillar
                self.game.find_pillar()
            elif sprite.name in ('ogre', 'mgirl', 'gremlin', 'skeleton'):
                # play monster sound
                if sprite.name not in self.sound.monster_sounds:
                    self.sound.monster_sounds = (sprite.name, False) 
                    self.sound.monster_play(sprite.name)

                npc = None
                for monster in self.game.room.occupants:
                    if monster.mtype == sprite.name:
                        npc = monster
                # battle logic
                if npc is not None:
                    self.player.arena.fight(npc)
                # else:
                #     raise TypeError('Incongruency with monster sprite exist but actual monster does not')

                # animate monster
                sprite.image = sprite.animation[0]
                if sprite.animate_count < sprite.animate_speed:
                    sprite.animate_count += 1
                else:
                    sprite.animation.rotate()
                    sprite.animate_count = 0
                
                # remove monster GUI and stop monster sound
                if npc is not None and npc.hit_points <= 0:
                    self.sound.monster_play(sprite.name, off=True)
                    self.sound.monster_sounds = (sprite.name, True)                
                    self.nearby_sprites.remove(sprite)
            # TODO insert pit interaction
        
        # pickup potions
        if distance < 40: 
            if sprite.name in ('H', 'V'):
                self.sound.pickup()
                self.nearby_sprites.remove(sprite)          
                if sprite.name == 'H' and self.game.room.healing_potions:
                    self.game.find_healing_potion()
                elif sprite.name == 'V' and self.game.room.vision_potions:
                    self.game.find_vision_potion()