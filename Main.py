import pygame
# import pickle

from DungeonAdventure import DungeonAdventure
from GUI.Raycast3D import Raycast
from GUI.Settings import *
from GUI.PlayerControls import PlayerControls
from GUI.Drawing import Drawing
from GUI.Sprites import SpritesContainer
from GUI.Menu import Menu
from GUI.Memo import Memo


class Main:
    def __init__(self):
        self.screen = None
        self.menu = None
        self.game_data = None
        self.dungeon = None
        self.world_coords = {}
        self.mini_map_coords = set()
        self.player_controls = None
        self.hero_class = None
        self.hero = None
        self.drawing = None
        self.sprites = None
        self.raycast = None
        self.collision_walls = []
        self.__load_game()   

    def __load_game(self):
        pygame.init()
        pygame.display.set_caption('Dungeon Escape')
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.memo = Memo(self.screen)
        self.menu = Menu(self.screen)
        self.__obtain_game_data()

        # TODO: decrease/narrow params passed
        self.player_controls = PlayerControls(self.screen, self.game_data, self.memo, self.collision_walls)
        self.sprites = SpritesContainer(self.screen, self.game_data, self.player_controls)
        self.drawing = Drawing(self.screen, self.hero_class, self.mini_map_coords, self.player_controls,
                               self.hero, self.sprites)
        self.raycast = Raycast(self.player_controls, self.world_coords, self.drawing.textures)
        self.player_controls.get_rooms_in_sight()  # initiate sprites for 1st room

    def __obtain_game_data(self):
        self.hero_class = self.menu.intro_menu()
        self.game_data = DungeonAdventure()
        self.dungeon = self.game_data.maze
        self.hero = self.game_data.hero
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

    def game_loop(self):
        clock = pygame.time.Clock()
        while self.hero.is_alive:
            clock.tick(FPS)
            self.player_controls.movement() 
            if self.player_controls.pause_on:
                self.player_controls.pause_on = False
                self.menu.pause_menu()
            elif self.player_controls.win_game:
                break
            else:
                self.drawing.background()
                self.sprites.load_sprites()

                walls = self.raycast.view_3D()
                objects = self.sprites.obtain_sprites(walls)
                self.drawing.world(walls + objects)

                self.memo.message_box()
                self.drawing.weapon_and_ui(clock)
                pygame.display.flip()
        
        if self.player_controls.win_game:
            self.menu.win_screen()
        else:
            self.menu.lose_screen()
            
if __name__ == '__main__':
    try:
        while True:
            m = Main()
            m.game_loop()
    except KeyboardInterrupt:
        print('\n\n                   Thank you for playing!\n\n')
        exit(0)

