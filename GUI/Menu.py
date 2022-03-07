import pygame
from GUI.Settings import *
from GUI.Utility import create_textline

class Cursor:
    def __init__(self) -> None:
        self.size = 40
        self.surface, self.rect = create_textline(
                                    '*', 
                                    pos=(HALF_WIDTH-140, HALF_HEIGHT), 
                                    size=self.size)

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.menu_options = {0:'New', 1:'Load', 2:'Settings'}
        self.menu_input = None
        self.option_count = None
        self.cursor = Cursor()

    def move_cursor(self, move):
        offset = 40
        top_height = HALF_HEIGHT
        bottom_height = top_height + offset * (self.option_count-1)
        move_reference = {'DOWN':1, 'UP':-1}

        self.cursor.rect.centery += offset * move_reference[move]
        if self.cursor.rect.centery > bottom_height:
            self.cursor.rect.centery = top_height
        if self.cursor.rect.centery < top_height:
            self.cursor.rect.centery = bottom_height

    def __blit_and_flip(self, envelope):
        """
        loop logic for putting objects on to screen.
        'blit' = put on surface
        'flip' = show user the final surface
        """
        self.screen.fill(GRAY)

        for object, pos in envelope:
            self.screen.blit(object, pos)

        self.screen.blit(self.cursor.surface, self.cursor.rect)
        pygame.display.flip()

    def menu_controls(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.move_cursor('UP')
                if event.key == pygame.K_DOWN:
                    self.move_cursor('DOWN')
                if event.key == pygame.K_RETURN:
                    return False
        return True

    def start_screen(self):
        """
        TODO convert height adjustment into offset variable, move size values to settings
        """

        title1, title1_pos = create_textline('DUNGEON', 
                                            pos=(HALF_WIDTH-50, HALF_HEIGHT * 1/2), 
                                            size=80)
        title2, title2_pos = create_textline('ESCAPE', 
                                            pos=(HALF_WIDTH, HALF_HEIGHT * 3/4), 
                                            size=80)
        new, new_pos = create_textline('New Game', 
                                            pos=(HALF_WIDTH, HALF_HEIGHT), 
                                            size=30)
        load, load_pos = create_textline('Load Game', 
                                            pos=(HALF_WIDTH, HALF_HEIGHT+40), 
                                            size=30)
        setting, setting_pos = create_textline('Settings', 
                                            pos=(HALF_WIDTH, HALF_HEIGHT+80), 
                                            size=30)
        messages = ((title1,title1_pos), (title2,title2_pos),
                    (new, new_pos), (load, load_pos), (setting, setting_pos))
        self.option_count = len(messages)-2
        while True:
            if not self.menu_controls():
                return False

            self.__blit_and_flip(messages)

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

            self.__blit_and_flip(messages)
            

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

            self.__blit_and_flip(messages)