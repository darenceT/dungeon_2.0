from Room import *

Coords = tuple[int, int]


class GridStr:
    """
    Builds the string of a 2 x 2 grid
    """
    __style_default = Room.styles.default

    @classmethod
    def set_style_default(cls, style: Room.styles.base):
        """
        Sets the default style for the grid
        :param style: Room styles
        :return:
        """
        cls.__style_default = style

    def __init__(self, grid, style=None):
        """
        Initializes the grid class, this underlays the maze
        :param grid:
        :param style:
        """
        self.style = self.__style_default
        if style is not None:
            self.style = style
        style = self.style  # just shorter to type
        self.lines = []
        for y in range(grid.height):
            # When starting new row, initialize each of row_lines to "".
            # But defer initialization until processing first room in row,
            # from which will then know how many lines.
            row_lines = []
            for x in range(grid.width):
                r = grid.room(x, y)
                rs = RoomStr(r, skip_north=y, skip_west=x, style=style)
                room_lines = rs.lines
                for i in range(len(room_lines)):
                    # New row, so initialize each of row_lines.
                    if len(row_lines) == i:
                        row_lines.append('')
                    row_lines[i] += room_lines[i]
            self.lines += row_lines

    def __str__(self):
        """
        Returns a string representation of the grid
        :return:
        """
        return "".join([f"{line}\n" for line in self.lines])


class Grid:

    @staticmethod
    def set_style_default(style):
        """
        Sets Grid Style
        :param style: style (Defined elsewhere)
        :return:
        """
        GridStr.set_style_default(style=style)

    def __init__(self, width=2, height=2, from_grid=None, from_coords: Coords = None):
        """
        Initializes Grid Class - 2 x 2 grid section within maze
        :param width: integer - number of cells across
        :param height: integer - number of cells down
        :param from_grid: value of last grid, if any
        :param from_coords: value of last coordinates, if any
        """
        from_x: int = 0
        from_y: int = 0
        if from_grid is not None and from_coords is None:
            raise ValueError(f"from_grid must be accompanied by from_coords")
        if from_coords is not None:
            if from_grid is None:
                raise ValueError(f"from_coords must be accompanied by from_grid")
            if not isinstance(from_coords[0], int) or not isinstance(from_coords[1], int):
                raise TypeError(f"from_coords must be tuple of int pair")
            from_x = from_coords[0]
            from_y = from_coords[1]
            if from_x + 1 > from_grid.width or from_y + 1 > from_grid.height:
                raise ValueError(f"subgrid would be South and/or East of from_grid")
            if from_x + width < 0 or from_y + height < 0:
                raise ValueError(f"subgrid would be North and/or West from_grid")

            # trim subgrid extent to what is inside parent
            if from_x < 0:
                width = width + from_x
                from_x = 0
            if from_x + width > from_grid.width:
                width = from_grid.width - from_x
            if from_y < 0:
                height = height + from_y
                from_y = 0
            if from_y + height > from_grid.height:
                height = from_grid.height - from_y

        self.__width = width
        self.__height = height
        self.__rooms = []
        for y in range(self.height):
            if from_grid is None:
                row = []
                self.__rooms.append(row)
                for x in range(self.width):
                    r = Room(grid=self, coords=(x, y))
                    row.append(r)
            else:
                # make a subgrid that refers to subset of rooms
                row = from_grid.rooms[from_y + y][from_x:from_x + width]
                self.__rooms.append(row)

    @property
    def width(self) -> int:
        """
        Returns width of grid
        :return:
        """
        return self.__width

    @property
    def height(self) -> int:
        """
        Returns height of grid
        :return:
        """
        return self.__height

    @property
    def rooms(self) -> list:
        """
        Returns a list of rooms contained within the grid
        :return:
        """
        return self.__rooms

    def room(self, x: int, y: int) -> Room:
        """
        TODO docs
        :param x:
        :param y:
        :return:
        """
        # If coords are out-of-bounds, just let resulting IndexError bubble up
        return self.__rooms[y][x]

    def str(self, *args, **kwargs) -> str:
        """
        Returns contents of string representation of grid
        :param args:arguments passed from other classes
        :param kwargs: keyword arguments passed from other classes
        :return:
        """
        return str(GridStr(self, *args, **kwargs))

    def __str__(self) -> str:
        """
        Returns string representation of grid
        :return:
        """
        return self.str()

    def __repr__(self) -> str:
        """
        Returns string representation of grid in a row
        :return:
        """
        return "".join([f"{row}\n" for row in self.__rooms])

    def empty(self):
        """
        TODO docs
        :return:
        """
        for y in range(self.height):
            for x in range(self.width):
                r = self.room(x, y)
                if y > 0:
                    r.add_door(North)
                if y + 1 < self.height:
                    r.add_door(South)
                if x > 0:
                    r.add_door(West)
                if x + 1 < self.width:
                    r.add_door(East)


if __name__ == '__main__':
    print(f"Greetings from Grid!\n")

    g = Grid()
    print(f"default grid is {g.width}x{g.height}:")
    print(f"{g}")

    GridStr.set_style_default(Room.styles.coords)
    g_w = 4
    g_h = 5
    print(f"parent {g_w}x{g_h} grid:")
    g1 = Grid(g_w, g_h)
    print(f"{g1}")
    g_w = 2
    g_h = 3
    g_x = 2
    g_y = 1
    print(f"...and {g_w}x{g_h} subgrid with origin at parent coords ({g_x},{g_y}):")
    g2 = Grid(g_w, g_h, from_grid=g1, from_coords=(g_x, g_y))
    print(f"{g2}")

    print(f"...and {g_w}x{g_h} subgrids, trimmed because overlap edges.")
    g_w = 3
    g_h = 3
    g_x = g1.width - 2
    g_y = g1.height - 2
    print("...trimmed to North:")
    g2 = Grid(g_w, g_h, from_grid=g1, from_coords=(1, -1))
    print(f"{g2}")
    print("...trimmed to South:")
    g2 = Grid(g_w, g_h, from_grid=g1, from_coords=(1, g_y))
    print(f"{g2}")
    print("...trimmed to East:")
    g2 = Grid(g_w, g_h, from_grid=g1, from_coords=(g_x, 1))
    print(f"{g2}")
    print(f"...trimmed to West:")
    g2 = Grid(g_w, g_h, from_grid=g1, from_coords=(-1, 1))
    print(f"{g2}")

    print("...and empty parent interior")
    g1.empty()
    print(f"{g1}")
    print("...and render with open-door style")
    print(f"{g1.str(style=Room.styles.open)}")

# END
