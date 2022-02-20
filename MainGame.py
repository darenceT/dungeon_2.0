import pygame
import pickle

from DungeonAdventure import DungeonAdventure
from GUI.Raycast3D import Raycast
from GUI.Settings import *
from GUI.PlayerControls import PlayerControls
from GUI.Drawing import Drawing
from GUI.Sprites import Sprites

class MainGame:
    def __init__(self):
        self.game_data = None
        self.dungeon = None
        self.world_coords = {}
        self.mini_map_coords = set()
        self.screen = None
        self.player_controls = None
        self.hero = None
        self.drawing = None
        self.sprites = None
        self.collision_walls = []
        self.__load_game()   

    def __load_game(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.__obtain_game_data()
        self.player_controls = PlayerControls(self.game_data, self.screen, self.world_coords, self.collision_walls)
        self.drawing = Drawing(self.screen, self.mini_map_coords)
        self.sprites = Sprites(self.game_data)
        self.__game_loop()

    def __obtain_game_data(self):
        self.game_data = DungeonAdventure()
        self.dungeon = self.game_data.maze
        self.hero = self.game_data.hero
        # Extract more dungeon data here e.g. rooms, objects, etc.
        # self.entrance_loc = self.dungeon.ingress.coords
        # self.exit_loc = self.maze.egress.coords
        print(self.dungeon)                         # DELETE

        def __parse_map(maze):
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

        __parse_map(self.dungeon)
        

    def __game_loop(self):
        clock = pygame.time.Clock()
        while self.hero.is_alive:       # or while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            self.drawing.background(self.player_controls.angle)
            walls = Raycast.view_3D(self.player_controls, self.world_coords, self.drawing.textures)
            objects = [obj.object_locate(self.player_controls, walls) for obj in self.sprites.list_of_objects]
            self.drawing.world(walls + objects)

            self.player_controls.movement()  
            
            if self.player_controls.show_map:
                self.drawing.mini_map(self.player_controls)

            self.drawing.fps_display(clock)
            pygame.display.flip()
            clock.tick(FPS)

        # Insert Game over menu here


if __name__ == '__main__':
    MainGame()





















