import pygame
from .Settings import *
from .Utility import create_textline

class Memo:
    def __init__(self, screen):
        self.screen = screen
        self.lines = ['Find all 4 pillars to Escape, good luck!']

    def new_message(self, message):
        if len(message) > 45:
            raise ValueError('Message length cannot be longer than 45 characters')
        else:
            self.lines.insert(0, message)

        if len(self.lines) > 4: self.lines.pop()

    def message_box(self):
        size = (5, HALF_HEIGHT + 225, 280, 120)
        pygame.draw.rect(self.screen, GRAY, size)
        self.display_messages()
    
    def display_messages(self):
        index = 0
        txt_size = 20
        txt_color = BLACK
        y_offset = 30
        while index < len(self.lines):
            msg = self.lines[index]
            if index is 0: 
                txt_color = DARK_RED
            else:
                txt_color = BLACK
            txt, text_pos = create_textline(msg, 
                                            pos=(145, HALF_HEIGHT + 240 + y_offset * index),
                                            font_type='GUI/font/Vertigo.ttf', 
                                            size=txt_size,
                                            color=txt_color)
            self.screen.blit(txt, text_pos)                                            
            index += 1           

