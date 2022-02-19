import pygame

from DungeonAdventure import DungeonAdventure
from Settings import *
from Player import Player
from Drawing import Drawing

class MainGame:
    def __init__(self):
        self.game_data = None
        self.dungeon = None
        self.world_coords = {}
        self.mini_map_coords = set()
        self.screen = None
        self.clock = None
        self.player = None
        self.drawing = None
        self.collision_walls = []
        self.load_game()   

    def load_game(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.obtain_game_data()
        self.player = Player(self.game_data, self.screen, self.world_coords, self.collision_walls)
        self.drawing = Drawing(self.screen, self.mini_map_coords)
        self.game_loop()

    def obtain_game_data(self):
        self.game_data = DungeonAdventure()
        self.dungeon = self.game_data.maze
        # Extract more dungeon data here e.g. rooms, objects, etc.
        # self.entrance_loc = self.dungeon.ingress.coords
        # self.exit_loc = self.maze.egress.coords
        print(self.dungeon)

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
            
            for j, line in enumerate(map_parsed):
                for i, char in enumerate(line):
                    if char == '---' or '+' in char or '|' in char:
                        self.collision_walls.append(pygame.Rect(i * TILE, j * TILE, TILE, TILE))
                        self.world_coords[(i * TILE, j * TILE)] = 'wall'
                        self.mini_map_coords.add((i * MAP_TILE, j * MAP_TILE))
                    if '=' in char or 'H' in char:
                        self.world_coords[(i * TILE, j * TILE)] = 'door'

        parse_map(self.dungeon)
        

    def game_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN \
                    and event.key == pygame.K_ESCAPE):
                    exit()

            self.drawing.background(self.player.angle)
            self.drawing.world(self.screen, self.player.pos, self.player.angle, self.world_coords)
            self.player.movement()  
            
            if self.player.show_map:
                self.drawing.mini_map(self.player)

            self.drawing.fps_display(self.clock)
            pygame.display.flip()
            self.clock.tick(FPS)



if __name__ == '__main__':
    MainGame()





















