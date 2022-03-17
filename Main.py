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
        self.__sound = Sound()
        self.__screen = None
        self.__menu = None
        self.__game_data = None
        self.world_coords = {}
        self.__mini_map_coords = set()
        self.__player_crtl = None
        self.hero = None
        self.drawing = None
        self.sprites = None
        self.raycast = None
        self.collision_walls = []
        self.__load_game()   

    @property
    def mini_map_coords(self):
        return self.__mini_map_coords

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
        self.__screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.memo = Memo(self.__screen)
        self.__menu = Menu(self.__screen, self.__sound)
        self.__obtain_game_data()

        # TODO: decrease/narrow params passed
        self.__player_crtl = PlayerControls(self.__sound, self.__game_data, self.memo, self.collision_walls)
        self.sprites = SpritesContainer(self.__screen, self.__sound, self.__game_data, self.__player_crtl)
        self.drawing = Drawing(self.__screen, self.__sound, self.__mini_map_coords, self.__player_crtl, 
                               self.hero, self.sprites, self.__game_data.maze.egress.coords)
        self.raycast = Raycast(self.__player_crtl, self.world_coords, self.drawing.textures)
        self.__player_crtl.get_rooms_in_sight()  # initiate sprites for 1st room

    @staticmethod
    def __validate_intro_dat(dat):
        if not isinstance(dat, dict):
            print(f'invalid dat type {type(dat)}')
            return False
        for k in 'guild name'.split():
            if k not in dat:
                print(f'invalid dat, missing {k}')
                return False
        return True

    def __obtain_game_data(self):
        """
        Helper function for load game, obtains:
        hero & dungeon maze (including its monsters & objects)
        """
        while self.__game_data is None:
            op, dat = self.__menu.intro_menu()
            if op == 'new':
                print('new game')
                if not self.__validate_intro_dat(dat):
                    continue
                guild = dat['guild']
                name = dat['name']
                dat = DungeonAdventure(guild=guild, name=name)
            elif op == 'load':
                print('load from saved game')
                if dat is None:
                    print(f'...but dat is None')
            else:
                raise ValueError(f"unrecognized op '{op}'")
            if dat is None:
                continue
            self.__game_data = dat
        self.hero = self.__game_data.hero
        print(self.__game_data.maze)                                         # DELETE ###################### (or move to after winning)
        print(self.hero.name)                                        # DELETE ###########################

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
        __parse_map(self.__game_data.maze)

    def game_loop(self):
        """
        Game work-horse that loops through all major components of game
        to create real-time effect of GUI game
        """
        self.__sound.in_game()
        clock = pygame.time.Clock()
        while self.hero.is_alive:
            clock.tick(FPS)
            self.__player_crtl.movement() 
            if self.__player_crtl.pause_on:
                self.__player_crtl.pause_on = False
                op = self.__menu.pause_menu(game_data=self.__game_data)
                if op == 'continue':
                    print('Carry on as you were.')
                elif op == 'reset':
                    print('Back to square one!')
                    self.__game_data = None
                    break
                else:
                    # "This is bad, Peter. This is very, very bad."
                    print(f'pause_menu returned unrecognized op {op}')
                    break
            elif self.__player_crtl.win_game:
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
        if self.__player_crtl.win_game:
            self.__menu.win_screen()
        elif not self.__menu.reset:
            self.__menu.lose_screen()
            
if __name__ == '__main__':
    try:
        while True:
            m = Main()
            m.game_loop()
    except KeyboardInterrupt:
        print('\n\n                   Thank you for playing!\n\n')
        exit(0)

