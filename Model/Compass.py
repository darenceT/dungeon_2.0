from typing import Optional, Union, ForwardRef

from Model.Util import obj_repr
from Model.Direction import Direction

DirObj = ForwardRef('CompassDirection')
DirAny = Union[DirObj, str, int]

class CompassDirection(Direction):
    """
    Initializes the CompassDirection class, which establishes the four cardinall values of the compass.
    """
    def __init__(self, mask: int = 0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__mask = mask

    @property
    def mask(self):
        return self.__mask


def __is_pow2(val: int):
    """
    TODO: Docstring
    """
    return (val + (val >> 1)) & ~val == val >> 1

def __diag(dir1: CompassDirection, dir2: CompassDirection):
    """
    Allows for diagonal movement with two provided directions
    :param dir2:
    :return:
    """
    if not __is_pow2(dir1.mask) or not __is_pow2(dir2.mask):
        raise ValueError(f"can only create diagonal direction from two primary directions")
    # FIXME also should check are not N+S nor E+W
    return CompassDirection(abbr=''.join([dir1.abbr, dir2.abbr]),
                     name=''.join([dir1.name, dir2.name.lower()]),
                     mask=dir1.mask | dir2.mask,
                     vect=(dir1.vector[0] + dir2.vector[0], dir1.vector[1] + dir2.vector[1]))

North = CompassDirection(abbr='N', name='North', mask=0b1000, vect=(0, 1))
South = CompassDirection(abbr='S', name='South', mask=0b0100, vect=(0, -1))
West = CompassDirection(abbr='W', name='West', mask=0b0010, vect=(-1, 0))
East = CompassDirection(abbr='E', name='East', mask=0b0001, vect=(1, 0))
Northeast = __diag(North, East)
Southeast = __diag(South, East)
Northwest = __diag(North, West)
Southwest = __diag(South, West)

class Compass:
    """
    The Compass class establishes all of the possible compass directions and their aliases
    """
    dirs: tuple = (North, South, East, West)
    diags: tuple = (Northeast, Southeast, Northwest, Southwest)
    xdirs: tuple = (*dirs, *diags)

    # Aliases to the globally defined instances
    north = North
    south = South
    east = East
    west = West
    northwest = Northwest
    southwest = Southwest
    northeast = Northeast
    southeast = Southeast

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
    def opposite(val: DirAny) -> Optional[CompassDirection]:
        """
        Returns opposites of all directions
        :param val:
        :return:
        """
        return Compass.opposites.get(Compass.dir(val))

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

    def __getitem__(self, item):
        if isinstance(item, str):
            if len(item) == 1 or len(item) == 2:
                item = item.upper()
                for d in Compass.xdirs:
                    if item == d.abbr:
                        return d
            elif len(item) > 2:
                item = item.capitalize()
                for d in Compass.xdirs:
                    if item == d.name:
                        return d
        return None


if __name__ == '__main__':
    def example():
        x: Compass = Compass()
        print('Four primary dirs...')
        for d in x.dirs:
            print(f'{d}: {obj_repr(d)}')
        print('Four secondary dirs...')
        for d in x.diags:
            print(f'{d}: {obj_repr(d)}')
        print('Case-insensitive name lookup...')
        for s in ('N n north North NORTH NoRtH southWest foo'.split(' ')):
            d = x[s]
            print(f"{s} -> {d}")

    example()

# END
