from typing import NamedTuple, Optional, Union

import Model.Compass
from Model.Box import *


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
        super().__init__()
        self.__owner = owner
        self.__coords: Optional[Coords] = coords

    @property
    def owner(self):
        """
        Gets the cell owner
        :return: cell owner
        """
        return self.__owner

    @owner.setter
    def owner(self, val):
        """
        Sets the cell owner
        :param: value of the cell owner
        """
        self.__owner = val

    @property
    def coords(self):
        """
        Gets the cell coordinates
        :return: cell coordinates
        """
        return self.__coords

    @coords.setter
    def coords(self, val: Coordish):
        """
        Sets the cell coordinates
        :param: value of coordinates
        """
        self.__coords = Coords(*val)

    @property
    def xy(self):
        """Shorthand for coords getter."""
        return self.coords

    @xy.setter
    def xy(self, val: Coordish):
        """Shorthand for coords setter."""
        self.coords = val

    def neighbor(self, direction):
        """ Get neighboring room in specified direction from self room.
        :param direction: Direction of neighboring room wrt self room.
        :return: Neighboring room, if there is one; otherwise None.
        :exception: only raised for direction; attempting to fetch a hypothetical
        neighbor that would lie outside the grid returns None.
        """
        _dir = Compass.dir(direction)
        if _dir is None:
            raise ValueError(f"neighbor got invalid direction {direction}")
        _grid = self.grid
        if _grid is None:
            return None
        x = self.coord_x + _dir.vect_x
        y = self.coord_y + _dir.vect_y
        if not 0 <= x < _grid.width or not 0 <= y < _grid.height:
            # print(f"neighbor: room({self.coords}) {_dir.name} -!- ({x},{y}) outside grid")
            return None
        # print(f"neighbor: room({self.coords}) {_dir.name} --> ({x},{y})")
        return _grid.room(x, y)


if __name__ == '__main__':

    def example():
        cell1 = Cell()
        cell1.E = "juliet"
        cell1.W = "sundown"
        cell1.xy = (4, 5)
        print(f"Cell 1: {cell1}")

    example()

# END
