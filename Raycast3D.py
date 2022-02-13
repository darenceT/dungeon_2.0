import pygame
from GuiSettings import *


class Raycast:

    @staticmethod
    def view_3D(player_x, player_y, player_angle, map, screen):
        """
        Create 3D view of walls, floor and ceiling using raycasting algorithm
        Algorithm credit to https://github.com/maksimKorzh/raycasting-tutorials
        """
        # define left most angle of FOV
        start_angle = player_angle - HALF_FOV

        # loop over casted rays
        for ray in range(CASTED_RAYS):
            # cast ray step by step
            for depth in range(MAX_DEPTH):
                # get ray target coordinates
                target_x = player_x - math.sin(start_angle) * depth
                target_y = player_y + math.cos(start_angle) * depth

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