import pygame
from .Settings import *


class Raycast:
    """
    A basic but effective game-engine to create 3D view of dungeon walls
    by using trigonometric relationship of the distance and angle of walls to the player
    """
    def __init__(self, player, world_coords, textures):
        self.__player = player
        self.__w_coords = world_coords
        self.__textures = textures

    def view_3D(self):
        """
        Raycasting algorithm to display 3D view of walls
        Credit: https://github.com/StanislavPetrovV/Raycasting-3d-game-tutorial/blob/master/part%20%232/ray_casting.py
        :return: wall objects in rendered in "3D" by modifying pixel size in relationship to player's position
        :rtype: pygame rendered image-surface object
        """  
        walls = []     
        ox, oy = self.__player.pos
        def mapping(a, b):
            return (a // TILE) * TILE, (b // TILE) * TILE
        xm, ym = mapping(ox, oy)
        cur_angle = self.__player.angle - HALF_FOV
        for ray in range(NUM_RAYS):
            sin_a = math.sin(cur_angle)
            cos_a = math.cos(cur_angle)
            sin_a = sin_a if sin_a else 0.000001
            cos_a = cos_a if cos_a else 0.000001

            # verticals
            x, dx = (xm + TILE, 1) if cos_a >= 0 else (xm, -1)
            for _ in range(0, WIDTH, TILE):
                depth_v = (x - ox) / cos_a
                yv = oy + depth_v * sin_a
                tile_v = mapping(x + dx, yv)
                if tile_v in self.__w_coords:
                    texture_v = self.__w_coords[tile_v]
                    break
                x += dx * TILE

            # horizontals
            y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)
            for _ in range(0, HEIGHT, TILE):
                depth_h = (y - oy) / sin_a
                xh = ox + depth_h * cos_a
                tile_h = mapping(xh, y + dy)
                if tile_h in self.__w_coords:
                    texture_h = self.__w_coords[tile_h]
                    break
                y += dy * TILE

            # projection
            depth, offset, texture = (depth_v, yv, texture_v) if depth_v < depth_h else (depth_h, xh, texture_h)
            offset = int(offset) % TILE
            depth *= math.cos(self.__player.angle - cur_angle)
            depth = max(depth, 0.00001)
            proj_height = min(int(PROJ_COEFF / depth), 2 * HEIGHT)

            wall_column = self.__textures[texture].subsurface(offset * TEXTURE_SCALE, 0, TEXTURE_SCALE, TEXTURE_HEIGHT)
            wall_column = pygame.transform.scale(wall_column, (SCALE, proj_height))

            wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)

            walls.append((depth, wall_column, wall_pos))
            cur_angle += DELTA_ANGLE
        
        return walls