import pygame
import math
from Settings import *
from Player import Player
from Maze import Maze
#from Raycast3D import Raycast
from Drawing import Drawing

class MainGame:
    def __init__(self):
        self.entrance_loc = None
        self.exit_loc = None
        self.maze = None
        self.world_coords = {}
        self.mini_map_coords = set()
        self.screen = None
        self.clock = None
        self.player = None
        self.drawing = None
        self.load_game()   

    def load_game(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.obtain_map_data()
        self.player = Player(self.entrance_loc, self.screen, self.world_coords)
        self.drawing = Drawing(self.screen, self.mini_map_coords)
        self.game_loop()

    def obtain_map_data(self):
        self.maze = Maze()
        self.entrance_loc = self.maze.ingress.coords
        self.exit_loc = self.maze.egress.coords
        print(self.maze)

        def parse_map(maze):
            map_text = maze.str().splitlines()
            map_parsed = []
            row = []
            for line in map_text:
                temp = ''
                i = 0
                while i < len(line):
                    if len(temp) == 3:
                        row.append(temp)
                        temp = ''
                    temp += line[i]
                    i += 1
                if len(line) > 0:
                    row.append(temp)
                i = 0
                map_parsed.append(row)
                row = []
            
            for j, row in enumerate(map_parsed):
                for i, char in enumerate(row):
                    if char == '---' or '+' in char or '|' in char:
                        self.world_coords[(i * TILE, j * TILE)] = '1'
                        self.mini_map_coords.add((i * MAP_TILE, j * MAP_TILE))

        parse_map(self.maze)
        

    def game_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN \
                    and event.key == pygame.K_ESCAPE):
                    exit()
            
            # self.screen.fill('black')

            pygame.draw.rect(self.screen, 'blue', (0, 0, WIDTH, HALF_HEIGHT))
            pygame.draw.rect(self.screen, 'gray', (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))

            self.drawing.world(self.screen, self.player.pos, self.player.angle, self.world_coords)
            self.player.movement()  
            # drawing.background()


            if pygame.key.get_pressed()[pygame.K_TAB]:
                self.drawing.mini_map(self.player)

            self.drawing.fps_display(self.clock)
            pygame.display.flip()
            self.clock.tick(FPS)



if __name__ == '__main__':
    MainGame()





















