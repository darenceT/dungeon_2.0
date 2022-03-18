import pygame
import math
from .Arena import Arena
from .Settings import DOUBLE_PI, PLAYER_SPEED
from .Utility import convert_pixel_to_coords, convert_coords_to_pixel, direction_of_vision


class PlayerControls:
    """
    Contains player keyboard input in addition to controller code.
    game_data is object of DungeonAdventure to access "enter_room" method.
    room_change boolean to trigger loading of sprites
    """
    def __init__(self, sound, game_data, memo, collision_walls):
        self.angle = 0
        self.__direction = 'east'       
        self.cur_room = game_data.room
        self.x, self.y = convert_coords_to_pixel(self.cur_room.coords)
        self.__attacking = False
        self.__fight_alone = True
        self.__special_skill_execute = False
        self.__special_skill_animate = False
        self.__vision_pot_used = False 
        
        self.__room_change = True     # set initial to True to for initial 1 time loading of nearby sprites
        self.__ready_for_new_sprites = True
        self.__sound = sound
        self.__pause_on = False
        self.game_data = game_data
        self.memo = memo
        self.__arena = Arena(self, game_data.hero, memo)

        self.__rooms_in_sight = tuple()
        self.__rooms_visited = game_data.rooms_visited
        self.map_visited_old = set()
        self.show_map = False             
        self.side = 50
        self.rect = pygame.Rect(*self.pos, self.side, self.side)
        #TODO below to make monsters impassible
        #self.collision_sprites = [pygame.Rect(*obj.pos, obj.side, obj.side) for obj in
                                  #self.sprites.list_of_objects if obj.blocked]
        self.collision_list = collision_walls #+ self.collision_sprites
        self.__new_pillar = None
        self.__win_game = False

    @property
    def pos(self):
        return (self.x, self.y)

    @property
    def rooms_visited(self):
        return self.__rooms_visited

    @property
    def rooms_in_sight(self):
        return self.__rooms_in_sight

    @property
    def ready_for_new_sprites(self):
        return self.__ready_for_new_sprites

    @property
    def pause_on(self):
        return self.__pause_on
    
    @pause_on.setter
    def pause_on(self, change=True):
        """
        Setter to change back to false after pause-menu accessed via Main
        """
        if isinstance(change, bool):
            if not change:
                self.__pause_on = False
            else:
                raise ValueError('True should not be accessed outside of PlayerControls')
        else:
            raise TypeError('Only boolean accepted for pause_on')

    @property
    def attacking(self):
        return self.__attacking

    @property
    def fight_alone(self):
        return self.__fight_alone

    @fight_alone.setter
    def fight_alone(self, change):
        """
        Allow detection of nearby monsters to let you know if you're alone,
        allowing additional use of arena for special skill when alone
        """
        if isinstance(change, bool):
            if change:
                self.__fight_alone = True
            else:
                self.__fight_alone = False
        else:
            raise TypeError('Only boolean accepted for fight_alone')

    @property
    def special_skill_execute(self):
        return self.__special_skill_execute

    @special_skill_execute.setter
    def special_skill_execute(self, change=False):
        """
        Setter to allow turning off special skill effects to allow 
        looping only once each time, accessed in Arena
        :return: None
        """
        if isinstance(change, bool):
            if not change:
                self.__special_skill_execute = False
            else:
                raise ValueError('True should not be accessed outside of PlayerControls')
        else:
            raise TypeError('Only boolean accepted for special_skill_execute')

    @property
    def special_skill_animate(self):
        return self.__special_skill_animate

    @special_skill_animate.setter
    def special_skill_animate(self, change=False):
        """
        Setter to allow turning off special skill animation to allow 
        looping only once each time, accessed in Drawing
        :return: None
        """
        if isinstance(change, bool):
            if not change:
                self.__special_skill_animate = False
            else:
                raise ValueError('True should not be accessed outside of PlayerControls')
        else:
            raise TypeError('Only boolean accepted for special_skill_animate')

    @property
    def vision_pot_used(self):
        return self.__vision_pot_used

    @vision_pot_used.setter
    def vision_pot_used(self, change=False):
        """
        Setter for vision potion used, to turn off
        :return: None
        """
        if isinstance(change, bool):
            if not change:
                self.__vision_pot_used = False
            else:
                raise ValueError('True should not be accessed outside of PlayerControls')
        else:
            raise TypeError('Only boolean accepted for vision_pot_used')
            
    @property
    def arena(self):
        return self.__arena

    @property
    def new_pillar(self):
        return self.__new_pillar

    @new_pillar.setter
    def new_pillar(self, pillar=None):
        # if isinstance(pillar, Pillar):
        self.__new_pillar = pillar
        # else:
        #     raise TypeError('Only Pillar object accepted outside PlayerControls')

    @property
    def win_game(self):
        return self.__win_game

    def detect_collision(self, dx, dy):
        """
        Creates impassible locations AKA do not walk through walls
        TODO Can be applied to Sprites in future implementation
        :param dx: change in player's movement horizontally
        :param type: float
        :param dy: change in player's movement vertically
        :param type: float
        :return: None
        Credit: https://github.com/StanislavPetrovV/Raycasting-3d-game-tutorial/blob/master/part%20%232/ray_casting.py
        """
        next_rect = self.rect.copy()
        next_rect.move_ip(dx, dy)
        hit_indexes = next_rect.collidelistall(self.collision_list)

        if len(hit_indexes):
            delta_x = delta_y = 0
            for hit_index in hit_indexes:
                hit_rect = self.collision_list[hit_index]
                if dx > 0:
                    delta_x += next_rect.right - hit_rect.left
                else:
                    delta_x += hit_rect.right - next_rect.left
                if dy > 0:
                    delta_y += next_rect.bottom - hit_rect.top
                else:
                    delta_y += hit_rect.bottom - next_rect.top

            if abs(delta_x - delta_y) < 10:
                dx = dy = 0
            elif delta_x > delta_y:
                dy = 0
            elif delta_y > delta_x:
                dx = 0
        self.x += dx
        self.y += dy

    def movement(self):
        """
        Controller code that triggers game events based off player's movement
        and position in maze, and obtain user's keyboard input
        :return: None
        """
        self.__keys_control()
        self.rect.center = self.x, self.y
        self.angle %= DOUBLE_PI

        # update room location
        next_x, next_y = convert_pixel_to_coords((self.x, self.y))
        if self.cur_room.coords != (next_x, next_y):
            self.cur_room = self.game_data.maze.rooms[next_y][next_x]
            
            # win logic 
            if self.cur_room.is_exit and self.cur_room.occupants == []:
                pillars = 4-len(self.game_data.hero.pillars)
                if pillars == 0:
                    self.__win_game = True
                    return
                else:
                    if pillars == 0: 
                        raise ValueError('Should win game instead of display 0 pillars remaining') 
                    else:
                        plur = 's!' if pillars > 1 else '!'
                        self.memo.new_message(f'You need to find {4-len(self.game_data.hero.pillars)} more pillar{plur}')
            elif self.__new_pillar and self.cur_room is not None:
                self.memo.new_message(f'You found pillar {self.__new_pillar}!')
                self.__new_pillar = None

            # move hero to new room, refresh nearby sprites
            self.game_data.enter_room(self.cur_room)
            self.__room_change = True
        else:
            self.__room_change = False
        self.get_rooms_in_sight()    
        self.__rooms_visited.add((next_x, next_y))

    def get_rooms_in_sight(self):
        """
        Determines direction player is facing using player angle, then 
        obtain coordinates of anticipated next room in addition to current room.
        List of these rooms will be used to loading sprites in field of vision.
        """
        direction = direction_of_vision(self.angle)
        if direction != self.__direction or self.__room_change:
            self.__direction = direction
            x, y = self.cur_room.coords
            next_x, next_y = x, y
            if direction == 'north':
                next_y -= 1
            elif direction == 'south':
                next_y += 1
            elif direction == 'west':
                next_x -= 1
            else:            # east
                next_x += 1
            
            cur_room = self.game_data.maze.rooms[y][x]
            max_x = self.game_data.maze.width
            max_y = self.game_data.maze.height
            if -1 < next_x < max_x and -1 < next_y < max_y:
                next_room = self.game_data.maze.rooms[next_y][next_x]
                self.__rooms_in_sight = (cur_room, next_room)
            else:
                self.__rooms_in_sight = (cur_room,)
            
            self.__ready_for_new_sprites = True
        else:
            self.__ready_for_new_sprites = False

    def __keys_control(self):
        """
        User input key controls, keyboard only because it's more fun!
        First half for non-continuous input and 2nd half for continuous key-down input
        :return: None
        """
        # for non-continuous key input
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    if self.game_data.hero.healing_potions:
                        self.memo.new_message('You used a healing potion!')
                        self.__sound.health_potion()
                    self.game_data.hero.use_healing_potion()
                elif event.key == pygame.K_v:
                    if self.game_data.hero.vision_potions:
                        self.__vision_pot_used = True
                        self.memo.new_message('Vision potion used, check your map!')
                        self.__sound.vision_potion()
                    self.game_data.hero.use_vision_potion()
                elif event.key == pygame.K_r:
                    if self.game_data.hero.can_use_special():
                        self.__special_skill_animate = True
                        self.__special_skill_execute = True
                        if self.__fight_alone:
                            self.__arena.fight()
                elif event.key == pygame.K_SPACE:
                    self.__pause_on = True
                elif event.key == pygame.K_TAB:
                    self.show_map = True if not self.show_map else False

        # for continuous key input
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()
            
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dx = PLAYER_SPEED * cos_a
            dy = PLAYER_SPEED * sin_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dx = -PLAYER_SPEED * cos_a
            dy = -PLAYER_SPEED * sin_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_a]:
            dx = PLAYER_SPEED * sin_a
            dy = -PLAYER_SPEED * cos_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_d]:
            dx = -PLAYER_SPEED * sin_a
            dy = PLAYER_SPEED * cos_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_LEFT]:
            self.angle -= 0.04
        if keys[pygame.K_RIGHT]:
            self.angle += 0.04

        self.__attacking = True if keys[pygame.K_e] else False

