from typing import NamedTuple, Optional, Union

from Box import *


IntPair = tuple[int, int]

class Coords(NamedTuple):
    x: int
    y: int

Coordish = Union[IntPair, Coords]


class Cell(Box):
    """
    Represents the smallest unit of floor area.
    """
    def __init__(self, owner=None, coords: Optional[Coordish] = None):
        """TODO docs"""
        super().__init__()
        self.__owner = owner
        self.__coords: Optional[Coords] = coords

    @property
    def owner(self):
        """TODO docs"""
        return self.__owner

    @owner.setter
    def owner(self, val):
        """TODO docs"""
        self.__owner = val

    @property
    def coords(self):
        """TODO docs"""
        return self.__coords

    @coords.setter
    def coords(self, val: Coordish):
        """TODO docs"""
        self.__coords = Coords(*val)

    @property
    def xy(self):
        """Shorthand for coords getter."""
        return self.coords

    @xy.setter
    def xy(self, val: Coordish):
        """Shorthand for coords setter."""
        self.coords = val


if __name__ == '__main__':

    def example():
        cell1 = Cell()
        cell1.E = "juliet"
        cell1.W = "sundown"
        cell1.xy = (4, 5)
        print(f"Cell 1: {cell1}")

    example()

# END
