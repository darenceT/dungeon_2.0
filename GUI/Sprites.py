import pygame
from collections import deque
from .Settings import *
from .Utility import convert_coords_to_pixel, convert_pixel_to_coords


class SpriteObject:
    """
    Objects that you see in GUI: potions, traps, exit door, monsters
    """
    ANIMATE_SPEED = 6
    def __init__(self, image, name, pos, object=None, shift=1.8, scale=0.4,
                 animation=None):
        self.__image = image
        self.__name = name
        self.__x, self.__y = convert_coords_to_pixel(pos) # + randrange(6)
        self.__object = object
        self.__shift = shift
        self.__scale = scale
        self.__visible_health = False
        self.__animation = animation
        self.__animate_count = 0

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, animate_image):
        #TODO add error check for pygame.image type
        if isinstance(animate_image, pygame.Surface):
            self.__image = animate_image
        else:
            raise TypeError('Sprite.image only accepts Pygame.Surface type')

    @property
    def name(self):
        return self.__name

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def object(self):
        return self.__object

    @property
    def shift(self):
        return self.__shift

    @property
    def scale(self):
        return self.__scale

    @property
    def visible_health(self):
        return self.__visible_health

    @visible_health.setter
    def visible_health(self, change):
        """
        Setter to change boolean value accessed in SpritesContainer.object_locate()
        """
        if isinstance(change, bool):
            if not change:
                self.__visible_health = False
            else:
                self.__visible_health = True
        else:
            raise TypeError('Only boolean accepted for pause_on')

    @property
    def animation(self):
        return self.__animation

    @property
    def animate_count(self):
        return self.__animate_count

    @animate_count.setter
    def animate_count(self, num):
        if isinstance(num, int):
            self.__animate_count = num
        else:
            raise TypeError('Only int accepted for animate count')

    def __str__(self): 
        return f'{self.__name} SpriteObject'

    def __repr__(self):
        return f'''SpriteObject({self.__image}, {self.__name}, 
                    {convert_pixel_to_coords((self.__x, self.__y))}, object={self.__object}, 
                    shift={self.__scale}, scale={self.__scale})'''

class SpritesContainer:
    def __init__(self, screen, sound, game, player):
        """
        Initial loading images of sprites
        Container of sprites for current and nearby rooms 
        images from www.pngegg.com
        """
        self.__screen = screen
        self.__sound = sound
        self.__player = player
        self.__game = game
        self.__nearby_sprites = set()
        self.__sprite_still = {
            'H': pygame.image.load('GUI/img/h_potion.png').convert_alpha(),
            'V': pygame.image.load('GUI/img/v_potion.png').convert_alpha(),
            'pillar': pygame.image.load('GUI/img/pillar.png').convert_alpha(),
            'exit': pygame.image.load('GUI/img/exit.png').convert_alpha(),
        }
        self.__sprite_animate = {
            'trap':{
                'sprite': pygame.image.load('GUI/img/trap0.png').convert_alpha(),
                'shift': 1.5,
                'scale': 0.6,
                'animation': deque([pygame.image.load(f'GUI/img/trap{i}.png').convert_alpha() for i in range(1, 3)]),
            },            
            'ogre':{
                'sprite': pygame.image.load('GUI/img/ogre0.png').convert_alpha(),
                'shift': 0.3,
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
                'shift': 0.5,
                'scale': 0.8,
                'animation': deque([pygame.image.load(f'GUI/img/skeleton{i}.png').convert_alpha() for i in range(1, 4)]),
            },
        }

    @property
    def nearby_sprites(self):
        return self.__nearby_sprites
        
    def load_sprites(self):
        """
        First, empty list of sprites after entering new location, therefore will not
        load sprites from rooms no longer in view

        Iterate through set of rooms in view to load sprites
        :return: None
        """
        if self.__player.ready_for_new_sprites:
            self.__nearby_sprites = set()
            add = self.__nearby_sprites.add
            for room in self.__player.rooms_in_sight:
                if room.occupants:
                    for npc in room.occupants:
                        add(SpriteObject(image=self.__sprite_animate[npc.mtype]['sprite'], 
                                        name=npc.mtype, 
                                        pos=room.coords, 
                                        object=npc, 
                                        scale=self.__sprite_animate[npc.mtype]['scale'], 
                                        shift=self.__sprite_animate[npc.mtype]['shift'], 
                                        animation=self.__sprite_animate[npc.mtype]['animation'].copy())) 
                if room.healing_potions:
                    for _ in range(room.healing_potions):
                        add(SpriteObject(self.__sprite_still['H'], 'H', room.coords))
                if room.vision_potions:
                    for _ in range(room.vision_potions):
                        add(SpriteObject(self.__sprite_still['V'], 'V', room.coords))        
                if room.has_pit:
                    add(SpriteObject(image=self.__sprite_animate['trap']['sprite'], 
                                     name='trap', 
                                     pos=room.coords, 
                                     scale=self.__sprite_animate['trap']['scale'], 
                                     shift=self.__sprite_animate['trap']['shift'], 
                                     animation=self.__sprite_animate['trap']['animation'].copy())) 
                if room.pillar:
                    add(SpriteObject(self.__sprite_still['pillar'], 'pillar', room.coords))
                if room.is_exit:
                    add(SpriteObject(self.__sprite_still['exit'], 'exit', room.coords, scale=1, shift=0))
    
    def obtain_sprites(self, walls):
        """"
        Obtain location of each sprite object in relation to player and nearby walls
        Copy of container used to avoid iteration error from object removal in object_locate
        :return: list of objects with information of distance to player's field of vision
        :rtype: list[tuple(float, SpriteObject, tuple(float, float))]
        """
        temp_container = self.__nearby_sprites.copy()
        return [self.object_locate(obj, walls) for obj in temp_container]

    def object_locate(self, sprite, walls):
        """
        Use raycasting to determine distance between hero and sprite objects
        Credit algo to: https://github.com/StanislavPetrovV/Raycasting-3d-game-tutorial/blob/master/part%20%232/ray_casting.py
        :return: sprite object in player's field of vision, therefore sprite's position & distance
        :rtype: tuple(float, SpriteObject, tuple(float, float))
        """
        fake_walls0 = [walls[0] for _ in range(FAKE_RAYS)]
        fake_walls1 = [walls[-1] for _ in range(FAKE_RAYS)]
        fake_walls = fake_walls0 + walls + fake_walls1

        dx, dy = sprite.x - self.__player.x, sprite.y - self.__player.y
        distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)
        
        # trigger game events by distance
        self.__interact_sprites(sprite, distance_to_sprite)

        theta = math.atan2(dy, dx)
        gamma = theta - self.__player.angle
        if dx > 0 and 180 <= math.degrees(self.__player.angle) <= 360 or dx < 0 and dy < 0:
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
        :return: None
        """
        # display monster health
        if distance < 80 and sprite.name in ('ogre', 'mgirl', 'gremlin', 'skeleton'):
            sprite.visible_health = True
        else:
            sprite.visible_health = False

        # interact ("seeing") pillars
        if distance < 55:
            if sprite.name == 'pillar' and self.__game.room.pillar and \
            self.__game.room.pillar not in self.__game.hero.pillars:
                self.__sound.pillar()
                self.__player.new_pillar = self.__game.room.pillar
                self.__game.find_pillar()

        # interact with trap, and monsters
        if distance < 50:

            if sprite.name in ('ogre', 'mgirl', 'gremlin', 'skeleton'):
                # play monster
                if sprite.name not in self.__sound.monster_sounds:
                    self.__sound.monster_sounds = (sprite.name, False) 
                    self.__sound.monster_play(sprite.name)

                self.__player.fight_alone = False
                self.__player.arena.fight(sprite.object)

                # animate monster
                sprite.image = sprite.animation[0]
                if sprite.animate_count < SpriteObject.ANIMATE_SPEED:
                    sprite.animate_count += 1
                else:
                    sprite.animation.rotate()
                    sprite.animate_count = 0
                
                # remove monster GUI and stop monster sound
                if not sprite.object.is_alive:
                    # turn off monster specific sound
                    self.__sound.monster_play(sprite.name, off=True)
                    self.__sound.monster_sounds = (sprite.name, True)
                    
                    self.__sound.defeat_monster()
                    print(f"\nYou defeated {sprite.object.mtype}!\n{sprite.object}")                
                    self.__nearby_sprites.remove(sprite)
                    # remove monster object from room
                    self.__player.cur_room.occupants = (sprite.object, True)
                    self.__player.fight_alone = True
            else:
                self.__player.fight_alone = True
            
            if sprite.name == 'trap':
                sprite.image = sprite.animation[0]
                if sprite.animate_count < SpriteObject.ANIMATE_SPEED:
                    sprite.animate_count += 1
                else:
                    sprite.animation.rotate()
                    sprite.animate_count = 0
                    self.__game.hero.hit_points -= 1 # temporary, will connect to trap object

        # pickup potions
        if distance < 40: 
            if sprite.name in ('H', 'V'):
                self.__sound.pickup()
                self.__nearby_sprites.remove(sprite)          
                if sprite.name == 'H' and self.__game.room.healing_potions:
                    self.__game.find_healing_potion()
                elif sprite.name == 'V' and self.__game.room.vision_potions:
                    self.__game.find_vision_potion()