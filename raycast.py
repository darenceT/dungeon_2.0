import pygame
import sys
import math

from Maze import Maze

SCREEN_HEIGHT = 720
SCREEN_WIDTH = 720
MAP_SIZE = 4 * 2 + 1        # (input here, 4 for 4x4 rooms) * 2 + 1

TILE_SIZE = int((SCREEN_WIDTH) / MAP_SIZE)
MAX_DEPTH = int(MAP_SIZE * TILE_SIZE)
FOV = math.pi / 3
HALF_FOV = FOV / 2
CASTED_RAYS = 120
STEP_ANGLE = FOV / CASTED_RAYS
SCALE = (SCREEN_WIDTH) / CASTED_RAYS


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
        self.player_x = None
        self.player_y = None 
        self.player_angle = math.pi
        self.initialize_screen()   

    def obtain_map_data(self):
        '''
        TODO pass Maze() into here. For now we create Maze() instance
        set entrance and exit loc
        '''
        maze = Maze()
        self.entrance_loc = maze.ingress.coords
        self.exit_loc = maze.egress.coords
        self.map = maze.str().replace('\n', '').strip()
        self.player_x = 120         # Constant value since entrance always starts at column 0
        self.player_y = int(SCREEN_WIDTH / 9 * 2 * self.entrance_loc[1]) + 120  # row location of entrance

    def initialize_screen(self):
        pygame.init()
        self.obtain_map_data()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Dungeon 2.0')
        self.clock = pygame.time.Clock()
        self.game_loop()

    def mini_map(self):
        """
        Creates map with player's position and the direction player is facing on map
        """
        for row in range(MAP_SIZE):
            for col in range(MAP_SIZE):
                index = row*25 + col*3       #TODO improve calculation
                map_color = None
                if self.map[index] == '+' or self.map[index] == '-' or self.map[index] == '|':
                    map_color = 'black'
                else:
                    map_color = 'orange'

                square = TILE_SIZE / 4
                pygame.draw.rect(self.screen, map_color,
                    (col * square, row * square, square, square))

        # draw player
        map_x = self.player_x/4
        map_y = self.player_y/4
        pygame.draw.circle(self.screen, 'green', (map_x, map_y), 4)

        # draw player field of vision
        pygame.draw.line(self.screen, (0, 255, 0), (map_x, map_y),
                                           (map_x - math.sin(self.player_angle - HALF_FOV) * 10,
                                            map_y + math.cos(self.player_angle - HALF_FOV) * 10), 2)
        pygame.draw.line(self.screen, (0, 255, 0), (map_x, map_y),
                                           (map_x - math.sin(self.player_angle + HALF_FOV) * 10,
                                            map_y + math.cos(self.player_angle + HALF_FOV) * 10), 2)

    def view_3D(self):
        """
        Create 3D view of walls, floor and ceiling using raycasting algorithm
        Again, credit to https://github.com/maksimKorzh/raycasting-tutorials
        """
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

                    # wall shading
                    color = 255 / (1 + depth * depth * 0.0001)

                    # fix fish eye effect
                    depth *= math.cos(self.player_angle - start_angle)

                    # calculate wall height
                    wall_height = 21000 / (depth + 0.0001)

                    # fix stuck at the wall
                    if wall_height > SCREEN_HEIGHT: wall_height = SCREEN_HEIGHT 

                    # draw 3D projection (rectangle by rectangle...)
                    pygame.draw.rect(self.screen, (color, color, color), (ray * SCALE, 
                        (SCREEN_HEIGHT / 2) - wall_height / 2, SCALE, wall_height))

                    break

            # increment angle by a single step
            start_angle += STEP_ANGLE

    
    def game_loop(self):
        # moving direction
        forward = True

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN \
                    and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit(0)

            # covert target X, Y coordinate to map col, row
            col = int(self.player_x / TILE_SIZE)
            row = int(self.player_y / TILE_SIZE)

            # calculate map square index
            index = row*25 + col*3

            # player hits the wall (collision detection)
            if self.map[index] == '+' or self.map[index] == '-' or self.map[index] == '|':
                if forward:
                    self.player_x -= -math.sin(self.player_angle) * 5
                    self.player_y -= math.cos(self.player_angle) * 5
                else:
                    self.player_x += -math.sin(self.player_angle) * 5
                    self.player_y += math.cos(self.player_angle) * 5

            # update 3D background
            pygame.draw.rect(self.screen, (100, 100, 100), (0, SCREEN_HEIGHT / 2, SCREEN_HEIGHT, SCREEN_HEIGHT))
            pygame.draw.rect(self.screen, (200, 200, 200), (0, -SCREEN_HEIGHT / 2, SCREEN_HEIGHT, SCREEN_HEIGHT))

            # raycasting for 3D view
            self.view_3D()

            # User input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]: self.player_angle -= 0.1
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]: self.player_angle += 0.1
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                forward = True
                self.player_x += -math.sin(self.player_angle) * 5
                self.player_y += math.cos(self.player_angle) * 5
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                forward = False
                self.player_x -= -math.sin(self.player_angle) * 5
                self.player_y -= math.cos(self.player_angle) * 5
            # if keys[pygame.K_d] TODO for strafe
            #     if MAP[target_x] in ' e': player_x += offset_x
            #     if MAP[target_y] in ' e': player_y += offset_y
            if keys[pygame.K_TAB]:
                self.mini_map()
            # set FPS
            self.clock.tick(30)

            # update display
            pygame.display.flip()


if __name__ == '__main__':
    GameScreen()























