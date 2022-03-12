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
    def __init__(self, screen):
        self.screen = screen
        self.menu_input = None
        self.picked = False
        self.select_number = 1
        self.cursor = Cursor()
        self.__x_pos = HALF_WIDTH
        self.__y_pos = HALF_HEIGHT + 100
        self.__y_offset = 40
        self.images = {
            1: pygame.image.load('GUI/img/thief.png').convert_alpha(),
            2: pygame.image.load('GUI/img/priestess.png').convert_alpha(),
            3: pygame.image.load('GUI/img/warrior.png').convert_alpha()
        }

    def move_cursor(self, choices, move=None):
        top_height = self.__y_pos
        bottom_height = top_height + self.__y_offset * (len(choices)-1)
        move_reference = {'DOWN': 1, 'UP': -1}

        if move is not None:
            self.cursor.rect.centery += self.__y_offset * move_reference[move]
            self.select_number += move_reference[move]
            
            if self.select_number < 1:
                self.select_number = len(choices)
                self.cursor.rect.centery = bottom_height
            elif self.select_number > len(choices):
                self.select_number = 1
                self.cursor.rect.centery = top_height
        
        if self.picked:
            self.menu_input = choices[self.select_number]
            self.picked = False

    def __blit_txt(self, envelope):
        """
        loop logic for putting objects on to screen.
        'blit' = put on surface
        'flip' = show user the final surface
        """
        self.screen.fill(GRAY)
        for obj, pos in envelope:
            self.screen.blit(obj, pos)
        self.screen.blit(self.cursor.surface, self.cursor.rect)
        
    def menu_controls(self, choices=None):
        move = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()
            elif choices and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move = 'UP'
                elif event.key == pygame.K_DOWN:
                    move = 'DOWN'
                elif event.key == pygame.K_RETURN:
                    self.picked = True
                self.move_cursor(choices, move)

    def intro_menu(self):
        """
        TODO: input and return hero name
        """
        while True:
            if self.menu_input in ('Warrior', 'Priest', "Thief"):
                return self.menu_input

            elif self.menu_input is None:
                self.start_screen()
            elif self.menu_input == 'New':
                self.instructions()
            elif self.menu_input == 'Hero':
                self.hero_selection()
            elif self.menu_input == 'Load':
                self.menu_input = None
            
            pygame.display.flip()

    def start_screen(self):
        """
        
        """
        x = self.__x_pos
        # x_offset = 50
        y = self.__y_pos
        off = self.__y_offset
        title1, title1_pos = create_textline('DUNGEON',
                                            pos=(x - off, y - off * 6),
                                            size=80)
        title2, title2_pos = create_textline('ESCAPE',
                                            pos=(x, y - off * 4),
                                            size=80)
        new, new_pos = create_textline('New Game',
                                            pos=(x, y),
                                            size=30)
        load, load_pos = create_textline('Load Game',
                                            pos=(x, y + off),
                                            size=30)
        setting, setting_pos = create_textline('Settings',
                                            pos=(x, y + off * 2),
                                            size=30)
        messages = ((title1, title1_pos), (title2, title2_pos),
                    (new, new_pos), (load, load_pos), (setting, setting_pos))
        
        choices = {1: 'New', 2: 'Load', 3: 'Settings'}
        self.menu_controls(choices)
        self.__blit_txt(messages)

    def instructions(self):
        self.menu_input = 'Hero'

    def hero_selection(self):
        """
        """
        x = self.__x_pos
        y = self.__y_pos
        y_off = self.__y_offset
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
        choices = {1: 'Thief', 2: 'Priest', 3: 'Warrior'}
        self.menu_controls(choices)
        self.__blit_txt(messages)

        char_pos = (150, y_off)
        char_size = (HALF_WIDTH, HALF_HEIGHT)
        char = pygame.transform.scale(self.images[self.select_number], char_size)
        self.screen.blit(char, char_pos)

    def load_menu(self):
        load, load_pos = create_textline('Load this game?', 
                                            pos=(self.__x_pos, HALF_HEIGHT),
                                            size=30)
        messages = ((load, load_pos),)
        choices = {1: 'Continue'}
        self.menu_controls(choices)
        self.__blit_txt(messages)

    def pause_menu(self):
        """
        """
        # resets cursor to bottom
        self.select_number = 3
        self.cursor.rect.centery = self.__y_pos + self.__y_offset * 2

        x = self.__x_pos
        y = self.__y_pos
        y_off = self.__y_offset
        save, save_pos = create_textline('Save',
                                            pos=(x, y),
                                            size=30)
        reset, reset_pos = create_textline('Reset',
                                            pos=(x, y + y_off),
                                            size=30)
        unpause, unpause_pos = create_textline('Continue',
                                            pos=(x, y + y_off * 2),
                                            size=30)
        messages = ((save, save_pos), (reset, reset_pos), (unpause, unpause_pos))
        choices = {1: 'Save', 2: 'Reset', 3: 'Continue'}
        while True:
            if self.menu_input == 'Continue':
                self.menu_input = None
                return
            self.menu_controls(choices)
            self.__blit_txt(messages)
            pygame.display.flip()

    def lose_screen(self):
        """
        """
        # resets cursor to top
        self.select_number = 1
        self.cursor.rect.centery = self.__y_pos

        x = self.__x_pos
        y = self.__y_pos
        y_off = self.__y_offset
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
        choices = {1: 'Reset', 2: 'Exit'}
        while True:
            if self.menu_input == 'Exit':
                pygame.quit()
                exit()
            elif self.menu_input == 'Reset':
                self.menu_input = None
                return
            else:
                self.menu_controls(choices)
                self.__blit_txt(messages)
                pygame.display.flip()

    def win_screen(self):
        """
        """
        # resets cursor to top
        self.select_number = 1
        self.cursor.rect.centery = self.__y_pos

        x = self.__x_pos
        y = self.__y_pos
        off = self.__y_offset
        title1, title1_pos = create_textline('You escaped!',
                                            pos=(x - off, y - off * 6),
                                            size=60)
        title2, title2_pos = create_textline('Winner winner!',
                                            pos=(x, y - off * 4),
                                            size=60)
        reset, reset_pos = create_textline('Play again?',
                                            pos=(x, y),
                                            size=30)
        exit_opt, exit_pos = create_textline('Exit',
                                            pos=(x, y + off),
                                            size=30)
        messages = ((title1, title1_pos), (title2, title2_pos), (reset, reset_pos), (exit_opt, exit_pos))
        choices = {1: 'Reset', 2: 'Exit'}
        while True:
            if self.menu_input == 'Exit':
                pygame.quit()
                exit()
            elif self.menu_input == 'Reset':
                self.menu_input = None
                return
            else:
                self.menu_controls(choices)
                self.__blit_txt(messages)
                pygame.display.flip()

# END
