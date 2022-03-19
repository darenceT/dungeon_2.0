# from version 1.0. This will be retired, new version in Model
from typing import Optional
from Model.Compass import *

Coords = tuple[int, int]


class RoomStyle:
    """
    Sets up the display style of individual rooms
    """
    def __init__(self, corner: str = "+",
                 wall_n: str = "-----", wall_s: str = None,
                 door_n: str = "--H--", door_s: str = None,
                 wall_w: str = "|", wall_e: str = None,
                 door_w: str = "=", door_e: str = None,
                 veiled: bool = False,
                 coords: bool = False,
                 crumbs: bool = False,
                 heroin: bool = True,
                 ):
        """
        :param corner: "+" indicating a room corner
        :param wall_n: Series of dashes indicating a north wall
        :param wall_s: No value - no walls needed to the South for individual rooms
        :param door_n: "--H--" indicating a north door
        :param door_s: No value - no doors needed to the South for individual rooms
        :param wall_w: "|" indicating a West wall
        :param wall_e: No value - no walls needed to the East for individual rooms
        :param door_w: "=" indicating a West door
        :param door_e: No value, no doors needed to the East for individual rooms
        :param veiled: A boolean indicating to show only visited/seen rooms
        :param coords: A boolean indicating to show room coordinates, not contents
        :param crumbs: A boolean indicating whether or not room has been visited
        :param heroin: A boolean indicating if the hero is in the current room
        """
        self.corner = corner
        # N/S walls
        self.wall_n = wall_n
        if wall_s:
            self.wall_s = wall_s
        else:
            self.wall_s = self.wall_n
        # N/S doors
        self.door_n = door_n
        if door_s:
            self.door_s = door_s
        else:
            self.door_s = self.door_n
        # W/E walls
        self.wall_w = wall_w
        if wall_e:
            self.wall_e = wall_e
        else:
            self.wall_e = self.wall_w
        # W/E doors
        self.door_w = door_w
        if door_e:
            self.door_e = door_e
        else:
            self.door_e = self.door_w

        # Show coords instead of contents
        if self.wall_len >= 4:
            self.coords = coords
        else:
            self.coords = False

        # Show only rooms with crumb
        self.veiled = veiled
        # Extra mark if hero present or, if not (or option disabled),
        # whether hero has visited/seen room
        if self.wall_len >= 2:
            # Hero in now
            self.heroin = heroin
            self.crumbs = crumbs
        else:
            self.heroin = False
            self.crumbs = False

    @property
    def wall_len(self) -> int:
        """
        Gets the length of the North wall
        :return:
        """
        return len(self.wall_n)


class RoomStyles:
    """
    TODO docs
    """
    base = RoomStyle()
    open = RoomStyle(door_n="     ", door_w=" ")
    coords = RoomStyle(coords=True)
    tom = RoomStyle(corner="*",
                    wall_n="*****", wall_w="*",
                    door_n=" --- ", door_w="|")
    tracker = RoomStyle(heroin=True, crumbs=True)
    veiled = RoomStyle(heroin=True, veiled=True)
    default = base


class RoomStr:
    """
    Builds a ASCII-text representation of room.
    Boundaries are single char wide, with wall and door represented differently.
    In center, single char that represents what the room contains.
    M - Mix of Items
    X - Pit
    i - Entrance (In)
    O - Exit (Out)
    V - Vision Potion
    H - Healing Potion
    <space> - Empty Room
    A, E, I, P - Pillars

    Additional markers, separate from contents. Only shown in some styles.
    . - Breadcrumb, i.e. room has been visited/seen
    @ - Adventurer themselves

    Rendering style is somewhat configurable, with several canned styles being
    available via Room.styles.* elements. See class RoomStyle for more details.

    Example:  Room at coordinates (1,1) with one of the Pillars and doors to
    East and South, in several styles:

    Default:
    +-----+
    | P.  =
    +--H--+

    Coords (Default with coordinates instead of contents):
    +-----+
    | 1,1 =
    +--H--+

    Tom:
    *******
    * P   |
    * --- *

    Open (Default with blanks instead of doors):
    +-----+
    | P    <--(blank padded East boundary, including doorway)
    +     +
    """

    def __init__(self, _room, skip_north=None, skip_west=None, style=RoomStyles.default):
        """
        Initializes RoomStr
        :param _room: the current room
        :param skip_north: boolean indicating whether or not to skip North wall
        :param skip_west: booolean indicating whether or not to skip West wall
        :param style: The style of room to use
        """
        self.room = _room
        self.lines = []
        skip_north = bool(skip_north)
        skip_west = bool(skip_west)

        # top
        if not skip_north:
            line = ""
            if not skip_west:
                line += style.corner
            if _room.has_door(North):
                line += style.door_n
            else:
                line += style.wall_n
            line += style.corner
            self.lines.append(line)

        # west side
        line = ""
        if not skip_west:
            if _room.has_door(West):
                line += style.door_w
            else:
                line += style.wall_w

        # center: contents and/or attributes
        if style.veiled and not _room.has_crumb:
            if style.wall_len < 3:
                center = ''
            else:
                center = '?' * style.wall_len
        else:
            if style.coords:
                # NOTE no attempt made to deal len(room_coords) > style.wall_len
                center = self.room_coords()
            else:
                center = self.room_contents()
            # additional indicators
            if style.heroin and _room.has_hero:
                center += '@'
            elif style.crumbs and _room.has_crumb:
                center += '.'
        # If style wide enough, pad with one blankspace on either side.
        # If only space for padding on one side, then pad left only.
        if style.wall_len >= 3:
            if len(center) + 1 <= style.wall_len:
                center = ' ' + center
        # Pad right, to reach fixed-width center
        if len(center) + 1 <= style.wall_len:
            pad = ' ' * (style.wall_len - len(center))
            center += pad
        line += center

        # east side
        if style.veiled and self.is_veiled_e(_room):
            line += '?'
        elif _room.has_door(East):
            line += style.door_e
        else:
            line += style.wall_e
        self.lines.append(line)

        # bottom
        line = ""
        if not skip_west:
            line += style.corner
        if style.veiled and self.is_veiled_s(_room):
            line += '?' * style.wall_len
        elif _room.has_door(South):
            line += style.door_s
        else:
            line += style.wall_s
        line += style.corner
        self.lines.append(line)

    @staticmethod
    def is_veiled_s(room) -> bool:
        _r2 = room.neighbor(South)
        if _r2 is None:
            return False
        if room.has_crumb:
            return False
        if _r2.has_crumb:
            return False
        return True

    @staticmethod
    def is_veiled_e(room) -> bool:
        _r2 = room.neighbor(East)
        if _r2 is None:
            return False
        if room.has_crumb:
            return False
        if _r2.has_crumb:
            return False
        return True

    # reporting only coords, rather than contents, is useful for testing
    def room_coords(self) -> str:
        """
        If the room has coordinates, return the current room coordinates. If not return default string.
        :return:
        """
        _r = self.room
        if _r.coords is not None:
            return f"{_r.coord_x},{_r.coord_y}"
        else:
            return "#,#"

    def room_contents(self) -> str:
        """
        Sets the strings to display to indicate contents of current room.
        :return:
        """
        _r = self.room
        if _r.has_mixed_contents:
            return 'M'
        elif _r.is_entrance:
            return 'i'
        elif _r.is_exit:
            return 'O'
        elif _r.has_pit:
            return 'X'
        elif _r.vision_potions:
            return 'V'
        elif _r.healing_potions:
            return 'H'
        elif _r.pillar:
            return _r.pillar
        else:
            return ''

    def __str__(self):
        """
        Returns the string representation of a room
        :return:
        """
        return "".join([f"{line}\n" for line in self.lines])


class Room:
    """
    A room in the Dungeon. May have:
    - (0/1) Entrance - only one room is an entrance, and that room contains NOTHING else
    - (0/1) Exit - only one room is an exit, and that room contains NOTHING else
    - (0/1) Pillar of OO - one of four unique Pillars of Object Oriented Programming
    - (0-4) Doors - N, S, E, W
    - (0+) Healing Potion - restore some lost hit points
    - (0+) Vision Potion - can be used to allow user to see eight rooms surrounding
      current room as well as current room (if on maze edge, less than 8)
    """
    styles = RoomStyles
    pillars = {
        'A': 'Abstraction',
        'E': 'Encapsulation',
        'I': 'Inheritance',
        'P': 'Polymorphism',
    }

    def __init__(self, grid=None, coords: Coords = None,
                 is_entrance: bool = False,
                 is_exit: bool = False,
                 doors_mask: int = 0,
                 doors_list: list = None,
                 has_pit: bool = False,
                 healing_potions: int = 0,
                 vision_potions: int = 0,
                 pillar: str = None,
                 has_crumb: bool = None,
                 has_hero: bool = None,
                 ) -> None:
        """
        :param grid: from grid class
        :param coords: X, Y coordinates of room
        :param is_entrance: boolean, indicates if the room is the map entrance
        :param is_exit: boolean, indicates if the room is the map exit
        :param doors_mask: indicates if the room has a door
        :param doors_list: list of doors in the current room
        :param has_pit: boolean, indicates if the room has a pit
        :param healing_potions: number of healing potions
        :param vision_potions: number of vision potions
        :param pillar: string, one of set of pillars
        :param has_crumb: boolean, indicates if room has been visited
        :param has_hero: boolean, indicates if hero is present
        """
        self.__grid = grid
        self.__coords: Coords = coords
        self.__is_entrance: bool = is_entrance
        self.__is_exit: bool = is_exit
        self.__has_pit: bool = has_pit
        self.__healing_potions: int = healing_potions
        self.__vision_potions: int = vision_potions
        self.__pillar: str = pillar
        self.__doors_mask: int = 0
        if doors_mask and doors_list:
            raise ValueError("init Room with doors_mask or doors_list, not both")
        elif doors_list and not doors_mask:
            self.__doors_mask = Compass.dirs2mask(doors_list)
        else:
            self.__doors_mask = doors_mask
        self.__has_crumb: bool = has_crumb
        self.__has_hero: bool = has_hero
        self.__occupants = []

    @property
    def occupants(self):
        return self.__occupants
    
    @occupants.setter
    def occupants(self, info):
        # TODO: add check for monster class type else error
        npc, add = info
        if npc is not None:
            if add:
                self.__occupants.append(npc) 
            else:
                self.__occupants.remove(npc)
    
    @property
    def grid(self):
        """
        Gets the current grid
        :return:
        """
        return self.__grid

    @property
    def coords(self) -> Optional[Coords]:
        """ Get coordinates of room within grid, assuming part of one.
            Returned value is a tuple of ints (x,y) in a Cartesian system.
            x-coord runs West-to-East (rightward), most Westward column at x=0.
            y-coord runs North-to-South (downward), most Northward row at y=0. """
        return self.__coords

    @property
    def coord_x(self) -> Optional[int]:
        """
        Returns X coordinate of room, if any
        :return:
        """
        if self.coords is not None:
            return self.coords[0]
        return None

    @property
    def coord_y(self) -> Optional[int]:
        """
        Returns Y coordinate of room, if any
        :return:
        """
        if self.coords is not None:
            return self.coords[1]
        return None

    @coords.setter
    def coords(self, coords: Coords) -> None:
        """ Set coordinates of room within grid, assuming part of one.
            Same tuple format as returned by getter. """
        if not isinstance(coords, tuple) or len(coords) != 2 or \
                not isinstance(coords[0], int) or \
                not isinstance(coords[1], int):
            raise TypeError(f"expected coords to be tuple of two ints")
        if coords[0] < 0 or coords[1] < 0:
            raise ValueError(f"expected coords to both be zero or greater")
        g = self.grid
        if g is not None and (coords[0] >= g.width or coords[1] >= g.height):
            raise ValueError(f"expected coords within grid bounds ({g.width}x{g.height})")
        self.__coords = coords

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

    @property
    def doors_mask(self) -> int:
        """
        Returns number of doors in room
        :return:
        """
        return self.__doors_mask

    # TODO merge doors setters into single method that accepts all formats
    @doors_mask.setter
    def doors_mask(self, doors_mask: int) -> None:
        """
        Sets doors mask
        :param doors_mask: number of doors in room
        :return:
        """
        self.__doors_mask = doors_mask

    @property
    def doors(self) -> list:
        """
        Returns a list of doors by direction
        :return:
        """
        return Compass.mask2dirs(self.__doors_mask)

    # @doors.setter
    # def doors(self, doors_list: list) -> None:
    #     self.__doors_mask = # TODO

    @property
    def doors_str(self) -> str:
        """
        Returns string representation of doors
        :return:
        """
        return ','.join([d.name[0] for d in self.doors])

    # TODO
    # @doors_str.setter
    # def doors_str(self, doors_str: str) -> None:
    #     self.__doors_mask = .....

    def has_door(self, direction) -> bool:
        """
        Checks to see if room has door in a given direction, if so returns true
        :param direction:
        :return:
        """
        return bool(self.__doors_mask & Compass.dir(direction).mask)

    def add_door(self, direction) -> None:
        """ Add a door in specified direction from self room, and likewise
        from corresponding neighboring room, if one exists in that direction.

        Since doors are represented within rooms via bitmask, rather than
        a ref to neighboring room; thus when a door connects two rooms,
        each room must have that door marked in its respective bitmask.

        Allowed to add a door that leads outside the grid, i.e. no neighboring
        room exists in that direction; though depending upon the context,
        perhaps not what you want.

        :param direction: Outward direction from room
        :return None
        :exception ValueError if direction is not recognized
        """
        _d = Compass.dir(direction)
        # print(f"add_door: > room({self.coords}) {_d.name}")
        self.__doors_mask |= _d.mask
        _r = self.neighbor(direction)
        if _r is not None:
            _d = _d.opposite
            # print(f"add_door: < room({_r.coords}) {_d.name}")
            _r.doors_mask |= _d.mask

    def del_door(self, direction) -> None:
        """ Remove door (if any) in specified direction from self room, and likewise
        from corresponding neighboring room, if one exists in that direction.
        Exact opposite of add_door().

        :param direction: Outward direction from room
        :return None
        :exception ValueError if direction is not recognized
        """
        _d = Compass.dir(direction)
        # print(f"del_door: > room({self.coords}) {_d.name}")
        self.__doors_mask &= ~_d.mask
        _r = self.neighbor(direction)
        if _r is not None:
            _d = _d.opposite
            # print(f"del_door: < room({_r.coords}) {_d.name}")
            _r.doors_mask &= ~_d.mask

    def add_wall(self, direction) -> None:
        """
        Deletes a door leaving a wall
        :param direction:
        :return:
        """
        self.del_door(direction)

    def del_wall(self, direction) -> None:
        """
        Deletes a wall adding a door
        :param direction:
        :return:
        """
        self.add_door(direction)

    @property
    def is_entrance(self) -> bool:
        """
        Returns true if there is an entrance in the room
        :return:
        """
        return self.__is_entrance

    @is_entrance.setter
    def is_entrance(self, val: bool) -> None:
        """
        Sets the boolean value for whether or not there is an entrance.
        :param val:
        :return:
        """
        self.__is_entrance = val

    @property
    def is_exit(self) -> bool:
        """
        Returns true if the room is the exit
        :return:
        """
        return self.__is_exit

    @is_exit.setter
    def is_exit(self, val: bool) -> None:
        """
        Sets the boolean value for whether or not the room has an exit
        :param val: True or False
        :return:
        """
        self.__is_exit = val

    @property
    def has_pit(self) -> bool:
        """
        Returns true if the room contains a pit
        :return:
        """
        return self.__has_pit

    @has_pit.setter
    def has_pit(self, val: bool) -> None:
        """
        Sets the boolean value for whether or not the room contains a pit
        :param val: True or False
        :return:
        """
        self.__has_pit = val

    @property
    def healing_potions(self) -> int:
        """
        Returns the number of healing potions contained within the room
        :return:
        """
        return self.__healing_potions

    @healing_potions.setter
    def healing_potions(self, val: int) -> None:
        """
        Sets the number of healing potions contained within the room
        :param val: Integer - number of healing potions (0 or 1)
        :return:
        """
        self.__healing_potions = val

    @property
    def vision_potions(self) -> int:
        """
        Returns the number of vision potions contained within the room
        :return:
        """
        return self.__vision_potions

    @vision_potions.setter
    def vision_potions(self, val: int) -> None:
        """
        Sets the number of vision potions contained within the room
        :param val: integer - number of healing potions (0 or 1)
        :return:
        """
        self.__vision_potions = val

    @property
    def pillar(self) -> str:
        """
        Returns the value of any pillar contained within the room
        :return:
        """
        return self.__pillar

    @pillar.setter
    def pillar(self, val: str) -> None:
        """
        Sets the value of any pillar contained in the room
        :param val: String, one of a set of pillars
        :return:
        """
        if val == '':
            self.__pillar = None
        else:
            self.__pillar = val

    @property
    def has_crumb(self) -> bool:
        """
        Returns the boolean value for whether or not the room has been visited
        :return:
        """
        return self.__has_crumb

    @has_crumb.setter
    def has_crumb(self, val: bool) -> None:
        """
        Sets the boolean value for whether or not the room has been visited
        :param val: True or False
        :return:
        """
        self.__has_crumb = val

    @property
    def has_hero(self) -> bool:
        """
        Returns the boolean value for whether or not the hero is in the room
        :return:
        """
        return self.__has_hero

    @has_hero.setter
    def has_hero(self, val: bool) -> None:
        """
        Sets the boolean value for whether or not the hero is in the room
        :param val: True or False
        :return:
        """
        self.__has_hero = val

    @property
    def is_empty(self) -> bool:
        """
        TODO docs
        :return:
        """
        if self.has_pit or self.vision_potions or self.healing_potions or self.pillar:
            return False
        return True

    @property
    def has_mixed_contents(self) -> bool:
        """
        Returns a boolean value for whether or not the room contains more than one thing
        :return:
        """
        count: int = 0
        if self.vision_potions > 0:
            count += 1
        if self.healing_potions > 0:
            count += 1
        if self.has_pit:
            count += 1
        if self.pillar is not None:
            count += 1
        return count > 1

    def describe(self):
        """
        Returns a description of what is in the room
        :return:
        """
        return ''.join([f"{line}\n" for line in [
            f"Coords:  {self.coords}",
            f"Doors:   {self.doors_str}",
            f"Pit:     {self.has_pit}",
            f"Healing: {self.healing_potions}",
            f"Vision:  {self.vision_potions}",
            f"Pillar:  {self.pillar}",
        ]])

    def str(self, *args, **kwargs) -> str:
        """
        Returns the arguments to be contained in the string representation of the room
        :param args:
        :param kwargs:
        :return:
        """
        return str(RoomStr(self, *args, **kwargs))

    def __str__(self) -> str:
        """
        Returns the string representation of the room
        :return:
        """
        return self.str()

    def __repr__(self) -> str:
        """
        Returns the string representation of the room at the current coordinates
        :return:
        """
        return RoomStr(self).room_coords()


if __name__ == '__main__':
    print(f"Greetings from Room!\n")

    print(f"standalone room, empty and sealed:")
    g_r = Room()
    print(f"{g_r}")
    print(f"...with coords-style contents, but hey no coords:")
    print(f"{g_r.str(style=Room.styles.coords)}")

    print(f"grid room, empty and sealed:")
    g_r = Room(coords=(2, 3))
    print(f"{g_r}")
    print(f"...with coords-style contents:")
    print(f"{g_r.str(style=Room.styles.coords)}")

    print(f"...coords large enough to squeeze out padding")
    g_r = Room(coords=(3, 10))
    print(f"{g_r.str(style=Room.styles.coords)}")
    g_r = Room(coords=(10, 10))
    print(f"{g_r.str(style=Room.styles.coords)}")

    print(f"room with doors and a potion:")
    g_r.add_door('N')
    g_r.add_door('west')
    g_r.healing_potions += 2
    print(f"{g_r}")
    print(f"...description thereof:")
    print(g_r.describe())
    print("...rendered with 'open' style doors:")
    print(f"{g_r.str(style=Room.styles.open)}")
    print("...rendered with Tom's janky style:")
    print(f"{g_r.str(style=Room.styles.tom)}")

    print(f"...rendered tracker style, and hero present:")
    g_r.has_hero = True
    print(f"{g_r.str(style=Room.styles.tracker)}")
    print(f"...or hero not present, but has visited/seen:")
    g_r.has_hero = False
    g_r.has_crumb = True
    print(f"{g_r.str(style=Room.styles.tracker)}")

# END
