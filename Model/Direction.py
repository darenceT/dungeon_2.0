from typing import NamedTuple, Union

IntPair = tuple[int, int]


class Vect(NamedTuple):
    x: int
    y: int


class Direction:
    def __init__(self, abbr: str, name: str, vect: IntPair):
        self.__abbr = abbr
        self.__name = name
        self.__vect = Vect(x=vect[0], y=vect[1])

    @property
    def abbr(self):
        return self.__abbr

    @property
    def name(self):
        return self.__name

    @property
    def vect(self):
        return self.__vect

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Direction(abbr:'{self.abbr}', name:'{self.name}', vect:{tuple(self.vect)}"


if __name__ == '__main__':
    from pprint import PrettyPrinter

    def example():
        pp = PrettyPrinter(compact=True)

        d1 = Direction('N', 'North', (0, 1))
        print("d1 = ", pp.pformat(vars(d1)))
        # show use of Vect fields by name and index
        v1 = d1.vect
        print(f"v1 = d1.vect...")
        print(f"v1    = {v1}")
        print(f"v1[0] = {v1[0]}, [1] = {v1[1]}")
        print(f"v1.x  = {v1.x }, .y  = {v1.y}")
        print(f"tuple = {tuple(v1)}")

        d2 = Direction('E', 'East', (1, 0))
        print("d2 = ", pp.pformat(vars(d2)))

    example()

# END
