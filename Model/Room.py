from Item import *
from Cell import Cell


class RoomContents:
    def __init__(self):
        self.__pit: bool = False
        self.__health: int = 0
        self.__vision: int = 0
        self.__bomb: int = 0

    @property
    def pit(self):
        return self.__pit

    @pit.setter
    def pit(self, val: bool):
        self.__pit = val

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, val: int):
        self.__health = val

    @property
    def vision(self):
        return self.__vision

    @vision.setter
    def vision(self, val: int):
        self.__vision = val

    @property
    def bomb(self):
        return self.__bomb

    @bomb.setter
    def bomb(self, val: int):
        self.__bomb = val

    def add(self, *item_types):
        for i in item_types:
            if not issubclass(i, Item):
                raise TypeError(f'room {self} cannot add non-item {i}')
            if issubclass(i, Pit):
                self.pit = True
            elif issubclass(i, HealthPotion):
                self.health += 1
            elif issubclass(i, VisionPotion):
                self.vision += 1
            elif issubclass(i, Bomb):
                self.bomb += 1

    def has(self, item_type):
        i = item_type
        if not issubclass(i, Item):
            raise TypeError(f'room {self} cannot haz non-item {i}')
        if issubclass(i, Pit):
            return bool(self.pit)
        elif issubclass(i, HealthPotion):
            return self.health > 0
        elif issubclass(i, VisionPotion):
            return self.vision > 0
        elif issubclass(i, Bomb):
            return self.bomb > 0


class Room(Cell):
    """
    A room, i.e. a cell and its contents.
    """
    def __init__(self):
        super().__init__()
        self.__contents: RoomContents = RoomContents()

    @property
    def contents(self):
        return self.__contents

    @contents.setter
    def contents(self, val: RoomContents):
        self.__contents = val


def example():
    """Example code"""
    from pprint import PrettyPrinter

    pp = PrettyPrinter(compact=True)

    print(f'Create 2 RoomContents...')
    cont1 = RoomContents()
    cont1.add(HealthPotion)
    cont1.add(Bomb)
    print(f'Contents 1: {pp.pformat(vars(cont1))}')

    cont2 = RoomContents()
    cont2.add(Pit, VisionPotion)
    print(f'Contents 2: {pp.pformat(vars(cont2))}')

    print(f'Create 2 Rooms...')
    room1 = Room()
    room1.contents.add(Pit)
    print(f'Room 1: {pp.pformat(vars(room1))}')

    room2 = Room()
    room2.contents.add(VisionPotion, HealthPotion)
    print(f'Room 2: {pp.pformat(vars(room2))}')


if __name__ == '__main__':
    example()

# END
