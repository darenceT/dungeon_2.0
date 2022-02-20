import pygame
from .Settings import *


class Raycast:

    @staticmethod
    def view_3D_EXPERIEMENT(screen, player_pos, player_angle, world_coords, textures):
        """
        Raycasting algorithm to display 3D view of walls, ceiling, floor
        Credit: https://github.com/StanislavPetrovV/Raycasting-3d-game-tutorial/blob/master/part%20%232/ray_casting.py
        """
        ox, oy = player_pos
        def mapping(a, b):
            return (a // TILE) * TILE, (b // TILE) * TILE
        start_x, start_y = mapping(ox, oy)
        cur_angle = player_angle - HALF_FOV
        texture_v = 'wall'; texture_h = 'wall'
        for ray in range(NUM_RAYS):
            sin_a = math.sin(cur_angle)
            cos_a = math.cos(cur_angle)
            sin_a = sin_a if sin_a else 0.000001
            cos_a = cos_a if cos_a else 0.000001

            # verticals
            target_x, direction_x = (start_x + TILE, 1) if sin_a >= 0 else (start_x, -1)
            # x, dx = (xm + TILE, 1) if cos_a >= 0 else (xm, -1)
            for _ in range(0, WIDTH, TILE):
                depth_v = (target_x - ox) / cos_a
                target_y = oy + depth_v * sin_a
                # yv = oy + depth_v * sin_a
                tile_v = mapping(target_x + direction_x, target_y)
                if tile_v in world_coords:
                    texture_v = world_coords[tile_v] if world_coords[tile_v] != 'wall' else 'door_openv'
                    if world_coords[tile_v] == 'door_closed':
                        target_x += direction_x * 32
                        depth_v = (target_x - ox) / cos_a
                        target_y = oy + depth_v * sin_a       
                    break
                target_x += direction_x * TILE

            # horizontals
            target_y, direction_y = (start_y + TILE, 1) if sin_a >= 0 else (start_y, -1)
            for _ in range(0, HEIGHT, TILE):
                depth_h = (target_y - oy) / sin_a
                target_x = ox + depth_h * cos_a
                tile_h = mapping(target_x, target_y + direction_x)
                if tile_h in world_coords:
                    texture_h = world_coords[tile_h] if world_coords[tile_h] != 'wall' else 'door_openh'
                    if world_coords[tile_h] == 'door_closed':
                        target_y += direction_y * 32
                        depth_h = (target_y - oy) / sin_a
                        target_x = ox + depth_h * cos_a
                    break
                target_y += direction_y * TILE

            # projection
            # texture_offset = target_y if depth_v < depth_h else target_x
            # texture = texture_v if depth_v < depth_h else texture_h
            # depth = depth_v if depth_v < depth_h else depth_h
            # depth *= math.cos(player_angle - cur_angle)
            # wall_height = TILE * 300 / (depth + 0.0001)
            # if wall_height > 50000: wall_height = 50000
            # wall_block = textures[texture].subsurface((texture_offset - int(texture_offset % TILE) * TILE), 0, 1, 64)
            # wall_block = pygame.transform.scale(wall_block, (1, abs(int(wall_height))))

            if depth_v < depth_h:
                texture_offset = target_y
                texture = texture_v
                depth = depth_v
            else:
                texture_offset = target_x
                texture = texture_h
                depth = depth_h
            texture_offset -= int(texture_offset % TILE)
            depth *= math.cos(player_angle - cur_angle)
            wall_height = min(int(PROJ_COEFF / depth), 2 * HEIGHT)
            
            wall_block = textures[texture].subsurface(texture_offset * TEXTURE_SCALE, 0, TEXTURE_SCALE, TEXTURE_HEIGHT)
            wall_block = pygame.transform.scale(wall_block, (SCALE, wall_height))
            # depth, offset, texture = (depth_v, target_y, texture_v) if depth_v < depth_h else (depth_h, target_x, texture_h)
            # offset = int(offset) % TILE
            # depth *= math.cos(player_angle - cur_angle)
            # depth = max(depth, 0.00001)
            # wall_height = min(int(PROJ_COEFF / depth), 2 * HEIGHT)

            # wall_block = textures[texture].subsurface(offset * TEXTURE_SCALE, 0, TEXTURE_SCALE, TEXTURE_HEIGHT)
            # wall_block = pygame.transform.scale(wall_block, (SCALE, wall_height))
            screen.blit(wall_block, (ray * SCALE, HALF_HEIGHT - wall_height // 2))

            cur_angle += DELTA_ANGLE

    @staticmethod
    def view_3D(player, world_coords, textures):
        """
        Raycasting algorithm to display 3D view of walls, ceiling, floor
        Credit: https://github.com/StanislavPetrovV/Raycasting-3d-game-tutorial/blob/master/part%20%232/ray_casting.py
        """
        walls = []        
        ox, oy = player.pos
        def mapping(a, b):
            return (a // TILE) * TILE, (b // TILE) * TILE
        xm, ym = mapping(ox, oy)
        cur_angle = player.angle - HALF_FOV
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
                if tile_v in world_coords:
                    texture_v = world_coords[tile_v]
                    break
                x += dx * TILE

            # horizontals
            y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)
            for _ in range(0, HEIGHT, TILE):
                depth_h = (y - oy) / sin_a
                xh = ox + depth_h * cos_a
                tile_h = mapping(xh, y + dy)
                if tile_h in world_coords:
                    texture_h = world_coords[tile_h]
                    break
                y += dy * TILE

            # projection
            depth, offset, texture = (depth_v, yv, texture_v) if depth_v < depth_h else (depth_h, xh, texture_h)
            offset = int(offset) % TILE
            depth *= math.cos(player.angle - cur_angle)
            depth = max(depth, 0.00001)
            proj_height = min(int(PROJ_COEFF / depth), 2 * HEIGHT)

            wall_column = textures[texture].subsurface(offset * TEXTURE_SCALE, 0, TEXTURE_SCALE, TEXTURE_HEIGHT)
            wall_column = pygame.transform.scale(wall_column, (SCALE, proj_height))
            # screen.blit(wall_column, (ray * SCALE, HALF_HEIGHT - proj_height // 2))

            wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)

            walls.append((depth, wall_column, wall_pos))
            cur_angle += DELTA_ANGLE
        
        return walls