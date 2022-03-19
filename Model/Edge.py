from abc import ABCMeta, abstractmethod

from Util import obj_repr


class Edge(metaclass=ABCMeta):
    """
    Initializes the Edge class. Identifies and classifies the edges between rooms/around rooms in the maze.
    """
    def __init__(self):
        self.__mates: list = []
        self.__can_pass: bool = True
        self.__can_peek: bool = True

    @property
    def mates(self):
        """
        Gets the cells on either side of the edge.
        :return: mates.copy()
        """
        return self.__mates.copy()

    @property
    def can_pass(self):
        """
        Gets a boolean determining if an edge is passable or not
        :return: can_pass (boolean)
        """
        return self.__can_pass

    @property
    def can_peek(self):
        """
        Gets a boolean determining if the hero can see past an edge or not
        :return: can_peak (boolean)
        """
        return self.__can_peek

    def mate(self, room):
        # XXX Can None be passed as room? For a perimeter wall, I guess so.
        # But can a wall/door link to The Void... on both sides? Whoa.
        """
        Takes in a room parameter and determines if it is a mate with the current room
        :param: room
        :return: r if room is not a mate
        """
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
        """
        abstract method taking in a room parameter and providing a link method for later use
        """
        pass

    def __repr__(self):
        """
        Gets the representation of the edge
        :return: obj_repr
        """
        return obj_repr(self)


class Wall(Edge):
    """
    Initializes the Wall class, a subclass of edge for impassable edges
    """
    def __init__(self):
        super().__init__()
        self.__can_pass: bool = False
        self.__can_peek: bool = False

    def link(self, room):
        """
        Establishes a link to a room
        :param: room
        """
        self._link(room)

    def bust(self, room):
        """
        Method for a busted wall, setting can pass and can peek to true, from current room (passed in as parameter)
        :param: room
        """
        self.__can_pass = True
        self.__can_peek = True


class Door(Edge):
    """
    Initializes the door class, a subclass of Edge for passable passageways
    """
    def __init__(self):
        super().__init__()
        self.__can_pass: bool = True
        self.__can_peek: bool = False

    def link(self, room):
        """
        Establishes a link to the room
        :param: room
        """
        self._link(room)

    def open(self):
        """
        Sets open doors to allow the hero to peek through them
        """
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
