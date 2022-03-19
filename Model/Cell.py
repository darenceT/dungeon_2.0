from typing import Any, NamedTuple  # Optional, Union via Compass

from Model.Compass import *
from Model.Box import Box


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
    def owner(self) -> Any:
        """
        Gets the cell owner, this is the grid to which the cell belongs
        :return: cell owner
        """
        return self.__owner

    @owner.setter
    def owner(self, val) -> None:
        """
        Sets the cell owner (Grid to which the cell belongs)
        :param: value of the cell owner
        """
        self.__owner = val

    @property
    def grid(self) -> Any:
        """
        Alias for owner(). (DEPRECATED)
        :return: value of cell owner
        """
        return self.owner

    @property
    def coords(self) -> Optional[Coords]:
        """
        Gets the cell coordinates
        :return: cell coordinates
        """
        return self.__coords

    @coords.setter
    def coords(self, val: Coordish) -> None:
        """
        Sets the cell coordinates
        :param: value of coordinates
        """
        self.__coords = Coords(*val)

    @property
    def xy(self) -> Optional[Coords]:
        """Shorthand for coords getter."""
        return self.coords

    @xy.setter
    def xy(self, val: Coordish) -> None:
        """Shorthand for coords setter."""
        self.coords = val

    @property
    def coord_x(self) -> Optional[int]:
        """
        Returns X coordinate of room, if any (DEPRECATED)
        :return:
        """
        if self.coords is not None:
            return self.coords.x
        return None

    @property
    def coord_y(self) -> Optional[int]:
        """
        Returns Y coordinate of room, if any (DEPRECATED)
        :return:
        """
        if self.coords is not None:
            return self.coords.y
        return None

    def neighbor(self, direction) -> Any:
        """ Get neighboring room in specified direction from self room.
        :param direction: Direction of neighboring room wrt self room.
        :return: Neighboring room, if there is one; otherwise None.
        :exception: only raised for direction; attempting to fetch a hypothetical
        neighbor that would lie outside the grid returns None.
        """
        _dir = Compass.dir(direction)
        if _dir is None:
            raise ValueError(f"neighbor got invalid direction {direction}")
        nbr = self[_dir]
        return nbr


if __name__ == '__main__':

    def example():
        cell1 = Cell()
        cell1.E = "juliet"
        cell1.W = "sundown"
        cell1.xy = (4, 5)
        print(f"Cell 1: {cell1}")

    example()

# END
