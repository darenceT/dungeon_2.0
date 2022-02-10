import pygame
import sys
import math

from Maze import Maze

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


class GameScreen:
    """
    Credit https://github.com/maksimKorzh/raycasting-tutorials
    """


    def __init__(self):
        self.entrance_loc = None
        self.exit_loc = None
        self.map = None
        self.screen = None
        self.clock = None
        self.player_x = (SCREEN_WIDTH / 2) / 2
        self.player_y = (SCREEN_WIDTH / 2) / 2
        self.player_angle = math.pi
        self.initialize_screen()   

    def obtain_map(self):
        '''
        TODO pass Maze() into here. For now we create Maze() instance
        set entrance and exit loc
        '''
        maze = Maze()
        self.entrance_loc = maze.ingress.coords
        self.exit_loc = maze.egress.coords
        self.map = maze.str().replace('\n', '').strip()

    def initialize_screen(self):
        pygame.init()
        self.obtain_map()
        # create game window
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Dungeon')
        self.clock = pygame.time.Clock()
        self.game_loop()

    def draw_mini_map(self):
        # loop over map rows
        for row in range(MAP_SIZE):
            # loop over map columns
            for col in range(MAP_SIZE):
                # calculate index
                index = row*25 + col*3       #TODO improve calculation

                # draw map in the game window
                map_color = None
                # whitish = (200, 200, 200)   # pathway color
                if self.map[index] == '+' or self.map[index] == '-' or self.map[index] == '|':
                    map_color = 'black'
                else:
                    map_color = 'brown'

                pygame.draw.rect(
                    self.screen,
                    map_color,
                    (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2)
                )

        # draw player on 2D board
        pygame.draw.circle(self.screen, (255, 0, 0), self.entrance_loc, 8)

        # draw player direction
        pygame.draw.line(self.screen, (0, 255, 0), (self.player_x, self.player_y),
                                           (self.player_x - math.sin(self.player_angle) * 50,
                                            self.player_y + math.cos(self.player_angle) * 50), 3)

        # draw player FOV
        pygame.draw.line(self.screen, (0, 255, 0), (self.player_x, self.player_y),
                                           (self.player_x - math.sin(self.player_angle - HALF_FOV) * 50,
                                            self.player_y + math.cos(self.player_angle - HALF_FOV) * 50), 3)

        pygame.draw.line(self.screen, (0, 255, 0), (self.player_x, self.player_y),
                                           (self.player_x - math.sin(self.player_angle + HALF_FOV) * 50,
                                            self.player_y + math.cos(self.player_angle + HALF_FOV) * 50), 3)

    # raycasting algorithm
    def cast_rays(self):
        # define left most angle of FOV
        start_angle = self.player_angle - HALF_FOV

        # loop over casted rays
        for ray in range(CASTED_RAYS):
            # cast ray step by step
            for depth in range(MAX_DEPTH):
                # get ray target coordinates
                target_x = self.player_x - math.sin(start_angle) * depth
                target_y = self.player_y + math.cos(start_angle) * depth

                # covert target X, Y coordinate to map col, row
                col = int(target_x / TILE_SIZE)
                row = int(target_y / TILE_SIZE)

                # calculate map square index
                #square = row * MAP_SIZE + col
                index = row*25 + col*3

                # ray hits the condition
                if self.map[index] == '+' or self.map[index] == '-' or self.map[index] == '|':
                    # highlight wall that has been hit by a casted ray
                    pygame.draw.rect(self.screen, (0, 255, 0), (col * TILE_SIZE,
                                                        row * TILE_SIZE,
                                                        TILE_SIZE - 2,
                                                        TILE_SIZE - 2))

                    # draw casted ray
                    pygame.draw.line(self.screen, (255, 255, 0), (self.player_x, self.player_y), (target_x, target_y))

                    # wall shading
                    color = 255 / (1 + depth * depth * 0.0001)

                    # fix fish eye effect
                    depth *= math.cos(self.player_angle - start_angle)

                    # calculate wall height
                    wall_height = 21000 / (depth + 0.0001)

                    # fix stuck at the wall
                    if wall_height > SCREEN_HEIGHT: wall_height = SCREEN_HEIGHT 

                    # draw 3D projection (rectangle by rectangle...)
                    pygame.draw.rect(self.screen, (color, color, color), (
                        SCREEN_HEIGHT + ray * SCALE,
                        (SCREEN_HEIGHT / 2) - wall_height / 2,
                         SCALE, wall_height))

                    break

            # increment angle by a single step
            start_angle += STEP_ANGLE

    
    def game_loop(self):

        # moving direction
        forward = True

        while True:
            # escape condition
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

            # covert target X, Y coordinate to map col, row
            col = int(self.player_x / TILE_SIZE)
            row = int(self.player_y / TILE_SIZE)

            # calculate map square index
            #square = row * MAP_SIZE + col
            index = row*25 + col*3

            # player hits the wall (collision detection)
            if self.map[index] == '+' or self.map[index] == '-' or self.map[index] == '|':
                if forward:
                    self.player_x -= -math.sin(self.player_angle) * 5
                    self.player_y -= math.cos(self.player_angle) * 5
                else:
                    self.player_x += -math.sin(self.player_angle) * 5
                    self.player_y += math.cos(self.player_angle) * 5

            # update 2D background
            pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, SCREEN_HEIGHT, SCREEN_HEIGHT))

            # update 3D background
            pygame.draw.rect(self.screen, (100, 100, 100), (480, SCREEN_HEIGHT / 2, SCREEN_HEIGHT, SCREEN_HEIGHT))
            pygame.draw.rect(self.screen, (200, 200, 200), (480, -SCREEN_HEIGHT / 2, SCREEN_HEIGHT, SCREEN_HEIGHT))

            # draw 2D map
            self.draw_mini_map()

            # apply raycasting
            self.cast_rays()

            # get user input
            keys = pygame.key.get_pressed()

            # handle user input
            if keys[pygame.K_LEFT]: self.player_angle -= 0.1
            if keys[pygame.K_RIGHT]: self.player_angle += 0.1
            if keys[pygame.K_UP]:
                forward = True
                self.player_x += -math.sin(self.player_angle) * 5
                self.player_y += math.cos(self.player_angle) * 5
            if keys[pygame.K_DOWN]:
                forward = False
                self.player_x -= -math.sin(self.player_angle) * 5
                self.player_y -= math.cos(self.player_angle) * 5

            # set FPS
            self.clock.tick(30)

            # display FPS
            fps = str(int(self.clock.get_fps()))

            # pick up the font
            font = pygame.font.SysFont('Monospace Regular', 30)

            # create font surface
            fps_surface = font.render(fps, False, (255, 255, 255))

            # print FPS to screen
            self.screen.blit(fps_surface, (480, 0))

            # update display
            pygame.display.flip()


if __name__ == '__main__':
    GameScreen()























