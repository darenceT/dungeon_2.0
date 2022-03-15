import pygame
import pickle

from DungeonAdventure import DungeonAdventure
from GUI.Raycast3D import Raycast
from GUI.Settings import *
from GUI.PlayerControls import PlayerControls
from GUI.Drawing import Drawing
from GUI.Sprites import SpritesContainer
from GUI.Menu import Menu
from GUI.Memo import Memo
from GUI.Sound import Sound


class Main:
    """
    Pygame controller for running game. This class works in tandem and gets information
    from DungeonAdventure which is the non-GUI controller of Model
    """
    save_file = 'dungeon_save.pkl'

    def __init__(self):
        self.sound = Sound()
        self.screen = None
        self.menu = None
        self.game_data = None
        self.dungeon = None
        self.world_coords = {}
        self.__mini_map_coords = set()
        self.player_controls = None
        self.guild = None
        self.hero = None
        self.drawing = None
        self.sprites = None
        self.raycast = None
        self.collision_walls = []
        self.__load_game()   

    @property
    def mini_map_coords(self):
        return self.__mini_map_coords
    
    @property
    def mini_map_exit_coords(self):
        return self.__mini_map_exit_coords

    def __load_game(self):
        """
        Load data needed for game, mainly:
        1. Setup models for pygame, loading constructors for
           GUI controls (PlayerControl), GUI objects (Sprites),
           drawing modules onto GUI sufrace (Drawing & Memo),
           and "3D engine" of sorts by Raycasting
        2. Grab Model information from DungeonAdventure.
        """
        pygame.init()
        pygame.event.set_blocked(None)  # start by block everything
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])  # allow only those relevant
        pygame.display.set_caption('Dungeon Escape')
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.memo = Memo(self.screen)
        self.menu = Menu(self.screen, self.sound)
        self.__obtain_game_data()

        # TODO: decrease/narrow params passed
        self.player_controls = PlayerControls(self.sound, self.game_data, self.memo, self.collision_walls)
        self.sprites = SpritesContainer(self.screen, self.sound, self.game_data, self.player_controls)
        self.drawing = Drawing(self.screen, self.sound, self.__mini_map_coords, self.player_controls, 
                               self.hero, self.sprites, self.game_data.maze.egress.coords)
        self.raycast = Raycast(self.player_controls, self.world_coords, self.drawing.textures)
        self.player_controls.get_rooms_in_sight()  # initiate sprites for 1st room

    def __obtain_game_data(self):
        """
        Helper function for load game, obtains:
        hero & dungeon maze (including its monsters & objects)
        """
        while not self.guild or not self.game_data:
            op, dat = self.menu.intro_menu()
            if op == 'new':
                print('new game')
                self.guild = dat[0]
                self.game_data = DungeonAdventure(guild=self.guild)
            elif op == 'load':
                print('load from saved game')
                try:
                    with open(file=self.save_file, mode='r') as f:
                        dat = pickle.load(f)
                        self.game_hero = dat[0]
                        self.game_data = dat[1]
                except Exception as e:
                    print(f"load failed: {e}")
            else:
                raise ValueError(f"unrecognized op '{op}'")
        self.dungeon = self.game_data.maze
        self.hero = self.game_data.hero
        print(self.dungeon)                         # DELETE

        def __parse_map(maze):
            """
            Parse maze layout information into usable
            information to create walls for GUI
            Converts 4x4 string map into 9x9, lists of 3-length strings, 9th will be 1 char
            """
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
                if len(temp) > 0:   
                    row.append(temp)
                map_parsed.append(row)
                row = []
            for j, line in enumerate(map_parsed):
                for i, char in enumerate(line):                                                                        
                    if char == '---' or '+' in char or '|' in char:
                        self.collision_walls.append(pygame.Rect(i * TILE, j * TILE, TILE, TILE))
                        self.world_coords[(i * TILE, j * TILE)] = 'wall'
                        self.__mini_map_coords.add((i * MAP_TILE, j * MAP_TILE))
                    elif '=' in char or char[0] == 'H':
                        self.world_coords[(i * TILE, j * TILE)] = 'door'             
        __parse_map(self.dungeon)

    def game_loop(self):
        """
        Game work-horse that loops through all major components of game
        to create real-time effect of GUI game
        """
        self.sound.in_game()
        clock = pygame.time.Clock()
        while self.hero.is_alive:
            clock.tick(FPS)
            self.player_controls.movement() 
            if self.player_controls.pause_on:
                self.player_controls.pause_on = False
                self.menu.pause_menu()
                if self.menu.reset:
                    break
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
        print(self.player_controls.cur_room.coords)
        if self.player_controls.win_game:
            self.menu.win_screen()
        elif not self.menu.reset:
            self.menu.lose_screen()
            
if __name__ == '__main__':
    try:
        while True:
            m = Main()
            m.game_loop()
    except KeyboardInterrupt:
        print('\n\n                   Thank you for playing!\n\n')
        exit(0)

