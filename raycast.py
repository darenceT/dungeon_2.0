import pygame
import sys
import math

from Maze import Maze

"""
# map                                       # DELETE
# MAP_default = (
    '########'
    '# #    #'
    '# #  ###'
    '#      #'
    '#      #'
    '#  ##  #'
    '#   #  #'
    '########'
#)"""

class GameScreen:
    # global constants
    SCREEN_HEIGHT = 480
    SCREEN_WIDTH = SCREEN_HEIGHT * 2
    MAP_SIZE = 4 * 2 + 1        # (input here) * 2 + 1
    TILE_SIZE = int((SCREEN_WIDTH / 2) / MAP_SIZE)
    MAX_DEPTH = int(MAP_SIZE * TILE_SIZE)
    FOV = math.pi / 3
    HALF_FOV = FOV / 2
    CASTED_RAYS = 120
    STEP_ANGLE = FOV / CASTED_RAYS
    SCALE = (SCREEN_WIDTH / 2) / CASTED_RAYS

    # global variables
    player_x = (SCREEN_WIDTH / 2) / 2
    player_y = (SCREEN_WIDTH / 2) / 2
    player_angle = math.pi
    
    def __init__(self):
        self.entrance_loc = None
        self.exit_loc = None
        self.initialize_screen()

    def obtain_map(self):

        map1 = (
        '+-----+-----+-----+-----+'
        '|     |     =     | O   |'
        '+--H--+-----+--H--+--H--+'
        '|     =     =     =     |'
        '+-----+-----+-----+--H--+'
        '|     =     |     =     |'
        '+-----+--H--+-----+--H--+'
        '| i   =     =     =     |'
        '+-----+-----+-----+-----+'
        )

        map2 = ("""
        +-----+-----+-----+-----+
        |     |     =     | O   |
        +--H--+-----+--H--+--H--+
        |     =     =     =     |
        +-----+-----+-----+--H--+
        |     =     |     =     |
        +-----+--H--+-----+--H--+
        | i   =     =     =     |
        +-----+-----+-----+-----+
        """)
        created_dungeon = Maze(map_str=map2)
        self.entrance_loc = created_dungeon.ingress.coords
        self.exit_loc = created_dungeon.egress.coords

    def initialize_screen(self):
        pygame.init()
        
        # create game window
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Dungeon')
        clock = pygame.time.Clock()

# draw map
    def draw_map():
        """
        Credit https://github.com/maksimKorzh/raycasting-tutorials
        """
        # loop over map rows
        for row in range(MAP_SIZE):
            # loop over map columns
            for col in range(MAP_SIZE):
                # calculate index
                index = row*25 + col*3       #TODO improve calculation

                # draw map in the game window
                map_color = None
                # whitish = (200, 200, 200)   # pathway color
                if MAP[index] == '+' or MAP[index] == '-' or MAP[index] == '|':
                    map_color = 'black'
                else:
                    map_color = 'brown'

                pygame.draw.rect(
                    screen,
                    map_color,
                    (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2)
                )

        # draw player on 2D board
        pygame.draw.circle(screen, (255, 0, 0), (int(player_x), int(player_y)), 8)

        # draw player direction
        pygame.draw.line(screen, (0, 255, 0), (player_x, player_y),
                                           (player_x - math.sin(player_angle) * 50,
                                            player_y + math.cos(player_angle) * 50), 3)

        # draw player FOV
        pygame.draw.line(screen, (0, 255, 0), (player_x, player_y),
                                           (player_x - math.sin(player_angle - HALF_FOV) * 50,
                                            player_y + math.cos(player_angle - HALF_FOV) * 50), 3)

        pygame.draw.line(screen, (0, 255, 0), (player_x, player_y),
                                           (player_x - math.sin(player_angle + HALF_FOV) * 50,
                                            player_y + math.cos(player_angle + HALF_FOV) * 50), 3)

    # raycasting algorithm
    def cast_rays():
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
                if MAP[index] == '+' or MAP[index] == '-' or MAP[index] == '|':
                    # highlight wall that has been hit by a casted ray
                    pygame.draw.rect(screen, (0, 255, 0), (col * TILE_SIZE,
                                                        row * TILE_SIZE,
                                                        TILE_SIZE - 2,
                                                        TILE_SIZE - 2))

                    # draw casted ray
                    pygame.draw.line(screen, (255, 255, 0), (player_x, player_y), (target_x, target_y))

                    # wall shading
                    color = 255 / (1 + depth * depth * 0.0001)

                    # fix fish eye effect
                    depth *= math.cos(player_angle - start_angle)

                    # calculate wall height
                    wall_height = 21000 / (depth + 0.0001)

                    # fix stuck at the wall
                    if wall_height > SCREEN_HEIGHT: wall_height = SCREEN_HEIGHT 

                    # draw 3D projection (rectangle by rectangle...)
                    pygame.draw.rect(screen, (color, color, color), (
                        SCREEN_HEIGHT + ray * SCALE,
                        (SCREEN_HEIGHT / 2) - wall_height / 2,
                         SCALE, wall_height))

                    break

            # increment angle by a single step
            start_angle += STEP_ANGLE

    # moving direction
    forward = True

    
    def game_loop(self):
        # game loop
        while True:
            # escape condition
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

            # covert target X, Y coordinate to map col, row
            col = int(player_x / TILE_SIZE)
            row = int(player_y / TILE_SIZE)

            # calculate map square index
            #square = row * MAP_SIZE + col
            index = row*25 + col*3

            # player hits the wall (collision detection)
            if MAP[index] == '+' or MAP[index] == '-' or MAP[index] == '|':
                if forward:
                    player_x -= -math.sin(player_angle) * 5
                    player_y -= math.cos(player_angle) * 5
                else:
                    player_x += -math.sin(player_angle) * 5
                    player_y += math.cos(player_angle) * 5

            # update 2D background
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, SCREEN_HEIGHT, SCREEN_HEIGHT))

            # update 3D background
            pygame.draw.rect(screen, (100, 100, 100), (480, SCREEN_HEIGHT / 2, SCREEN_HEIGHT, SCREEN_HEIGHT))
            pygame.draw.rect(screen, (200, 200, 200), (480, -SCREEN_HEIGHT / 2, SCREEN_HEIGHT, SCREEN_HEIGHT))

            # draw 2D map
            draw_map()

            # apply raycasting
            cast_rays()

            # get user input
            keys = pygame.key.get_pressed()

            # handle user input
            if keys[pygame.K_LEFT]: player_angle -= 0.1
            if keys[pygame.K_RIGHT]: player_angle += 0.1
            if keys[pygame.K_UP]:
                forward = True
                player_x += -math.sin(player_angle) * 5
                player_y += math.cos(player_angle) * 5
            if keys[pygame.K_DOWN]:
                forward = False
                player_x -= -math.sin(player_angle) * 5
                player_y -= math.cos(player_angle) * 5

            # set FPS
            clock.tick(30)

            # display FPS
            fps = str(int(clock.get_fps()))

            # pick up the font
            font = pygame.font.SysFont('Monospace Regular', 30)

            # create font surface
            fps_surface = font.render(fps, False, (255, 255, 255))

            # print FPS to screen
            screen.blit(fps_surface, (480, 0))

            # update display
            pygame.display.flip()


if __name__ == '__main__':
    GameScreen()























