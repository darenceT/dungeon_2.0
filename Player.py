import pygame

from Settings import *

class Player:
    """
    game_data is instance of DungeonAdventure for "enter_room" method.
    """
    def __init__(self, game_data, screen, world_raw, collision_walls):
        self.cur_room = game_data.maze.ingress
        self.x = int(120 + WIDTH / 9 * 2 * self.cur_room.coords[0])  
        self.y = int(120 + HEIGHT / 9 * 2 * self.cur_room.coords[1])
        self.angle = 0
        self.player_speed = 4
        self.screen = screen
        self.map_visited = set()
        self.show_map = False
        self.game_data = game_data
        self.rooms = game_data.maze.rooms
        self.world_raw = world_raw
        self.side = 50
        self.rect = pygame.Rect(*(self.x, self.y), self.side, self.side)
        # self.collision_sprites = [pygame.Rect(*obj.pos, obj.side, obj.side) for obj in
        #                           self.sprites.list_of_objects if obj.blocked]
        self.collision_list = collision_walls #+ self.collision_sprites
        print(self.rooms)

    @property
    def pos(self):
        return (self.x, self.y)

    def detect_collision(self, dx, dy):
        next_rect = self.rect.copy()
        next_rect.move_ip(dx, dy)
        hit_indexes = next_rect.collidelistall(self.collision_list)

        if len(hit_indexes):
            delta_x, delta_y = 0, 0
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
                dx, dy = 0, 0
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
        next_x = int((self.x - 120) / 160)
        next_y = int((self.y - 120) / 160)
        self.game_data.enter_room(self.rooms[next_y][next_x])
        self.map_visited.add((self.x // MAP_TILE * 3, self.y // MAP_TILE * 3)) # TODO optimize

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

