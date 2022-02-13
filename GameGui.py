import pygame
import sys
import math

from GuiSettings import *
from Maze import Maze
from Raycast3D import Raycast
from Drawing import Drawing


class GameScreen:
    """
    In-game screen
    Intro screen to be added later
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
        self.drawing = None
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
        self.drawing = Drawing(self.screen)
        self.game_loop()

    def mini_map(self):
        """
        Creates map top left corner with player's position and 
        the direction player is facing on map
        Hold Tab during game to view map
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
    
    def game_loop(self):
        # moving direction
        forward = True
        # lateral_strafe = False
        # left_move = False

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
            player_speed = 5
            sin = -math.sin(self.player_angle) * player_speed
            cos = math.cos(self.player_angle) * player_speed

            if self.map[index] == '+' or self.map[index] == '-' or self.map[index] == '|':
                if forward:
                    self.player_x -= sin
                    self.player_y -= cos
                else:
                    self.player_x += sin
                    self.player_y += cos
                #TODO Fix bug sometimes go through wall
                # if lateral_strafe and left_move:     
                #     self.player_x -= cos
                #     self.player_y -= -sin
                # elif lateral_strafe:
                #     self.player_x -= -cos
                #     self.player_y -= sin


            # update 3D background
            self.drawing.background(self.player_angle)

            # raycasting for 3D view
            Raycast.view_3D(self.screen, (self.player_x, self.player_y), self.player_angle, self.map, )

            # User input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]: self.player_angle -= 0.1
            if keys[pygame.K_RIGHT]: self.player_angle += 0.1
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                forward = True
                self.player_x += sin
                self.player_y += cos
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                forward = False
                self.player_x -= sin
                self.player_y -= cos
            # if keys[pygame.K_a]:      # TODO fix above wall collision
            #     lateral_strafe = True
            #     left_move = True
            #     self.player_x += cos
            #     self.player_y += -sin
            # if keys[pygame.K_d]: 
            #     lateral_strafe = True
            #     self.player_x += -cos
            #     self.player_y += sin
            if keys[pygame.K_TAB]:
                self.mini_map()
            # set FPS
            self.clock.tick(FPS)


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























