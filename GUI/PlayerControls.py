import pygame
import math
from Grid import Grid
from .Arena import Arena
from .Settings import PI, DOUBLE_PI, MAP_TILE
from .Utility import convert_coords_to_pixel


class PlayerControls:
    """
    Contains player keyboard input in addition to controller code.
    game_data is object of DungeonAdventure to access "enter_room" method.
    room_change boolean to trigger loading of sprites
    """
    def __init__(self, screen, sound, game_data, memo, collision_walls):
        self.angle = 0
        self.player_speed = 3
        self.__attacking = False
        self.__special_skill = False
   
        self.cur_room = game_data.maze.ingress
        self.x = convert_coords_to_pixel(self.cur_room.coords[0])
        self.y = convert_coords_to_pixel(self.cur_room.coords[1])
        self.room_change = True     # set initial to True to for initial 1 time loading of nearby sprites

        self.screen = screen
        self.sound = sound
        self.__pause_on = False
        self.game_data = game_data
        self.memo = memo
        self.arena = Arena(sound, self, game_data.hero)

        self.rooms_in_sight = set()
        self.map_visited = set()
        self.show_map = False             
        self.side = 50
        self.rect = pygame.Rect(*self.pos, self.side, self.side)
        #self.collision_sprites = [pygame.Rect(*obj.pos, obj.side, obj.side) for obj in
                                  #self.sprites.list_of_objects if obj.blocked]
        self.collision_list = collision_walls #+ self.collision_sprites
        self.__new_pillar = None
        self.__win_game = False

    @property
    def pos(self):
        return (self.x, self.y)

    @property
    def pause_on(self):
        return self.__pause_on
    
    @pause_on.setter
    def pause_on(self, change=True):
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
    def special_skill(self):
        return self.__special_skill

    @special_skill.setter
    def special_skill(self, change=False):
        if isinstance(change, bool):
            if not change:
                self.__special_skill = False
            else:
                raise ValueError('True should not be accessed outside of PlayerControls')
        else:
            raise TypeError('Only boolean accepted for pause_on')
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

    # @win_game.setter
    # def win_game(self, change=False):
    #     if isinstance(change, bool):
    #         if change:
    #             self.__win_game = change
    #         else:
    #             raise ValueError('False should not be accessed outside of PlayerControls')
    #     else:
    #         raise TypeError('Only boolean accepted for pause_on')

    def detect_collision(self, dx, dy):
        """
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
        self.keys_control()
        # self.mouse_control()
        self.rect.center = self.x, self.y
        self.angle %= DOUBLE_PI

        # update room location
        next_x = int((self.x - 120) / 160)
        next_y = int((self.y - 120) / 160)

        if self.cur_room.coords != (next_x, next_y):
            self.cur_room = self.game_data.maze.rooms[next_y][next_x]

            # exit logic from sprites.object_locate() to detect hero near door
            if self.cur_room.is_exit:
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
            self.room_change = True
            self.get_rooms_in_sight()
        else:
            self.room_change = False
        self.map_visited.add((self.x // MAP_TILE * 3, self.y // MAP_TILE * 3)) # TODO optimize
        

    def get_rooms_in_sight(self):
        """
        Determines direction player is facing using player angle,
        then obtain coordinates of the 6 rooms (including current room)
        allowing for use in loading sprites in these rooms
        """
        width = height = 2
        x, y = self.cur_room.coords
        if PI/4 >= self.angle >= 7/4*PI: # east
            height = 3
            y -= 1
        elif PI/4 < self.angle <= 3/4*PI: # south
            width = 3
            x -= 1
        elif 3/4*PI < self.angle <= 5/4*PI: # west
            height = 3
            x -= 1
            y -= 1
        else:  # 5/4*PI < self.angle < 7/4*PI: # north
            width = 3
            x -= 1
            y -= 1
        
        self.rooms_in_sight = set() # reset
        extent = Grid(width, height, from_grid=self.game_data.maze, from_coords=(x, y))
        add = self.rooms_in_sight.add
        for row in extent.rooms:
            for room in row:
                add(room)

    def keys_control(self):
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
                        self.sound.health_potion()
                    self.game_data.hero.use_healing_potion()
                elif event.key == pygame.K_v:
                    if self.game_data.hero.vision_potions:
                        self.memo.new_message('Vision potion used, check your map!')
                        self.sound.vision_potion()
                    self.game_data.hero.use_vision_potion()
                elif event.key == pygame.K_r:
                    special = self.game_data.hero.special_skill()
                    if special is not None:
                        self.__special_skill = True
                        self.memo.new_message(special)
                        self.sound.special_heal()
                elif event.key == pygame.K_SPACE:
                    self.__pause_on = True

        # for continuous key input
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()
            
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dx = self.player_speed * cos_a
            dy = self.player_speed * sin_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dx = -self.player_speed * cos_a
            dy = -self.player_speed * sin_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_a]:
            dx = self.player_speed * sin_a
            dy = -self.player_speed * cos_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_d]:
            dx = -self.player_speed * sin_a
            dy = self.player_speed * cos_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_LEFT]:
            self.angle -= 0.04
        if keys[pygame.K_RIGHT]:
            self.angle += 0.04

        self.__attacking = True if keys[pygame.K_e] else False
        self.show_map = True if keys[pygame.K_TAB] else False

