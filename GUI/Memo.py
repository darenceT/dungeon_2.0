import pygame
from .Settings import *
from .Utility import create_textline

class Memo:
    """
    TODO docstrings
    """
    def __init__(self, screen):
        self.screen = screen
        self.lines = ['Find all 4 pillars to escape, good luck!']

    def new_message(self, message):
        """
        TODO docstrings
        """
        if len(message) > 40:
            raise ValueError('Message length cannot be longer than 45 characters')
        else:
            self.lines.insert(0, message)

        if len(self.lines) > 4: self.lines.pop()

    def message_box(self):
        """
        TODO docstrings
        """
        size = (8, HALF_HEIGHT + 228, 274, 114)
        border = (5, HALF_HEIGHT + 225, 280, 120)
        pygame.draw.rect(self.screen, BLACK, border)
        pygame.draw.rect(self.screen, WHITE, size)
        self.display_messages()
    
    def display_messages(self):
        """
        TODO docstrings
        """
        index = 0
        y_offset = 30
        while index < len(self.lines):
            txt_color = BLACK
            txt_size = 15
            msg = self.lines[index]
            if index == 0: 
                txt_color = DARK_RED
                txt_size = 18
            txt, text_pos = create_textline(msg, 
                                            pos=(145, HALF_HEIGHT + 240 + y_offset * index),
                                            font_type='GUI/font/Titillium.ttf', 
                                            size=txt_size,
                                            color=txt_color)
            self.screen.blit(txt, text_pos)                                            
            index += 1           

