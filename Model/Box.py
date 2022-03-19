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

    def __getitem__(self, key):
        """
        Gets an item in the side of the box
        :param key:
        :return: sides[item]
        """
        idx = self.dir2idx(key)
        if idx is not None:
            return self.__sides[idx]

    def __setitem__(self, key, val):
        """
        Sets an item in the side of the box
        :param key:
        :param val:
        """
        idx = self.dir2idx(key)
        if idx is not None:
            self.__sides[idx] = val

    @property
    def N(self):
        """"
        Gets the north side of the box
        :return: self[0]
        """
        idx = self.dir2idx(North)
        if idx is not None:
            return self.__sides[idx]

    @N.setter
    def N(self, val):
        """
        Sets the north side of the box
        :param: value of cell
        """
        idx = self.dir2idx(North)
        if idx is not None:
            self.__sides[idx] = val

    @property
    def E(self):
        """
        Gets the East side of the box
        :return: self[1]
        """
        idx = self.dir2idx(East)
        if idx is not None:
            return self.__sides[idx]

    @E.setter
    def E(self, val):
        """
        Sets the cell on the East side of the box
        :param: value of cell
        """
        idx = self.dir2idx(East)
        if idx is not None:
            self.__sides[idx] = val

    @property
    def S(self):
        """
        Gets the cell on the South side of the box
        :return: self[2]
        """
        idx = self.dir2idx(South)
        if idx is not None:
            return self.__sides[idx]

    @S.setter
    def S(self, val):
        """
        Sets the cell on the South side of the box
        :param: value of cell
        """
        idx = self.dir2idx(South)
        if idx is not None:
            self.__sides[idx] = val

    @property
    def W(self):
        """
        Gets the cell on the West side of the box
        :return: self[3]
        """
        idx = self.dir2idx(West)
        if idx is not None:
            return self.__sides[idx]

    @W.setter
    def W(self, val):
        """
        Sets the cell on the West side of the box
        :param: value of cell
        """
        idx = self.dir2idx(West)
        if idx is not None:
            self.__sides[idx] = val

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
        box = Box()
        box.E = "morning"
        box.W = "wicked"
        box.S = "tropics"
        box.N = "arctic"
        for d in Compass.dirs:
            print(f'{d} -> side index {box.dir2idx(d)}')
        print(box)
        print(f'box.N...')
        print(box.N)
        print(f'box[North]...')
        print(box[North])

    example()

# END
