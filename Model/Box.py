from Model.Compass import *
from Model.Util import obj_repr


class Box:
    """
    The four boundaries of a square.
    """
    __dirs = (North, South, East, West)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__sides = [None] * 4
        # self.__north = None
        # self.__east = None
        # self.__south = None
        # self.__west = None

    def __getitem__(self, item):
        """
        Gets an item in the side of the box
        :param:
        :return: sides[item]
        """
        return self.__sides[item]

    def __setitem__(self, key, value):
        """
        Sets an item in the side of the box
        :param: key, value
        """
        self.__sides[key] = value

    @property
    def N(self):
        """"
        Gets the north side of the box
        :return: self[0]
        """
        # return self.__north
        return self[0]

    @N.setter
    def N(self, val):
        """
        Sets the north side of the box
        :param: value of cell
        """
        # self.__north = val
        self[0] = val

    @property
    def E(self):
        """
        Gets the East side of the box
        :return: self[1]
        """
        # return self.__east
        return self[1]

    @E.setter
    def E(self, val):
        """
        Sets the cell on the East side of the box
        :param: value of cell
        """
        # self.__east = val
        self[1] = val

    @property
    def S(self):
        """
        Gets the cell on the South side of the box
        :return: self[2]
        """
        # return self.__south
        return self[2]

    @S.setter
    def S(self, val):
        """
        Sets the cell on the South side of the box
        :param: value of cell
        """
        # self.__south = val
        self[2] = val

    @property
    def W(self):
        """
        Gets the cell on the West side of the box
        :return: self[3]
        """
        # return self.__west
        return self[3]

    @W.setter
    def W(self, val):
        """
        Sets the cell on the West side of the box
        :param: value of cell
        """
        # self.__west = val
        self[3] = val

    def __repr__(self):
        """
        Representation of the box
        :return: obj_repr
        """
        return obj_repr(self)

    @staticmethod
    def dir2idx(dir) -> int:
        """
        Returns the compass directions of the box
        :return: compass directions
        """
        d = Compass.dir(dir)
        if d in Box.__dirs:
            return Box.__dirs.index(d)

if __name__ == '__main__':

    def example():
        box1 = Box()
        box1.E = "morning"
        box1.W = "wicked"
        box1.S = "tropics"
        box1.S = "arctic"
        print(f"Box 1: {box1}")

    example()

# END
