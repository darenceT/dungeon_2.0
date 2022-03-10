from typing import NamedTuple, Union

from Direction import *
from Cell import *
from Util import obj_repr


class Dimens(NamedTuple):
    width: int
    height: int

Dimenish = Union[IntPair, Dimens]

class Bounds(NamedTuple):
    orig: Coords
    size: Dimens


class Grid:
    """TODO docs"""
    def __init__(self, size: Dimenish, cell_type: type = Cell, _cells: Optional[list] = None,
                 ):
        """
        TODO docs

        Deprecaated params, only for transitioning from v1.0:
        width: integer - number of cells across
        height: integer - number of cells down
        from_grid: value of last grid, if any
        from_coords: value of last coordinates, if any
        """
        if not issubclass(cell_type, Cell):
            raise TypeError(f'cell_type must be subclass of Cell')
        self.__cell_type = cell_type
        self.__size: Dimens = Dimens(*size)

        # Aliasing a slice of an existing Grid instance cells
        if _cells:
            self.__cells = _cells
            return

        self.__cells = []
        w: int = self.__size.width
        h: int = self.__size.height
        cells: list = self.__cells
        factory: type = self.__cell_type
        for y in range(h):
            row = []
            for x in range(w):
                cell = factory(owner=self, coords=(x, y))
                row.append(cell)
            cells.append(row)

    @property
    def size(self) -> Optional[Dimens]:
        """
        Returns dimensions of grid
        :return namedtuple of width, height:
        """
        return self.__size

    @size.setter
    def size(self, val: Dimens) -> None:
        """
        Returns dimensions of grid
        :return namedtuple of width, height:
        """
        self.__size = Dimens(*val)

    @property
    def width(self) -> Optional[int]:
        """
        Returns width of grid
        :return:
        """
        if self.size is not None:
            return self.size.width

    @property
    def height(self) -> Optional[int]:
        """
        Returns height of grid
        :return:
        """
        if self.size is not None:
            return self.size.height

    def crop_copy(self, orig: Optional[Coordish] = None, size: Optional[Dimenish] = None):
        """Create a new Grid instance whose cells alias a slice of those in self.

        Important: The new Grid points to cells that are already pointed to by self.
        All cells retain links to the same neighbors as in the original; but any
        neighbor outside the crop extent will not be pointed to by the new Grid.

        :param orig: Coordinates of cell in original grid, that is origin in slice.
          This may lie outside the original grid; it will be adjusted as needed.
        :param size: Dimensions of slice.
          This may extend outside the original grid; it will be adjusted as needed.
        :returns: New Grid instance, whose cells alias a slice of those in self.
        """
        bounds: Bounds = self.crop_bounds(orig=orig, size=size)
        orig = bounds.orig
        size = bounds.size
        cells = []
        for y in range(size.height):
            row = self.__cells[orig.y + y][orig.x:orig.x + size.width]
            cells.append(row)
        grid = Grid(size, _cells=cells)
        return grid

    def crop_bounds(self, size: Dimenish, orig: Coordish) -> Bounds:
        """TODO docs"""
        # default, validate, convert
        if orig is None:
            orig = Coords(0, 0)
        elif not isinstance(orig[0], int) or not isinstance(orig[1], int):
            raise TypeError(f"orig must be tuple of int pair")
        else:
            orig = Coords(*orig)
            if orig.x + 1 > self.width or orig.y + 1 > self.height:
                raise IndexError(f"crop does not overlap")

        if size is None:
            size = self.size
        elif not isinstance(size[0], int) or not isinstance(size[1], int):
            raise TypeError(f"orig must be tuple of int pair")
        else:
            size = Dimens(*size)
            if orig.x + size.width < 0 or orig.y + self.height < 0:
                raise IndexError(f"crop does not overlap")

        # shrink to overlap
        x: int = orig.x
        y: int = orig.y
        w: int = size.width
        h: int = size.height
        if x < 0:
            w = w + x
            x = 0
        if x + w > self.width:
            w = self.width - x
        if y < 0:
            h = h + y
            y = 0
        if y + h > self.height:
            h = self.height - y
        return Bounds(orig=Coords(x=x, y=y), size=Dimens(width=w, height=h))

    def __repr__(self):
        return obj_repr(self)

"""
Deprecated v1 API
class Grid:
    @property
    rooms(self) -> list
    Replaced by _cells getter.
    
    room(self, x: int, y: int) -> Room
    If coords are out-of-bounds, just let resulting IndexError bubble up

    empty(self):
    Zap all the doors.
"""

if __name__ == '__main__':

    def example():
        print('parent grid...')
        g1 = Grid(size=Dimens(width=3, height=3))
        print(g1.size)
        print(g1)
        print('fully encompassed by parent...')
        g2 = g1.crop_copy(orig=Coords(x=1, y=0), size=(2, 2))
        print(g2.size)
        print(g2)
        print('extends beyond right side...')
        g2 = g1.crop_copy(orig=(2, 1), size=(2, 2))
        print(g2.size)
        print(g2)
        print('extends beyond bottom-right corner...')
        g2 = g1.crop_copy(orig=(2, 2), size=(2, 2))
        print(g2.size)
        print(g2)
        print('fully outside parent...?')
        try:
            g2 = g1.crop_copy(orig=(3, 0), size=(1, 2))
            print(g2)
        except IndexError as e:
            print(f'Nope! {e}')

    example()

    """
    def old_example():

        g = Grid()
        print(f"default grid is {g.width}x{g.height}:")
        print(f"{g}")

        GridStr.set_style_default(Room.styles.coords)
        w = 4
        h = 5
        print(f"parent {w}x{h} grid:")
        g1 = Grid(w, h)
        print(f"{g1}")
        w = 2
        h = 3
        x = 2
        y = 1
        print(f"...and {w}x{h} subgrid with origin at parent coords ({x},{y}):")
        g2 = Grid(w, h, from_grid=g1, from_coords=(x, y))
        print(f"{g2}")

        print(f"...and {w}x{h} subgrids, trimmed because overlap edges.")
        w = 3
        h = 3
        x = g1.width - 2
        y = g1.height - 2
        print("...trimmed to North:")
        g2 = Grid(w, h, from_grid=g1, from_coords=(1, -1))
        print(f"{g2}")
        print("...trimmed to South:")
        g2 = Grid(w, h, from_grid=g1, from_coords=(1, y))
        print(f"{g2}")
        print("...trimmed to East:")
        g2 = Grid(w, h, from_grid=g1, from_coords=(x, 1))
        print(f"{g2}")
        print(f"...trimmed to West:")
        g2 = Grid(w, h, from_grid=g1, from_coords=(-1, 1))
        print(f"{g2}")

        print("...and empty parent interior")
        g1.empty()
        print(f"{g1}")
        print("...and render with open-door style")
        print(f"{g1.str(style=Room.styles.open)}")
    """

# END
