import pygame

from Grid import Grid
from .Settings import *

class PlayerControls:
    """
    game_data is object of DungeonAdventure to access "enter_room" method.
    room_change boolean to trigger loading of sprites
    """
    def __init__(self, game_data, screen, collision_walls):
        self.angle = 0
        self.player_speed = 4
   
        self.cur_room = game_data.maze.ingress
        self.x = convert_coords_to_pixel(self.cur_room.coords[0])
        self.y = convert_coords_to_pixel(self.cur_room.coords[1])
        self.room_change = True     # set initial to True to for initial 1 time loading of nearby sprites

        self.screen = screen
        self.game_data = game_data
        # self.world_raw = world_raw
        self.rooms_in_sight = set()

        self.map_visited = set()
        self.show_map = False             
        self.side = 50
        self.rect = pygame.Rect(*self.pos, self.side, self.side)
        #self.collision_sprites = [pygame.Rect(*obj.pos, obj.side, obj.side) for obj in
                                  #self.sprites.list_of_objects if obj.blocked]
        self.collision_list = collision_walls #+ self.collision_sprites

    @property
    def pos(self):
        return (self.x, self.y)

    def detect_collision(self, dx, dy):
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
        if PI/4 > self.angle > 7/4*PI: # east
            height = 3
            y -= 1
        elif PI/4 < self.angle < 3/4*PI: # south
            width = 3
            x -= 1
        elif 3/4*PI < self.angle < 5/4*PI: # west
            height = 3
            x -= 1
            y -= 1
        elif 5/4*PI < self.angle < 7/4*PI: # north
            width = 3
            x -= 1
            y -= 1
        # TODO will "else" for 1 direction may run into == errors?

        self.rooms_in_sight = set() # reset
        extent = Grid(width, height, from_grid=self.game_data.maze, from_coords=(x, y))
        add = self.rooms_in_sight.add
        for row in extent.rooms:
            for room in row:
                add(room)

    def keys_control(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            exit()
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
            self.angle -= 0.02
        if keys[pygame.K_RIGHT]:
            self.angle += 0.02

        if keys[pygame.K_TAB]:
            self.show_map = True
        else:
            self.show_map = False

