import pygame
from GuiSettings import *


class Raycast:

    @staticmethod
    def view_3D(screen, player_pos, player_angle, map):
        """
        Raycasting algorithm to display 3D view of walls, ceiling, floor
        Credit: https://github.com/StanislavPetrovV/Raycasting-3d-game-tutorial/blob/master/part%20%232/ray_casting.py
        """
        ox, oy = player_pos

        def mapping(a, b):
            return (a // TILE_SIZE) * TILE_SIZE, (b // TILE_SIZE) * TILE_SIZE
        xm, ym = mapping(ox, oy)
        cur_angle = player_angle - HALF_FOV
        for ray in range(CASTED_RAYS):
            sin_a = math.sin(cur_angle)
            cos_a = math.cos(cur_angle)
            sin_a = sin_a if sin_a else 0.000001
            cos_a = cos_a if cos_a else 0.000001

            # verticals
            x, dx = (xm + TILE_SIZE, 1) if cos_a >= 0 else (xm, -1)
            for i in range(0, SCREEN_WIDTH, TILE_SIZE):
                depth_v = (x - ox) / cos_a
                y = oy + depth_v * sin_a
                if mapping((x + dx), y) in map:     #TODO map likely wrong variable
                    break
                x += dx * TILE_SIZE

            # horizontals
            y, dy = (ym + TILE_SIZE, 1) if sin_a >= 0 else (ym, -1)
            for i in range(0, SCREEN_HEIGHT, TILE_SIZE):
                depth_h = (y - oy) / sin_a
                x = ox + depth_h * cos_a
                if mapping(x, y + dy) in map:
                    break
                y += dy * TILE_SIZE

            # projection
            depth = depth_v if depth_v < depth_h else depth_h
            depth *= math.cos(player_angle - cur_angle)
            proj_height = PROJ_COEFF / depth
            c = 255 / (1 + depth * depth * 0.00002)
            color = (c, c // 2, c // 3)
            pygame.draw.rect(screen, color, (ray * SCALE, SCREEN_HEIGHT/2 - proj_height // 2, SCALE, proj_height))
            cur_angle += STEP_ANGLE


    @staticmethod
    def view_3D(screen, player_pos, player_angle, map):
        """
        Create 3D view of walls, floor and ceiling using raycasting algorithm
        Algorithm credit to https://github.com/maksimKorzh/raycasting-tutorials
        """
        p_x, p_y = player_pos
        # define left most angle of FOV
        start_angle = player_angle - HALF_FOV

        # loop over casted rays
        for ray in range(CASTED_RAYS):
            # cast ray step by step
            for depth in range(MAX_DEPTH):
                # get ray target coordinates
                target_x = p_x - math.sin(start_angle) * depth
                target_y = p_y + math.cos(start_angle) * depth

                # covert target X, Y coordinate to map col, row
                col = int(target_x / TILE_SIZE)
                row = int(target_y / TILE_SIZE)

                # calculate map square index
                #square = row * MAP_SIZE + col
                index = row*25 + col*3

                # ray hits the condition
                if map[index] == '+' or map[index] == '-' or map[index] == '|':

                    # wall shading
                    color = 255 / (1 + depth * depth * 0.0001)

                    # fix fish eye effect
                    depth *= math.cos(player_angle - start_angle)

                    # calculate wall height
                    wall_height = 21000 / (depth + 0.0001)

                    # fix stuck at the wall
                    if wall_height > SCREEN_HEIGHT: wall_height = SCREEN_HEIGHT 

                    # draw 3D projection (rectangle by rectangle...)
                    pygame.draw.rect(screen, (color, color, color), (ray * SCALE, 
                        (SCREEN_HEIGHT / 2) - wall_height / 2, SCALE, wall_height))

                    break

            # increment angle by a single step
            start_angle += STEP_ANGLE