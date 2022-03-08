import pygame
from GUI.Settings import *
from GUI.Utility import create_textline

class Cursor:
    def __init__(self) -> None:
        self.size = 40
        self.surface, self.rect = create_textline(
                                    '*', 
                                    pos=(HALF_WIDTH-140, HALF_HEIGHT + 100), 
                                    size=self.size)

class Menu:
    def __init__(self, screen):
        self.screen = screen
        # self.menu_options = {0:'New', 1:'Load', 2:'Settings'}
        self.menu_input = None
        # self.option_count = None
        self.picked = False
        self.select_number = 1
        self.cursor = Cursor()
        self.images = {
            1: pygame.image.load('GUI/img/thief.png').convert_alpha(),
            2: pygame.image.load('GUI/img/priestess.png').convert_alpha(),
            3: pygame.image.load('GUI/img/warrior.png').convert_alpha()
        }

    def move_cursor(self, choices, move=None):
        offset = 40
        top_height = HALF_HEIGHT + 100
        bottom_height = top_height + offset * (len(choices)-1)
        move_reference = {'DOWN':1, 'UP':-1}

        if move is not None:
            self.cursor.rect.centery += offset * move_reference[move]
            self.select_number += move_reference[move]
            
            if self.select_number < 1:
            # if self.cursor.rect.centery < top_height:
                self.select_number = len(choices)
                self.cursor.rect.centery = bottom_height
            # if self.cursor.rect.centery > bottom_height:
            if self.select_number > len(choices):
                self.select_number = 1
                self.cursor.rect.centery = top_height
        
        if self.picked:
            self.menu_input = choices[self.select_number]
            self.select_number = 1
            self.picked = False


    def __blit_txt(self, envelope):
        """
        loop logic for putting objects on to screen.
        'blit' = put on surface
        'flip' = show user the final surface
        """
        self.screen.fill(GRAY)
        for object, pos in envelope:
            self.screen.blit(object, pos)
        self.screen.blit(self.cursor.surface, self.cursor.rect)
        

    def menu_controls(self, choices):
        move = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: move = 'UP'
                if event.key == pygame.K_DOWN: move = 'DOWN'
                if event.key == pygame.K_RETURN: self.picked = True
            self.move_cursor(choices, move)

    def intro_menu(self):
        """
        TODO: input and return hero name
        """
        while True:
            # print('menu_input:', self.menu_input, 'picked: ', self.picked)
            if self.menu_input in ('Warrior', 'Priest', "Thief"):
                return self.menu_input

            elif self.menu_input == None:
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
        x_pos = HALF_WIDTH
        x_offset = 50
        y_pos = HALF_HEIGHT + 100
        y_offset = 40
        title1, title1_pos = create_textline('DUNGEON', 
                                            pos=(x_pos - x_offset, y_pos - y_offset * 6), 
                                            size=80)
        title2, title2_pos = create_textline('ESCAPE', 
                                            pos=(x_pos, y_pos - y_offset * 4), 
                                            size=80)
        new, new_pos = create_textline('New Game', 
                                            pos=(x_pos, y_pos), 
                                            size=30)
        load, load_pos = create_textline('Load Game', 
                                            pos=(x_pos, y_pos + y_offset), 
                                            size=30)
        setting, setting_pos = create_textline('Settings', 
                                            pos=(x_pos, y_pos + y_offset * 2), 
                                            size=30)
        messages = ((title1,title1_pos), (title2,title2_pos),
                    (new, new_pos), (load, load_pos), (setting, setting_pos))
        
        choices={1:'New', 2:'Load', 3:'Settings'}
        self.menu_controls(choices)
        self.__blit_txt(messages)

    def instructions(self):
        self.menu_input = 'Hero'

    def hero_selection(self):
        """
        """
        x_pos = HALF_WIDTH
        y_pos = HALF_HEIGHT + 100
        y_offset = 40
        thief, thief_pos = create_textline('Thief', 
                                            pos=(x_pos, y_pos), 
                                            size=30)
        priestess, priestess_pos = create_textline('Priest', 
                                            pos=(x_pos, y_pos + y_offset), 
                                            size=30)
        warrior, warrior_pos = create_textline('Warrior', 
                                            pos=(x_pos, y_pos + y_offset * 2), 
                                            size=30)
        messages = ((thief, thief_pos), (priestess, priestess_pos), (warrior, warrior_pos))
        choices = {1:'Thief', 2:'Priest', 3:'Warrior'}
        self.menu_controls(choices)
        self.__blit_txt(messages)

        char_pos = (150, y_offset)
        char_size = (HALF_WIDTH, HALF_HEIGHT)
        char = pygame.transform.scale(self.images[self.select_number], char_size)
        self.screen.blit(char, char_pos)

    def load_menu(self):
        load, load_pos = create_textline('Load this game?', 
                                            pos=(HALF_WIDTH, HALF_HEIGHT), 
                                            size=30)
        messages = ((load, load_pos))
        choices = {1:'Continue'}
        self.menu_controls(choices)
        self.__blit_txt(messages)

    def pause_menu(self):
        save, save_pos = create_textline('Save', 
                                            pos=(HALF_WIDTH, HALF_HEIGHT), 
                                            size=30)
        reset, reset_pos = create_textline('Reset', 
                                            pos=(HALF_WIDTH, HALF_HEIGHT+40), 
                                            size=30)
        unpause, unpause_pos = create_textline('Continue', 
                                            pos=(HALF_WIDTH, HALF_HEIGHT+80), 
                                            size=30)
        messages = ((save, save_pos), (reset, reset_pos), (unpause, unpause_pos))
        self.option_count = len(messages)
        while True:
            if not self.menu_controls():
                return False
            self.__blit_txt(messages)
            
    def end_screen(self):
        """
        Credit: https://www.geeksforgeeks.org/python-display-text-to-pygame-window/
        """
        title, title_pos = create_textline('GAME OVER', 
                                            pos=(HALF_WIDTH, HALF_HEIGHT * 3/4), 
                                            size=60)
        reset, reset_pos = create_textline('Try again?', 
                                            pos=(HALF_WIDTH, HALF_HEIGHT), 
                                            size=30)
        done, done_pos = create_textline('I AM DONE', 
                                            pos=(HALF_WIDTH, HALF_HEIGHT+40), 
                                            size=30)
        messages = ((title, title_pos), (reset, reset_pos), (done, done_pos))
        self.option_count = len(messages)-1
        while True:
            if not self.menu_controls():
                return False

            self.__blit_txt(messages)