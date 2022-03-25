from typing import Any
import pygame
from Model.Util import dat_save, dat_load
from GUI.Settings import *
from GUI.Utility import create_textline

class Cursor:
    """
    Pointer object used in selecting choices in Menu system
    """
    def __init__(self) -> None:
        self.__size = 40
        self.__surface, self.__rect = create_textline(
                                    '*', 
                                    pos=(HALF_WIDTH-150, HALF_HEIGHT + 100),
                                    size=self.__size)

    @property
    def rect(self):
        return self.__rect

    @property
    def surface(self):
        return self.__surface

class Menu:
    """
    Menu system that contains structure to deploy multiple selection screens.
    There are 3 subparts that uses Menu's attributes: intro menu, pause menu, win/lose screen
    """
    # Constants
    X_POS = HALF_WIDTH
    Y_POS = HALF_HEIGHT + 100
    Y_OFFSET = 40

    def __init__(self, screen, sound):
        self.__screen = screen
        self.__sound = sound
        self.__messages: tuple = tuple()
        self.__select_number = 1
        self.__cursor = Cursor()
        self.__images = {
            1: pygame.image.load('GUI/img/thief.png').convert_alpha(),
            2: pygame.image.load('GUI/img/priestess.png').convert_alpha(),
            3: pygame.image.load('GUI/img/warrior.png').convert_alpha()
        }
        self.__reset = False

    @property
    def reset(self):
        """
        Getter for Main to pass trigger to reset game (from pause and win/lose menu)
        """
        return self.__reset

    def __draw(self):
        """
        Brings the menu to life, blits(paints) objects onto a surface then flip(reveal!)
        Attribute self.message acts as param, containing text objects of choices.
        """
        self.__screen.fill(GRAY)
        for obj, pos in self.__messages:
            self.__screen.blit(obj, pos)
        self.__screen.blit(self.__cursor.surface, self.__cursor.rect)
        pygame.display.flip()

    def __move_cursor(self, choices, move=None):
        """
        Within the current menu's displayed set of choices, handle up/down movement of
        the current (but not yet chosen) selection, shifting both the on-screen cursor
        and the internally recorded `self.select_number` that is a key in `choices`.
        Selection wraps around if already at top or bottom.
        :param choices: dictionary of choices, see description in `menu_controls()`
        :param move: str indicating direction of cursor movement, either 'UP' or 'DOWN'
        :return: None
        """
        move_reference = {'DOWN': 1, 'UP': -1}
        if move not in move_reference:
            return
        num = self.__select_number
        # print(f"move_cursor <- {num}:'{choices[num]}' + {move}")
        chg = move_reference[move]
        num += chg
        if num < 1:
            # print(f"move_cursor -> wrap to bottom")
            num = len(choices)
        elif num > len(choices):
            # print(f"move_cursor -> wrap to top")
            num = 1
        # print(f"move_cursor -> {num}:'{choices[num]}")
        self.__select_number = num
        self.__cursor.rect.centery = self.Y_POS + self.Y_OFFSET * (self.__select_number - 1)

    def __menu_controls(self, choices: dict = None, also=None) -> Any:
        """
        Allow user input to selection options. This is used by all menu
        versions of game: intro, pause, ending, etc.
        :param choices: container of choices for a menu screen. Container is a dict.
          The dict values should be unique, as they are the method return value.
          The dict keys must be unique ints, the 1-based index in the menu choices;
          ergo, the range from 1 to the count of menu choices, inclusive.
          For example: `{1:'First item', 2:'Second option', 3:'Third option'}`
          `choices` may also be `None`, indicating an interstitial screen where
          there is no selection for the user to make, only the option to hit return.
        :param also: function to call after a cursor move; typically a "curried" function.
          This is a hack to re-render the hero image in `hero_selection()`.
        :return: value from selected option in `choices`, e.g. `'Second option'` above.
          Or if `choices` was `None`, then `None` is returned.

        In addition to returning one of the values in `choices`, the corresponding
        key in `choices` is recorded as `self.select_number`.
        """
        pygame.event.clear()
        while True:
            event = pygame.event.wait()
            # print(f'menu_controls <- event: {event}')
            if event.type == pygame.QUIT or \
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                num = self.__select_number
                if choices and len(choices) > 1:
                    chose = choices[num]
                else:
                    chose = None
                # print(f"menu_controls -> {num}'{chose}'")
                return chose
            if choices and len(choices) > 1 and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.__move_cursor(choices, 'UP')
                elif event.key == pygame.K_DOWN:
                    self.__move_cursor(choices, 'DOWN')
                self.__draw()
                # hack to update hero images
                if also:
                    also()
                continue  # next event.get()

    def intro_menu(self):
        """
        Controller for intro menu, triggered by Main.
        It is a handler for pickling.
        It will return game option of load or new (and therefore then hero class & name)
        :return: game optin of new vs load, hero class, and hero name
        :rtype: tuple(str, tuple(str, str))
        """
        self.__sound.intro()
        return self.__start_screen()

    def __start_screen(self):
        """
        Handles logic for intro menu, allow load or new game, toggle through 
        hero selection, name input, and instructions. Returns information back to intro_menu()
        :return: game optin of new vs load, hero class, and hero name
        :rtype: tuple(str, tuple(str, str))
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
        self.__messages = ((title1, title1_pos), (title2, title2_pos),
                    (new, new_pos), (load, load_pos), (setting, setting_pos))
        choices = {1: 'New', 2: 'Load', 3: 'Settings'}
        self.__select_number = 1
        self.__cursor.rect.centery = y + y_off * (self.__select_number - 1)
        self.__draw()
        default_names = {'thief': "Theo", 'priestess': "Lena", 'warrior': 'Xena'}
        while True:
            chose = self.__menu_controls(choices)
            self.__draw()
            if chose == 'New':
                print("start_menu <- 'New'")
                print("start_menu -> hero_selection")
                guild = self.__hero_selection()
                print(f"start_menu <- guild '{guild}'")
                print("start_menu -> name_input")
                name = self.__name_input()
                if name == '': name = default_names[guild]
                print(f"start_menu <- name '{name}'")
                print("name -> instructions")
                self.__instructions()           
                return 'new', {'guild': guild, 'name': name}
            elif chose == 'Load':
                print("start_menu <- 'Load'")
                # TODO self.load_menu()
                dat, err = dat_load()
                return 'load', dat
            elif chose == 'Settings':
                # TODO: sound menu or other settings
                print(f"start_menu <- unimplemented '{chose}'")
                # continue, try again
            else:
                print(f"start_menu <- unrecognized '{chose}'")
                # continue, try again

    def __name_input(self):
        """
        Input hero name, more difficult than you'd think compared to using the terminal.
        Loops through to show keys entered.
        TODO: Add more features such as error message for wrong inputs
        TODO: Load default name for each class that disappears on user input
        credit short but glitchy method: https://localcoder.org/pygame-is-there-any-easy-way-to-find-the-letter-number-of-any-alphanumeric-pres
        credit verbose method: https://stackoverflow.com/questions/27713855/how-to-get-an-input-from-user-in-pygame-and-save-it-as-a-variable
        """
        name_input=""
        while True:
            ask1, ask1_pos = create_textline("Please  enter  your  name: ",
                                                pos=(self.X_POS, self.Y_POS - self.Y_OFFSET * 4), size=30)
            ask2, ask2_pos = create_textline("Then  press  enter",
                                                pos=(self.X_POS, self.Y_POS + self.Y_OFFSET * 2), size=20)
            name, name_pos = create_textline(name_input, pos=(self.X_POS, self.Y_POS), size=20)
            self.__messages = ((ask1, ask1_pos), (ask2, ask2_pos), (name, name_pos))
            self.__draw()
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        name_input = name_input[:-1]
                    elif event.key == pygame.K_RETURN:
                        return name_input.strip().capitalize()  
                    elif len(name_input) < 14:    
                        # Option 1: most letters stop working after using backspace
                        name_input += str(event.unicode) 

                        # Option 2: works better but prints out "space, tab, etc"                
                        # name_input += str(pygame.key.name(event.key))
                        
                        # Option 3: Unsightly but works best but cannot use space      
                        # if event.key == pygame.K_a:
                        #     name_input += str(chr(event.key))
                        # elif event.key == pygame.K_b:
                        #     name_input += str(chr(event.key))           
                        # elif event.key == pygame.K_c:
                        #     name_input += str(chr(event.key))
                        # elif event.key == pygame.K_d:
                        #     name_input += str(chr(event.key))
                        # elif event.key == pygame.K_e:
                        #     name_input += str(chr(event.key))
                        # elif event.key == pygame.K_f:
                        #     name_input += str(chr(event.key))
                        # elif event.key == pygame.K_g:
                        #     name_input += str(chr(event.key))
                        # elif event.key == pygame.K_h:
                        #     name_input += str(chr(event.key))
                        # elif event.key == pygame.K_i:
                        #     name_input += str(chr(event.key))
                        # elif event.key == pygame.K_j:
                        #     name_input += str(chr(event.key))
                        # elif event.key == pygame.K_k:
                        #     name_input += str(chr(event.key))
                        # elif event.key == pygame.K_l:
                        #     name_input += str(chr(event.key))
                        # elif event.key == pygame.K_m:
                        #     name_input += str(chr(event.key))
                        # elif event.key == pygame.K_n:
                        #     name_input += str(chr(event.key))
                        # elif event.key == pygame.K_o:
                        #     name_input += str(chr(event.key))
                        # elif event.key == pygame.K_p:
                        #     name_input += str(chr(event.key)) 
                        # elif event.key == pygame.K_q:
                        #     name_input += str(chr(event.key))
                        # elif event.key == pygame.K_r:
                        #     name_input += str(chr(event.key))
                        # elif event.key == pygame.K_s:
                        #     name_input += str(chr(event.key))
                        # elif event.key == pygame.K_t:
                        #     name_input += str(chr(event.key))
                        # elif event.key == pygame.K_u:
                        #     name_input += str(chr(event.key))
                        # elif event.key == pygame.K_v:
                        #     name_input += str(chr(event.key))
                        # elif event.key == pygame.K_x:
                        #     name_input += str(chr(event.key))
                        # elif event.key == pygame.K_y:
                        #     name_input += str(chr(event.key))
                        # elif event.key == pygame.K_z:
                        #     name_input += str(chr(event.key))                                                                                             
            
    def __instructions(self):
        """
        Simple 2-page screen for instructions as part of intro menu,
        appears after hero selection before hero type is returned to Main
        :return: None
        """
        text1 = """
Welcome to Dungeon Escape, brave Hero!

The 4 pillars of object-oriented programming have been captured
by the evil Sorcerer King Ca-Paul, and the world has been plunged
into an age of darkness and endless scripts. Ca-Paul has placed
the pillars under guard by fearsome monsters: 
Ogres, Skeletons, Gremlins, and worst of all--Mean Girls.

Your task--should you dare to accept it--is to locate the 
four pillars and find the exit to Ca-Paul's dungeon before
the monsters drain you of all of your health points.

Take heart! For you will find that not all in Ca-Paul's realm 
are in league with his evil scheme. Within the dungeon, 
neutral wizards have placed Vision potions and Healing potions
for your use. You have also been granted a special ability, 
which you may use to vanquish Ca-Paul's evil brethren.        
"""
        
        text2 = """
Use the following commands to ease your journey:

Arrow keys & A, D, W, S - find your way
E - use your main weapon
R - use your special ability, most useful in a fight
H - use a healing potion
V - use a vision potion (then look at your map)
Tab - toggle to see a map of the maze, thus far explored
Space - Take a breather, pause the game
Escape - Give up & exit program (DANGER: not saved!)

Good luck, brave hero!        
"""
        screens = {
            0: {
                'text': text1,
                'y_off' : 22,
                'size': 20
            },
            1: {
                'text': text2,
                'y_off' : 28,
                'size': 23
            }
        }
        page = 0
        while page < 2:
            text_rendered = []
            text_list = screens[page]['text'].splitlines()
            for number, line in enumerate(text_list):
                txt, txt_pos = create_textline(line, pos=(90, 90 + screens[page]['y_off'] * number), 
                                                font_type='GUI/font/Titillium.ttf', 
                                                size = screens[page]['size'], pos_type='xy')
                text_rendered.append((txt, txt_pos))
            cont, cont_pos = create_textline('Continue', pos=(self.X_POS, self.Y_POS + self.Y_OFFSET * 3), size=30)
            text_rendered.append((cont, cont_pos))

            self.__messages = tuple(text_rendered)
            choices = {1: 'Continue'}
            self.__select_number = 1
            self.__cursor.rect.centery = self.Y_POS + self.Y_OFFSET * 3
            self.__draw()
            self.__menu_controls(choices)
            page += 1

    def __hero_selection(self):
        """ 
        Display and allow hero class selection as part of intro menu
        :return: selected hero class
        :rtype: str
        """
        thief, thief_pos = create_textline('Thief',
                                            pos=(self.X_POS, self.Y_POS),
                                            size=30)
        priestess, priestess_pos = create_textline('Priestess',
                                            pos=(self.X_POS, self.Y_POS + self.Y_OFFSET),
                                            size=30)
        warrior, warrior_pos = create_textline('Warrior',
                                            pos=(self.X_POS, self.Y_POS + self.Y_OFFSET * 2),
                                            size=30)
        self.__messages = ((thief, thief_pos), (priestess, priestess_pos), (warrior, warrior_pos))
        choices = {1: 'thief', 2: 'priestess', 3: 'warrior'}
        self.__select_number = 1
        self.__cursor.rect.centery = self.Y_POS + self.Y_OFFSET * (self.__select_number - 1)
        self.__draw()

        def __draw_hero():
            # TODO after every cursor move, also update character image
            print(f"draw hero {self.__select_number}")
            char_pos = (150, self.Y_OFFSET)
            char_size = (HALF_WIDTH, HALF_HEIGHT)
            char = pygame.transform.scale(self.__images[self.__select_number], char_size)
            self.__screen.blit(char, char_pos)
            pygame.display.flip()

        __draw_hero()
        guild = self.__menu_controls(choices, also=__draw_hero)
        print(f"hero_selection <- hero_class '{guild}'")
        return guild

    def __load_menu(self):
        """
        Currently non-functional as only one saved file.
        Place holder to allow selection of multiple saved files
        """
        load, load_pos = create_textline('Load this game?', 
                                            pos=(self.X_POS, HALF_HEIGHT),
                                            size=30)
        self.__messages = ((load, load_pos),)
        choices = {1: 'Continue'}
        self.__select_number = 1
        self.__cursor.rect.centery = HALF_HEIGHT
        self.__draw()
        self.__menu_controls(choices)

    def pause_menu(self, game_data):
        """ 
        In-game pause menu, accessed by Space key,
        Functions independent of intro_menu but uses
        similar methods of menu_controls() & draw().
        Contains unique feature of saving game
        :param game_data: our game data, which might get saved
        :return: string 'continue' or 'reset'
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
        self.__messages = [(unpause, unpause_pos), (save, save_pos), (reset, reset_pos)]
        choices = {1: 'Continue', 2: 'Save', 3: 'Reset'}
        self.__select_number = 1
        self.__cursor.rect.centery = y + y_off * (self.__select_number - 1)
        self.__draw()
        while True:
            chose = self.__menu_controls(choices)
            self.__draw()
            if chose == 'Continue':
                print(f"pause_menu -> continue game-play")
                return 'continue'
            elif chose == 'Save':
                print(f"pause_menu -> save")
                err = dat_save(game_data)
                if err is not None:
                    print(f'Save failed: {err}')
                else:
                    saved, saved_pos = create_textline('Game  progress  saved',
                                               pos=(x, y - y_off * 2),
                                               size=20)
                    self.__messages.append((saved, saved_pos))
                    
                    # effect of removing message after moving cursor
                    self.__draw()
                    self.__messages.pop() 
            elif chose == 'Reset':
                print(f"pause_menu -> reset")
                self.__reset = True
                return 'reset'
            else:
                print(f"pause_menu <- unrecognized '{chose}'")
                # continue, still in pause_menu

    def lose_screen(self):
        """ 
        At this point game loop has ended as triggered by loop while hero.is_alive
        No additional logic needed to reset game: 
        Return continues loop outside of main class --> create new main then start loop again
        """
        self.__sound.lose()
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
        self.__messages = ((title, title_pos), (reset, reset_pos), (exit_opt, exit_pos))
        choices = {1: 'Reset', 2: 'Exit'}
        self.__select_number = 1
        self.__cursor.rect.centery = y + y_off * (self.__select_number - 1)
        self.__draw()
        while True:
            chose = self.__menu_controls(choices)
            self.__draw()
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
        self.__sound.win()
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
        self.__messages = ((title1, title1_pos), (title2, title2_pos), (reset, reset_pos), (exit_opt, exit_pos))
        choices = {1: 'Reset', 2: 'Exit'}
        self.__select_number = 1
        self.__cursor.rect.centery = y + y_off * (self.__select_number - 1)
        self.__draw()
        while True:
            chose = self.__menu_controls(choices)
            self.__draw()
            if chose == 'Exit':
                # print(f"win_screen -> exit")
                pygame.quit()
                exit()
            elif chose == 'Reset':
                return
            else:
                print(f"win_screen <- unrecognized '{chose}")

# END
