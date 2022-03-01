from typing import Optional

Coords = tuple[int, int]


class Box:
    """
    The four boundaries of a square.
    """
    def __init__(self):
        self.__north = None
        self.__east = None
        self.__south = None
        self.__west = None

    @property
    def N(self):
        return self.__north

    @N.setter
    def N(self, val):
        self.__north = val

    @property
    def E(self):
        return self.__east

    @E.setter
    def E(self, val):
        self.__east = val

    @property
    def S(self):
        return self.__south

    @S.setter
    def S(self, val):
        self.__south = val

    @property
    def W(self):
        return self.__west

    @W.setter
    def W(self, val):
        self.__west = val


class Cell(Box):
    """
    Represents the smallest unit of floor area.
    """
    def __init__(self):
        super().__init__()
        self.__coords: Optional[Coords] = None

    @property
    def xy(self):
        return self.__coords

    @xy.setter
    def xy(self, val: Coords):
        self.__coords = val


if __name__ == '__main__':
    # Example code
    from pprint import PrettyPrinter

    g_pp = PrettyPrinter(compact=True)
    g_box1 = Box()
    g_box1.E = "morning"
    g_box1.W = "wicked"
    g_box1.S = "tropics"
    g_box1.S = "arctic"
    print(f"Box 1: {g_pp.pformat(vars(g_box1))}")

    g_cell1 = Cell()
    g_cell1.E = "juliet"
    g_cell1.W = "sundown"
    g_cell1.xy = (4, 5)
    print(f"Cell 1: {g_pp.pformat(vars(g_cell1))}")

# END
