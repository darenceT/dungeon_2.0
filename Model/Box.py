# from Direction import *
from Util import *


class Box:
    """
    The four boundaries of a square.
    """
    def __init__(self):
        super().__init__()
        self.__north = None
        self.__east = None
        self.__south = None
        self.__west = None

    @property
    def N(self):
        return self.__north

    @N.setter
    def N(self, val):
        self.__north = val

    @property
    def E(self):
        return self.__east

    @E.setter
    def E(self, val):
        self.__east = val

    @property
    def S(self):
        return self.__south

    @S.setter
    def S(self, val):
        self.__south = val

    @property
    def W(self):
        return self.__west

    @W.setter
    def W(self, val):
        self.__west = val

    def __repr__(self):
        return obj_repr(self)


if __name__ == '__main__':

    def example():
        box1 = Box()
        box1.E = "morning"
        box1.W = "wicked"
        box1.S = "tropics"
        box1.S = "arctic"
        print(f"Box 1: {box1}")

    example()

# END
