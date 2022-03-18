from typing import NamedTuple, Union

from Model.Util import obj_repr

IntPair = tuple[int, int]


class Vect(NamedTuple):
    x: int
    y: int


Vectish = Union[IntPair, Vect]


class Direction:
    def __init__(self, abbr: str, name: str, vect: Vectish):
        self.__abbr = abbr
        self.__name = name
        self.__vect = Vect(*vect)

    @property
    def abbr(self):
        return self.__abbr

    @property
    def name(self):
        return self.__name

    @property
    def vect(self):
        return self.__vect

    @property
    def vector(self):
        """ Alias for `vect`. """
        return self.__vect

    def __str__(self):
        return self.name

    def __repr__(self):
        return obj_repr(self)


if __name__ == '__main__':

    def example():
        d1 = Direction('N', 'North', (0, 1))
        print(f"str(d1) = {d1}")
        print(f"d1 = {d1!r}")

        # show use of Vect fields by name and index
        v1 = d1.vect
        print(f"v1 = d1.vect...")
        print(f"v1    = {v1}")
        print(f"v1[0] = {v1[0]}, [1] = {v1[1]}")
        print(f"v1.x  = {v1.x }, .y  = {v1.y}")
        print(f"tuple = {tuple(v1)}")

        d2 = Direction('E', 'East', (1, 0))
        print(f"d2 = {d2!r}")

    example()

# END
