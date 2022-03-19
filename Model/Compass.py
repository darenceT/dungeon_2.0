# from version 1.0. This will be retired, new version in Model

from typing import Optional, Union, ForwardRef

Coords = tuple[int, int]
DirObj = ForwardRef('CompassDirection')
DirAny = Union[DirObj, str, int]


class CompassDirection:
    """
    Defines the characteristics of each individual compass direction
    """
    def __init__(self, name: str, mask: int, vector: Coords, abbr: str = None):
        """
        TODO docs
        :param name: String, Name of direction
        :param mask: Integer, mask representation of direction
        :param vector: Change in coordinates for next room in provided direction
        :param abbr: String, abbreviation for Direction
        """
        self.__name: str = name.capitalize()
        self.__abbr: str = self.name[0]
        if abbr is not None:
            self.__abbr = abbr.upper()
        self.__mask: int = mask
        self.__vector: Coords = vector

    def diag(self, dir2):
        """
        Allows for diagonal movement with two provided directions
        :param dir2:
        :return:
        """
        if self.mask & ~self.mask != 0 or dir2.mask & ~dir2.mask != 0:
            raise ValueError(f"can only create diagonal direction from two perpendicular directions")
        return CompassDirection(name=self.name + dir2.name,
                                abbr=self.abbr + dir2.abbr,
                                mask=self.mask | dir2.mask,
                                vector=(self.vector[0] + dir2.vector[0], self.vector[1] + dir2.vector[1]))

    @property
    def name(self) -> str:
        """
        Returns name of direction
        :return:
        """
        return self.__name

    @property
    def abbr(self) -> str:
        """
        Returns abbreviation for direction
        :return:
        """
        return self.__abbr

    @property
    def mask(self) -> int:
        """
        Returns direction mask
        :return:
        """
        return self.__mask

    @property
    def vector(self) -> Coords:
        """
        Returns direction vector
        :return:
        """
        return self.__vector

    @property
    def vect_x(self) -> int:
        """
        Returns direction vector on x axis
        :return:
        """
        return self.__vector[0]

    @property
    def vect_y(self) -> int:
        """
        Returns direction vector on y axis
        :return:
        """
        return self.__vector[1]

    @property
    def opposite(self) -> DirObj:
        """
        Returns opposite of direction
        :return:
        """
        return Compass.opposites.get(self)


class Compass:
    """
    Class that sets characteristics of all directions
    """
    north = CompassDirection(name='North', mask=0b1000, vector=(0, -1))
    south = CompassDirection(name='South', mask=0b0100, vector=(0, +1))
    west = CompassDirection(name='West', mask=0b0010, vector=(-1, 0))
    east = CompassDirection(name='East', mask=0b0001, vector=(+1, 0))
    dirs: list = [north, south, west, east]

    northwest = north.diag(west)
    southwest = south.diag(west)
    northeast = north.diag(east)
    southeast = south.diag(east)
    diags: list = [northwest, southwest, northeast, southeast]

    # Map each direction to its opposite.
    # Could be done programmatically, but whatever. Eight lines.
    opposites = {
        north: south,
        south: north,
        east: west,
        west: east,
        northeast: southwest,
        southwest: northeast,
        northwest: southeast,
        southeast: northwest,
    }

    # Map from string representations of each direction to its instance.
    # Lookups are case-insensitive and works for full name or first letter.
    # So for example, these all work: "North", "NORTH", "north", "N", "n".
    # This might be better implemented with collections.Mapping subclass;
    # but dict with overloaded keys is quick-n-easy.
    names: dict = {}
    names.update([(_d.name.lower(), _d) for _d in dirs])
    names.update([(_d.name.lower()[0], _d) for _d in dirs])
    # If lookup always lower-cases target first -- which dir() does --
    # then don't need to add dict keys for any other case combinations.
    # names.update([(_d.name, _d) for _d in dirs])
    # names.update([(_d.name[0], _d) for _d in dirs])
    # names.update([(_d.name.upper(), _d) for _d in dirs])

    # Map from bitmask representation of each direction to its instance.
    # This might be better implemented with collection.Sequence subclass,
    # but list grokking sparse array is quick-n-easy.
    masks: list = [None] * ((1 << len(dirs)) + 1)
    for _d in dirs:
        masks[_d.mask] = _d

    @staticmethod
    def opposite(dir: DirAny) -> Optional[CompassDirection]:
        """
        Returns opposites of all directions
        :param dir:
        :return:
        """
        return Compass.opposites.get(Compass.dir(dir))

    @staticmethod
    def name2dir(name: str) -> Optional[CompassDirection]:
        """ Lookup direction by name (string).
        :param name: String corresponding to one direction.
        :return: CompassDirection instance, or None.
        """
        name = name.lower()
        out = Compass.names.get(name)
        return out

    @staticmethod
    def mask2dir(mask: int) -> Optional[CompassDirection]:
        """ Lookup direction by bitmask (integer).
        :param mask: Integer mask corresponding to one direction.
        :return: CompassDirection instance, or None.
        """
        if 0 < mask < len(Compass.masks):
            return Compass.masks[mask]
        return None

    @staticmethod
    def dir(val: DirAny) -> Optional[CompassDirection]:
        """ Lookup direction by bitmask (integer).
        :param val: Value corresponding to one direction.
        :return: CompassDirection instance, or None.
        """
        if isinstance(val, CompassDirection) and val in Compass.dirs:
            return val
        if isinstance(val, int):
            return Compass.mask2dir(val)
        if isinstance(val, str):
            return Compass.name2dir(val)
        raise TypeError(f"Compass.dir() does not accept that type")

    @staticmethod
    def dirs2mask(dirs: list[DirAny]) -> int:
        """ TODO summary
        :param dirs: List of zero or more CompassDirection instances or string names
        :return: Integer mask representing zero to multiple directions
        """
        out = 0
        for _d in dirs:
            out |= Compass.dir(_d).mask
        return out

    @staticmethod
    def mask2dirs(mask: int) -> list[CompassDirection]:
        """ TODO summary
        :param mask: Integer mask representing zero to multiple directions.
        :return: List of CompassDirection instances
        """
        out = []
        for _d2 in Compass.dirs:
            if mask & _d2.mask:
                out.append(_d2)
        return out


North = Compass.north
South = Compass.south
West = Compass.west
East = Compass.east


if __name__ == '__main__':
    print(f"Greetings from Compass!")

    def show_dirs(dir_list):
        for _d in dir_list:
            _mask = f"{_d.mask:04b}({_d.mask})"  # max width 8
            _vec = str(_d.vector)  # max width 8
            _opp = _d.opposite.name
            print(f"name:{_d.name:6} abbr:{_d.abbr} mask:{_mask:8} vector:{_vec:8} opposite:{_opp}")

    print(f"\nPrimary directions:")
    show_dirs(Compass.dirs)
    print(f"\nDiagonal directions:")
    show_dirs(Compass.diags)

# END

