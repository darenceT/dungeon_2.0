import pygame
from GUI.Settings import *
from GUI.Utility import create_textline

class Cursor:
    def __init__(self) -> None:
        self.size = 40
        self.surface, self.rect = create_textline(
                                    '*', 
                                    pos=(HALF_WIDTH-100, HALF_HEIGHT), 
                                    size=self.size)

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.menu_options = {0:'New', 1:'Load', 2:'Settings'}
        self.menu_input = None
        self.cursor = Cursor()

    def move_cursor(self, move):
        offset = 45
        top_height = HALF_HEIGHT
        bottom_height = top_height + offset * 2
        move_reference = {'DOWN':1, 'UP':-1}

        self.cursor.rect.centery += offset * move_reference[move]
        if self.cursor.rect.centery > bottom_height:
            self.cursor.rect.centery = top_height
        if self.cursor.rect.centery < top_height:
            self.cursor.rect.centery = bottom_height


    def start_screen(self):
        """
        TODO Insert Game over menu here        
        Credit: https://www.geeksforgeeks.org/python-display-text-to-pygame-window/
        """

        title, title_pos = create_textline('DUNGEON 2.0', 
                                            pos=(HALF_WIDTH, HALF_HEIGHT * 3/4), 
                                            size=40)
        new, new_pos = create_textline('New Game', 
                                            pos=(HALF_WIDTH, HALF_HEIGHT), 
                                            size=30)
        load, load_pos = create_textline('Load Game', 
                                            pos=(HALF_WIDTH, HALF_HEIGHT+40), 
                                            size=30)
        setting, setting_pos = create_textline('Settings', 
                                            pos=(HALF_WIDTH, HALF_HEIGHT+80), 
                                            size=30)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.move_cursor('UP')
                    if event.key == pygame.K_DOWN:
                        self.move_cursor('DOWN')
                    if event.key == pygame.K_RETURN: 
                        return
                    elif event.key == pygame.K_ESCAPE:
                        exit()
            self.screen.fill(BLACK)
            self.screen.blit(title, title_pos)
            self.screen.blit(new, new_pos)
            self.screen.blit(load, load_pos)
            self.screen.blit(setting, setting_pos)
            self.screen.blit(self.cursor.surface, self.cursor.rect)
            pygame.display.flip()
