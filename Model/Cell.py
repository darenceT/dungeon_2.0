from typing import Optional

from Util import *

Coords = tuple[int, int]


class Box():
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


class Cell(Box):
    """
    Represents the smallest unit of floor area.
    """
    def __init__(self):
        super().__init__()
        self.__coords: Optional[Coords] = None

    @property
    def xy(self):
        return self.__coords

    @xy.setter
    def xy(self, val: Coords):
        self.__coords = val


def example():
    box1 = Box()
    box1.E = "morning"
    box1.W = "wicked"
    box1.S = "tropics"
    box1.S = "arctic"
    print(f"Box 1: {box1}")

    cell1 = Cell()
    cell1.E = "juliet"
    cell1.W = "sundown"
    cell1.xy = (4, 5)
    print(f"Cell 1: {cell1}")


if __name__ == '__main__':
    example()

# END
