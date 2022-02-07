# from typing import Any
from random import randrange
from time import sleep

# from Compass import *
from Room import *
from Grid import Grid

Coords = tuple[int, int]


class Maze(Grid):
    """
    Class that assembles and generates maze
    """

    def __init__(self,
                 width: int = 4, height: int = 4,
                 map_str: str = None,
                 debug: bool = False) -> None:
        """
        Initializes maze class
        :param width: number of cells across
        :param height: number of cells down
        :param map_str: string representation of map
        :param debug: boolean to trigger debugging mode
        """
        if map_str is not None:
            width, height = Maze.parse_map(map_str=map_str, debug=debug)

        super().__init__(width=width, height=height)

        self.__ingress: Optional[Room] = None   # entrance
        self.__egress: Optional[Room] = None    # exit

        if map_str is not None:
            self.load_map(map_str=map_str, debug=debug)
        else:
            self.empty()
            self.generate()

    @property
    def ingress(self) -> Optional[Room]:
        """
        returns entry point
        :return:
        """
        return self.__ingress

    @ingress.setter
    def ingress(self, room: Room) -> None:
        """
        Sets entry point as room
        :param room: Instance of Room
        :return:
        """
        self.__ingress = room

    @property
    def egress(self) -> Optional[Room]:
        """
        Returns exit point
        :return:
        """
        return self.__egress

    @egress.setter
    def egress(self, room: Room) -> None:
        """
        Sets exit point as room
        :param room: instance of Room
        :return:
        """
        self.__egress = room

    def load_map(self, **kwargs):
        """
        Loads map of maze
        :param kwargs: keyword arguments
        :return:
        """
        Maze.parse_map(grid=self, **kwargs)
        for row in self.rooms:
            for room in row:
                if room.is_entrance:
                    self.ingress = room
                if room.is_exit:
                    self.egress = room

    @staticmethod
    def parse_map(map_str: str = None, grid=None,
                  style: RoomStyle = Room.styles.default,
                  debug=False):
        """ Parse string containing specification for map.
        Operates in one of two modes, depending upon whether grid is provided:

        - grid is None - measure-only mode:
          Returns dimensions necessary for a grid that can contain the map.
          This is a quick estimate that assumes properly formatted input.

        - grid present - full-load mode:
          Fully parses map, populating the grid as specified in the map.
          Non-static method load_map() is a thin wrapper for this mode,
          since Maze is a Grid subclass.

        Map format is identical to output format, except mixed-item 'M'
        marker is replaced with multi-character list of markers for items,
        with repetition where there are multiple of same item type,
        e.g. "HHV" represents 2 health potions + 1 vision potion.

        For measure-only mode, there is no validation of walls, doors, or
        room contents, other than having expected width.

        :param map_str: String containing specification for map.
        :param grid: Grid of rooms of sufficient size to hold map.
            If None, function instead operates in measure-only mode.
        :param style: Map rendering style in which map is formatted.
        :param debug: Whether to print debug info while parsing.
            For troubleshooting mistakes in str_map (and/or bugs in parsing)
        :return: In measure-only mode, returns a pair of ints representing
            width and height, respectively, of necessary grid dimensions.
            In full-load mode, returns None.
        :exception ValueError, if map appears improperly formatted.
        """
        wall_len: int = len(style.wall_n)
        line_len: int = 0

        in_grid: bool = False
        south_edge: bool = False

        num_rows: int = 0
        # num_cols: int = 0
        grid_row: int = 0
        want_lat: bool = True

        line_num: int = 0  # 1-indexed, unlike everything else
        char_num = 0

        def dbg_parse(*args, **kwargs):
            """ Nested utility function. """
            if debug:
                print(f"L{line_num}C{char_num}: ", *args, **kwargs)

        lines = map_str.splitlines()
        for line in lines:
            line_num += 1
            line = line.rstrip()
            dbg_parse(f"line '{line}'")

            # skip header comment/whitespace lines
            if not in_grid and (len(line) == 0 or line.startswith('#')):
                continue

            # one-time work upon first entering grid
            if not in_grid:
                in_grid = True

                # Initial dimensions assessment, before grid has been created.
                # Do quick math sanity-check, conversion to grid dimensions.
                # Parses only first line of grid, then returns result.
                if grid is None:
                    if len(line) % (wall_len+1) != 1:
                        raise ValueError(f"L{line_num}: expected line len of form {wall_len+1}*N+1, got {len(line)}")
                    num_cols = (len(line)-1)//(wall_len+1)
                    if (len(lines)-line_num) % 2 != 0:
                        raise ValueError(f"expected line count 2*N+1, got {len(lines)-line_num}")
                    num_rows = (len(lines)-line_num)//2
                    dbg_parse(f"estimated grid dims={num_cols}x{num_rows}")
                    return num_cols, num_rows
                    # All done! Only estimating dimensions.
                    # TODO could optionally do fuller validation that grid looks legit

                else:
                    num_cols = grid.width
                    num_rows = grid.height
                    line_len = num_cols * (wall_len + 1) + 1
                    dbg_parse(f"grid dims={num_cols}x{num_rows} line_len={line_len}")

            dbg_parse(f"line len {len(line)}")
            # sanity check, for errant line unexpectedly longer than first line
            if len(line) != line_len:
                raise ValueError(f"L{line_num}: does not match expected len_len {line_len}")
            dbg_parse(f"want_lat={want_lat}")

            # walk the line
            char_num = 0
            grid_col: int = 0
            east_edge: bool = False
            r = None  # current room
            while char_num < len(line):
                dbg_parse(f"room ({grid_col},{grid_row})")

                # last char in line
                if char_num + 1 >= len(line):
                    dbg_parse(f"last char in line")
                    east_edge = True

                # on or aligned with a vertical wall, which is either:
                # west side of room contents that follows
                # OR east side of room contents just parsed
                dbg_parse(f"grid col {grid_col}")
                c = line[char_num]
                if want_lat:
                    if c != style.corner:
                        raise ValueError(f"L{line_num}C{char_num}: expected corner '{style.corner}', got '{c}'")
                    dbg_parse(f"corner")
                else:
                    if c != style.wall_w and c != style.door_w:
                        raise ValueError(f"L{line_num}C{char_num}: expected wall '{style.wall_w}'" +
                                         f" or door '{style.door_w}', got '{c}'")
                    dbg_parse(f"East-West room side")
                if east_edge:
                    if not want_lat and r:
                        # completing room from previous round
                        if c == style.door_e:
                            r.add_door(East)
                    break  # from "walk the line" loop

                dbg_parse(f"get room...")
                r = grid.room(grid_col, grid_row)

                if not want_lat:
                    if r and c == style.door_w:
                        r.add_door(West)

                char_num += 1

                # between vertical walls
                if want_lat:
                    # horizontal wall/door
                    wall = line[char_num:char_num+wall_len]
                    if wall != style.wall_n and wall != style.door_n:
                        raise ValueError(f"L{line_num}C{char_num}: expected north wall '{style.wall_n}'" +
                                         f" or door '{style.door_n}', but got '{wall}'")
                    dbg_parse(f"North-South room side")
                    if r:
                        if south_edge:
                            if wall == style.door_s:
                                r.add_door(South)
                        elif wall == style.door_n:
                            r.add_door(North)
                else:
                    contents = line[char_num:char_num+wall_len].strip()
                    dbg_parse(f"contents: {contents}")
                    for c in contents:
                        if c == 'i':
                            r.is_entrance = True
                        elif c == 'O':
                            r.is_exit = True
                        elif c == 'X':
                            r.has_pit = True
                        elif c == 'H':
                            r.healing_potions += 1
                        elif c == 'V':
                            r.vision_potions += 1
                        elif c in Room.pillars:
                            r.pillar = c
                        else:
                            raise ValueError(f"{c} in room {r.coords} not recognized")
                char_num += wall_len

                if not east_edge:
                    grid_col += 1
                    dbg_parse(f"next up: grid_col {grid_col} west edge")
                else:
                    dbg_parse(f"next up: grid_row {grid_row} east edge")

            dbg_parse(f"prep for next line...")

            # if last line, then completing room on bottom row
            if line_num == len(lines):
                dbg_parse(f"final wall completed")
                break

            # prep for next line
            # if got content line, increment in row_num for next row...
            # unless on last row, in which case next line is final line,
            # handled as south wall of final row and south edge of grid.
            if not want_lat:
                if grid_row + 1 < num_rows:
                    grid_row += 1
                else:
                    south_edge = True
                    dbg_parse(f"next up: row {grid_row} south edge")
            want_lat = not want_lat
            dbg_parse(f"next up: row {grid_row} want_lat={want_lat}")

    @staticmethod
    def __clear_screen():
        """
        Clears the screen
        :return:
        """
        print("clear screen...")
        print('\033c', end='')

    def __rec_div(self, origin: Coords = None, dimens: Coords = None,
                  debug: bool = False, animate: bool = False) -> None:
        """ One round of recursive division.
        :param origin: coordinates of origin
        :param dimens: dimensions
        :return: None
        """
        def __dbg_print(*args, **kwargs):
            if debug:
                print(*args, **kwargs)

        if debug and animate:
            sleep(1)
            Maze.__clear_screen()
            __dbg_print(f"{self}")

        __dbg_print(f"origin:{str(origin):10} dimens:{str(dimens):10}")
        (x, y) = origin
        (w, h) = dimens
        if w == 1 or h == 1:
            __dbg_print("no-op")
            return
        w_mid = randrange(1, w)
        h_mid = randrange(1, h)
        if w > h:
            # split into W/E parts
            __dbg_print(f"split into W/E parts at {x+w_mid}")
            for y_i in range(y, y+h):
                if y_i == y+h_mid:
                    continue
                r = self.room(x+w_mid-1, y_i)
                r.add_wall(East)
            # recurse into both parts
            self.__rec_div(origin=(x, y), dimens=(w_mid, h),
                           debug=debug, animate=animate)
            self.__rec_div(origin=(x+w_mid, y), dimens=(w-w_mid, h),
                           debug=debug, animate=animate)
        else:
            # split into N/S parts
            __dbg_print(f"split into N/S parts at {y+h_mid}")
            for x_i in range(x, x+w):
                if x_i == x+w_mid:
                    continue
                r = self.room(x_i, y+h_mid-1)
                r.add_wall(South)
            # recurse into both parts
            self.__rec_div(origin=(x, y), dimens=(w, h_mid),
                           debug=debug, animate=animate)
            self.__rec_div(origin=(x, y+h_mid), dimens=(w, h-h_mid),
                           debug=debug, animate=animate)

    def generate_rec_div(self, *args, **kwargs):
        """ Generate maze via Recursive Division algorithm.
        :return: None
        """
        self.__rec_div((0, 0), (self.width, self.height), *args, **kwargs)

        # Set ingress and egress.
        # Since this algo produces result wherein every cell is guaranteed reachable,
        # can just pick random cells on the outer grid edge as ingress and egress.
        # To easily avoid cells that are too close, select from opposite grid edges.
        if randrange(2) % 1:
            self.ingress = self.room(randrange(self.width), 0)
            self.egress = self.room(randrange(self.width), self.height-1)
        else:
            self.ingress = self.room(0, randrange(self.height))
            self.egress = self.room(self.height-1, randrange(self.height))

    def generate(self, *args, **kwargs):
        """ Generate maze.
        For now, only has one algorithm. But could implement more...
        :return: None
        """
        self.generate_rec_div(*args, **kwargs)
        self.ingress.is_entrance = True
        self.egress.is_exit = True

    def can_move(self, from_room: Room, direction: CompassDirection) -> tuple[bool, Optional[Room]]:
        """
        Determine if room has door in direction
        :param from_room: instance of Room that you are moving from
        :param direction: Direction in which you are moving
        :return:
        """
        # print(f"can_move from_room...\n{from_room}")
        if not from_room.has_door(direction):
            return False, None
        next_room = from_room.neighbor(direction)
        if next_room is None:
            return True, None
        return True, next_room


if __name__ == '__main__':
    print("Greetings from Maze!\n")

    # Default 4x4 grid, no doors yet
    g_m = Maze()
    print(f"default maze is {g_m.width}x{g_m.height}:")
    print(g_m)

    # Measure canned
    print(f"canned dungeon:")
    g_map_str = """
# This is my dungeon
+-----+-----+-----+
| i   |     =     |
+--H--+--H--+--H--+
|     =     | O   |
+-----+-----+-----+
""".lstrip()
    print(g_map_str)
    g_width, g_height = Maze.parse_map(map_str=g_map_str)
    print(f"measure-only estimates as {g_width}x{g_height}\n")

    # Full init from canned maze
    print(f"another canned dungeon:")
    g_map_str = """
# This is my other dungeon
+-----+-----+-----+
| i   |     = O   |
+--H--+--H--+-----+
| P   = XV  = HH  |
+-----+-----+-----+
""".lstrip()
    print(g_map_str)
    print(f"...now do full load:")
    g_m = Maze(map_str=g_map_str)
    print(f"...reports dimensions {g_m.width}x{g_m.height}")
    print(f"...and re-render:")
    print(f"{g_m}")

    # Generate with Recursive Division algo
    Grid.set_style_default(Room.styles.open)
    g_m = Maze(width=7, height=7)
    g_m.empty()
    print(f"start from empty grid {g_m.width}x{g_m.height}:")
    print(g_m)
    print(f"...generate maze with Recursive Division algo:")
    g_m.generate_rec_div(debug=False, animate=False)
    print(g_m)

# END
