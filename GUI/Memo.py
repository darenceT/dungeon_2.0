import pygame
from .Settings import *
from .Utility import create_textline

class Memo:
    """
    Message box at bottom left corner, read-only. 
    """
    def __init__(self, screen):
        self.__screen = screen
        self.__lines = ['Find all 4 pillars to escape, good luck!']

    def new_message(self, message):
        """
        Allows other classes to deliver messages to this class for display
        :param message: said message
        :param type: str
        :return: None
        """
        if len(message) > 40:
            raise ValueError('Message length cannot be longer than 45 characters')
        else:
            self.__lines.insert(0, message)

        if len(self.__lines) > 4: self.__lines.pop()

    def message_box(self):
        """
        Create background for message box
        :return: None
        """
        size = (8, HALF_HEIGHT + 228, 276, 114)
        border = (5, HALF_HEIGHT + 225, 282, 120)
        pygame.draw.rect(self.__screen, BLACK, border)
        pygame.draw.rect(self.__screen, WHITE, size)
        self.__display_messages()
    
    def __display_messages(self):
        """
        Create GUI for text messages, roller-index formate.
        New message is slightly larger and red-colored, then 
        moves down as new message comes in. Older text becomes black.
        :return: None
        """
        index = 0
        y_offset = 30
        while index < len(self.__lines):
            txt_color = BLACK
            txt_size = 15
            msg = self.__lines[index]
            if index == 0: 
                txt_color = DARK_RED
                txt_size = 18
            txt, text_pos = create_textline(msg, 
                                            pos=(145, HALF_HEIGHT + 240 + y_offset * index),
                                            font_type='GUI/font/Titillium.ttf', 
                                            size=txt_size,
                                            color=txt_color)
            self.__screen.blit(txt, text_pos)                                            
            index += 1           

