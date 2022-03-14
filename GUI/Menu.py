from typing import Any
import pygame
from GUI.Settings import *
from GUI.Utility import create_textline

class Cursor:
    def __init__(self) -> None:
        self.size = 40
        self.surface, self.rect = create_textline(
                                    '*', 
                                    pos=(HALF_WIDTH-150, HALF_HEIGHT + 100),
                                    size=self.size)

class Menu:
    # Constants
    X_POS = HALF_WIDTH
    Y_POS = HALF_HEIGHT + 100
    Y_OFFSET = 40

    def __init__(self, screen, sound):
        self.screen = screen
        self.sound = sound
        self.messages: tuple = tuple()
        self.select_number = 1
        self.cursor = Cursor()
        self.images = {
            1: pygame.image.load('GUI/img/thief.png').convert_alpha(),
            2: pygame.image.load('GUI/img/priestess.png').convert_alpha(),
            3: pygame.image.load('GUI/img/warrior.png').convert_alpha()
        }
        self.__reset = False

    @property
    def reset(self):
        return self.__reset

    def draw(self):
        self.screen.fill(GRAY)
        for obj, pos in self.messages:
            self.screen.blit(obj, pos)
        self.screen.blit(self.cursor.surface, self.cursor.rect)
        pygame.display.flip()

    def move_cursor(self, choices, move=None):
        move_reference = {'DOWN': 1, 'UP': -1}
        if move not in move_reference:
            return
        num = self.select_number
        print(f"move_cursor <- {num}:'{choices[num]}' + {move}")
        chg = move_reference[move]
        num += chg
        if num < 1:
            print(f"move_cursor -> wrap to bottom")
            num = len(choices)
        elif num > len(choices):
            print(f"move_cursor -> wrap to top")
            num = 1
        print(f"move_cursor -> {num}:'{choices[num]}")
        self.select_number = num
        self.cursor.rect.centery = self.Y_POS + self.Y_OFFSET * (self.select_number - 1)

    def menu_controls(self, choices=None, also=None) -> Any:
        pygame.event.clear()
        while True:
            event = pygame.event.wait()
            print(f'menu_controls <- event: {event}')
            if event.type == pygame.QUIT or \
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                num = self.select_number
                chose = choices[num]
                print(f"menu_controls -> {num}'{chose}'")
                return chose
            if len(choices) > 1 and event.type == pygame.KEYDOWN:
            # if choices and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.move_cursor(choices, 'UP')
                elif event.key == pygame.K_DOWN:
                    self.move_cursor(choices, 'DOWN')
                self.draw()
                # FIXME hack to update hero images
                if also:
                    also()
                continue  # next event.get()

    def intro_menu(self):
        """
        TODO: input and return hero name
        """
        self.sound.intro()
        return self.start_screen()

    def start_screen(self):
        """
        TODO docs
        """
        x = self.X_POS
        y = self.Y_POS
        y_off = self.Y_OFFSET
        # Static
        title1, title1_pos = create_textline('DUNGEON',
                                            pos=(x - y_off, y - y_off * 6),
                                            size=80)
        title2, title2_pos = create_textline('ESCAPE',
                                            pos=(x, y - y_off * 4),
                                            size=80)
        # Choices
        new, new_pos = create_textline('New Game',
                                            pos=(x, y),
                                            size=30)
        load, load_pos = create_textline('Load Game',
                                            pos=(x, y + y_off),
                                            size=30)
        setting, setting_pos = create_textline('Settings',
                                            pos=(x, y + y_off * 2),
                                            size=30)
        messages = ((title1, title1_pos), (title2, title2_pos),
                    (new, new_pos), (load, load_pos), (setting, setting_pos))
        self.messages = messages
        choices = {1: 'New', 2: 'Load', 3: 'Settings'}
        self.select_number = 1
        self.cursor.rect.centery = y + y_off * (self.select_number - 1)
        self.draw()
        while True:
            chose = self.menu_controls(choices)
            self.draw()
            if chose == 'New':
                print("start_menu <- 'New'")
                print("start_menu -> hero_selection")
                hero_class = self.hero_selection()  
                print("hero_selected -> instructions")
                self.instructions()           
                print(f"start_menu <- hero_class '{hero_class}'")
                return 'new', (hero_class, None)
            elif chose == 'Load':
                print("start_menu <- 'Load'")
                return 'load', None
            elif chose == 'Settings':
                print(f"start_menu <- unimplemented '{chose}'")
                # continue, try again
            else:
                print(f"start_menu <- unrecognized '{chose}'")
                # continue, try again

    def instructions(self):
        text1 = """
Welcome to Dungeon Escape, brave Hero!

The 4 pillars of object-oriented programming have been captured
by the evil Sorcerer King Ca-Pul, and the world has been plunged
into an age of darkness and endless scripts. Ca-Pu has placed
the pillars under guard by fearsome monsters: 
Ogres, Skeletons, Gremlins, and worst of all--Mean Girls.

Your task--should you dare to accept it--is to locate the 
four pillars and find the exit to Ca-Pul's dungeon before
the monsters drain you of all of your health points.

Take heart! For you will find that not all in Ca-Pul's realm 
are in league with his evil scheme. Within the dungeon, 
neutral wizards have placed Vision potions and Healing potions
for your use. You have also been granted a special ability, 
which you may use to vanquish Ca-Pul's evil brethren.        
"""
        
        text2 = """
Use the following commands to ease your journey:

Arrow keys & A, D, W, S - find your way
E - use your main weapon
R - use your special ability, most useful in a fight
H - use a healing potion
V - use a vision potion (then look at your map)
Tab - see a map of the maze, thus far explored
Space - Take a breather, pause the game

Good luck, brave hero!        
"""
        #TODO remove x,y in dict since they are same/similar
        screens = {
            0: {
                'text': text1,
                'x': 100,
                'y': 100,
                'y_off' : 22,
                'size': 20
            },
            1: {
                'text': text2,
                'x': 100,
                'y': 100,
                'y_off' : 28,
                'size': 25
            }
        }
        page = 0
        while page < 2:
            text_rendered = []
            text_list = screens[page]['text'].splitlines()
            for number, line in enumerate(text_list):
                txt, txt_pos = create_textline(line, pos=(screens[page]['x'], 
                                                screens[page]['y'] + screens[page]['y_off'] * number), 
                                                font_type='GUI/font/Titillium.ttf', 
                                                size = screens[page]['size'], pos_type='xy')
                text_rendered.append((txt, txt_pos))
            cont, cont_pos = create_textline('Continue', pos=(self.X_POS, self.Y_POS + self.Y_OFFSET * 3), size=30)
            text_rendered.append((cont, cont_pos))

            messages = tuple(text_rendered)
            self.messages = messages
            choices = {1: 'Continue'}
            self.select_number = 1
            self.cursor.rect.centery = self.Y_POS + self.Y_OFFSET * 3
            self.draw()
            self.menu_controls(choices)
            page += 1

    def hero_selection(self):
        """ TODO docs
        """
        x = self.X_POS
        y = self.Y_POS
        y_off = self.Y_OFFSET
        thief, thief_pos = create_textline('Thief',
                                            pos=(x, y),
                                            size=30)
        priestess, priestess_pos = create_textline('Priest',
                                            pos=(x, y + y_off),
                                            size=30)
        warrior, warrior_pos = create_textline('Warrior',
                                            pos=(x, y + y_off * 2),
                                            size=30)
        messages = ((thief, thief_pos), (priestess, priestess_pos), (warrior, warrior_pos))
        self.messages = messages
        choices = {1: 'thief', 2: 'priest', 3: 'warrior'}
        self.select_number = 1
        self.cursor.rect.centery = y + y_off * (self.select_number - 1)
        self.draw()

        def draw_hero():
            # TODO after every cursor move, also update character image
            print(f"draw hero {self.select_number}")
            char_pos = (150, y_off)
            char_size = (HALF_WIDTH, HALF_HEIGHT)
            char = pygame.transform.scale(self.images[self.select_number], char_size)
            self.screen.blit(char, char_pos)
            pygame.display.flip()

        draw_hero()
        hero_class = self.menu_controls(choices, also=draw_hero)
        print(f"hero_selection <- hero_class '{hero_class}'")
        # TODO get name
        return hero_class

    def load_menu(self):
        load, load_pos = create_textline('Load this game?', 
                                            pos=(self.X_POS, HALF_HEIGHT),
                                            size=30)
        messages = ((load, load_pos),)
        self.messages = messages
        choices = {1: 'Continue'}
        self.select_number = 1
        self.cursor.rect.centery = HALF_HEIGHT
        self.draw()
        self.menu_controls(choices)

    def pause_menu(self):
        """ TODO docs
        """

        x = self.X_POS
        y = self.Y_POS
        y_off = self.Y_OFFSET
        unpause, unpause_pos = create_textline('Continue',
                                               pos=(x, y),
                                               size=30)
        save, save_pos = create_textline('Save',
                                         pos=(x, y + y_off),
                                         size=30)
        reset, reset_pos = create_textline('Reset',
                                           pos=(x, y + y_off * 2),
                                           size=30)
        messages = ((unpause, unpause_pos), (save, save_pos), (reset, reset_pos))
        self.messages = messages
        choices = {1: 'Continue', 2: 'Save', 3: 'Reset'}
        self.select_number = 1
        self.cursor.rect.centery = y + y_off * (self.select_number - 1)
        self.draw()
        while True:
            chose = self.menu_controls(choices)
            self.draw()
            if chose == 'Continue':
                print(f"pause_menu -> continue game-play")
                return
            elif chose == 'Reset':
                print(f"pause_menu -> reset, unimplemented")
                # TODO quit game... then restart with trip through start_menu?
                self.__reset = True
                return
            elif chose == 'Save':
                print(f"pause_menu -> save, unimplemented")
                # TODO save game
                # TODO display some indication whether succeeded
                # continue, still in pause_menu
            else:
                print(f"pause_menu <- unrecognized '{chose}'")
                # continue, still in pause_menu

    def lose_screen(self):
        """ 
        At this point game loop has ended as triggered by loop while hero.is_alive
        No additional logic needed to reset game: 
        Return continues loop outside of main class --> create new main then start loop again
        """
        self.sound.lose()
        x = self.X_POS
        y = self.Y_POS
        y_off = self.Y_OFFSET
        title, title_pos = create_textline('GAME OVER',
                                            pos=(x, y - y_off * 4),
                                            size=60)
        reset, reset_pos = create_textline('Try again?',
                                            pos=(x, y),
                                            size=30)
        exit_opt, exit_pos = create_textline('Exit',
                                            pos=(x, y + y_off),
                                            size=30)
        messages = ((title, title_pos), (reset, reset_pos), (exit_opt, exit_pos))
        self.messages = messages
        choices = {1: 'Reset', 2: 'Exit'}
        self.select_number = 1
        self.cursor.rect.centery = y + y_off * (self.select_number - 1)
        self.draw()
        while True:
            chose = self.menu_controls(choices)
            self.draw()
            if chose == 'Exit':
                print(f"lose_screen -> exit")
                pygame.quit()
                exit()
            elif chose == 'Reset':
                return
            else:
                print(f"lose_screen <- unrecognized '{chose}")

    def win_screen(self):
        """ 
        At this point game loop has ended as triggered at PlayerControls when
        hero has obtained 4 pillars and reached exit.
        No additional logic needed to reset game: 
        Return continues loop outside of main class --> create new main then start loop again
        """
        self.sound.win()
        x = self.X_POS
        y = self.Y_POS
        y_off = self.Y_OFFSET
        title1, title1_pos = create_textline('You  escaped!',
                                            pos=(x - y_off, y - y_off * 6),
                                            size=60)
        title2, title2_pos = create_textline('Winner winner!',
                                            pos=(x, y - y_off * 4),
                                            size=40)
        reset, reset_pos = create_textline('Play again?',
                                            pos=(x, y),
                                            size=30)
        exit_opt, exit_pos = create_textline('Exit',
                                            pos=(x, y + y_off),
                                            size=30)
        messages = ((title1, title1_pos), (title2, title2_pos), (reset, reset_pos), (exit_opt, exit_pos))
        self.messages = messages
        choices = {1: 'Reset', 2: 'Exit'}
        self.select_number = 1
        self.cursor.rect.centery = y + y_off * (self.select_number - 1)
        self.draw()
        while True:
            chose = self.menu_controls(choices)
            self.draw()
            if chose == 'Exit':
                print(f"win_screen -> exit")
                pygame.quit()
                exit()
            elif chose == 'Reset':
                return
            else:
                print(f"win_screen <- unrecognized '{chose}")

# END
