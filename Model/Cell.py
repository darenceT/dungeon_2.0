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
    def __init__(self):
        super().__init__()
        self.__coords: Optional[Coords] = None

    @property
    def xy(self):
        return self.__coords

    @xy.setter
    def xy(self, val: Coordish):
        self.__coords = Coords(*val)


if __name__ == '__main__':

    def example():
        cell1 = Cell()
        cell1.E = "juliet"
        cell1.W = "sundown"
        cell1.xy = (4, 5)
        print(f"Cell 1: {cell1}")

    example()

# END
