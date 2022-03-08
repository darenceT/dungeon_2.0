from abc import ABCMeta, abstractmethod

from Util import obj_repr


class Edge(metaclass=ABCMeta):
    def __init__(self):
        self.__mates: list = []
        self.__can_pass: bool = True
        self.__can_peek: bool = True

    @property
    def mates(self):
        return self.__mates.copy()

    @property
    def can_pass(self):
        return self.__can_pass

    @property
    def can_peek(self):
        return self.__can_peek

    def mate(self, room):
        # XXX Can None be passed as room? For a perimeter wall, I guess so.
        # But can a wall/door link to The Void... on both sides? Whoa.
        if room not in self.__mates:
            raise ValueError(f"room is not linked")
        if len(self.__mates) == 1:
            return None
        for r in self.__mates:
            if r is not room:
                return r

    def _link(self, room):
        """ Semi-private method for linking a room.
        Abstract superclass does not need this, but subclasses both do;
        so implemented once in superclass, and subclasses call in link().
        """
        if room in self.__mates:
            raise ValueError(f"already linked to room")
        if len(self.__mates) == 2:
            raise ValueError(f"already linked to two mates")
        nbr = None
        if len(self.__mates) == 1:
            nbr = self.__mates[0]
        self.__mates.append(room)

    @abstractmethod
    def link(self, room):
        pass

    def __repr__(self):
        return obj_repr(self)


class Wall(Edge):
    def __init__(self):
        super().__init__()
        self.__can_pass: bool = False
        self.__can_peek: bool = False

    def link(self, room):
        self._link(room)

    def bust(self, room):
        self.__can_pass = True
        self.__can_peek = True


class Door(Edge):
    def __init__(self):
        super().__init__()
        self.__can_pass: bool = True
        self.__can_peek: bool = False

    def link(self, room):
        self._link(room)

    def open(self):
        self.__can_peek = True


if __name__ == '__main__':

    def example():
        a = "One"
        print(f"make a Wall, link room {a}")
        wall = Wall()
        wall.link(a)
        print(wall)
        nbr = wall.mate(a)
        print(f"mate of {a}: {nbr}")
        try:
            print(f"link room {a} again...")
            wall.link(a)
        except ValueError as e:
            print(f"Nope! {e}")

        b = "Two"
        print(f"link room {b}...")
        wall.link(b)
        print(wall)
        nbr = wall.mate(b)
        print(f"mate of {b}: {nbr}")
        nbr = wall.mate(a)
        print(f"mate of {a}: {nbr}")

        c = "XXX"
        try:
            print(f"link room {c}...")
            wall.link(c)
        except ValueError as e:
            print(f"Nope! {e}")

        print(f"make a Door, link rooms {a}, {b}")
        door = Door()
        door.link(a)
        door.link(b)
        print(door)
        print(f"open door...")
        door.open()
        print(door)

    example()

# END
