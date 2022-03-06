from typing import Optional

from Item import *
from Cell import Cell
from Util import obj_repr


class RoomContents:
    def __init__(self):
        self.__ingress: bool = False
        self.__egress: bool = False
        # TODO instances, not ints/bools
        self.__pit: bool = False
        self.__health: int = 0
        self.__vision: int = 0
        self.__bomb: int = 0
        self.__pillar: Optional[str] = None

    @property
    def ingress(self):
        return self.__ingress

    @ingress.setter
    def ingress(self, val: bool):
        self.__ingress = val

    @property
    def egress(self):
        return self.__egress

    @egress.setter
    def egress(self, val: bool):
        self.__egress = val

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

    @property
    def pillar(self):
        return self.__pillar

    @pillar.setter
    def pillar(self, val: Optional[Pillar]):
        self.__pillar = val

    def can_add(self, obj: Any):
        if self.ingress or self.egress:
            return False
        else:
            if isinstance(obj, Pillar):
                # print(f"{obj} is Pillar instance")
                return True
            elif isinstance(obj, Item):
                # print(f"{obj} is Item instance")
                return True
            elif isinstance(obj, type) and issubclass(obj, Pillar):
                # print(f"{obj} is Pillar subclass")
                return True
            elif isinstance(obj, type) and issubclass(obj, Item):
                # print(f"{obj} is Item subclass")
                return True
        return False

    def can_have(self, obj: Any):
        if self.ingress or self.egress:
            return False
        else:
            if isinstance(obj, type):
                if issubclass(obj, Item):
                    return True
                # if issubclass(obj, Pillar):
                #     return True
            elif isinstance(obj, Item):
                return True
            # elif isinstance(obj, Pillar):
            #     return True
        return False

    def add(self, *items) -> None:
        for i in items:
            if not self.can_add(i):
                # TODO raising exception mauybe too extreme, but at least log somewhere
                raise TypeError(f"room cannot add {i}")
                # continue
            # TODO instantiate (if passed class) and add
            if isinstance(i, type):
                if issubclass(i, Pit):
                    self.pit = True
                elif issubclass(i, HealthPotion):
                    self.health += 1
                elif issubclass(i, VisionPotion):
                    self.vision += 1
                elif issubclass(i, Bomb):
                    self.bomb += 1
            elif isinstance(i, Pillar):
                self.pillar = i

    def has(self, item: Any) -> bool:
        i = item
        if not self.can_have(i):
            # TODO raising exception mauybe too extreme, but at least log somewhere
            raise TypeError(f"room cannot have {i}")
            # return False
        if isinstance(i, type):
            if issubclass(i, Pit):
                return bool(self.pit)
            elif issubclass(i, VisionPotion):
                return self.vision > 0
            elif issubclass(i, HealthPotion):
                return self.health > 0
            elif i is Potion:
                return self.has(HealthPotion) or self.has(VisionPotion)
            elif issubclass(i, VisionPotion):
                return self.vision > 0
            elif issubclass(i, Bomb):
                return self.bomb > 0
            elif issubclass(i, Pillar):
                return bool(self.pillar)
        elif isinstance(i, Pillar):
            return i is self.pillar
        return False

    def __repr__(self):
        return obj_repr(self)


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


if __name__ == '__main__':

    def example():
        """Example code"""
        print(f'RoomContents 1...')
        cont = RoomContents()
        cont.add(HealthPotion)
        cont.add(Bomb)
        print(cont)
        print(f'has a Potion? {cont.has(Potion)}')
        print(f'has a Vision Potion? {cont.has(VisionPotion)}')
        print(f'has a Health Potion? {cont.has(HealthPotion)}')
        print(f'has a Bomb? {cont.has(Bomb)}')

        print(f'RoomContents 2...')
        cont = RoomContents()
        cont.add(Pit, VisionPotion)
        cont.add(Abstraction)
        print(cont)
        print(f'has a Pit? {cont.has(Pit)}')
        print(f'has a Potion? {cont.has(Potion)}')
        print(f'has a Vision Potion? {cont.has(VisionPotion)}')
        print(f'has a Health Potion? {cont.has(HealthPotion)}')
        print(f'has a Bomb? {cont.has(Bomb)}')
        print(f'has a Pillar? {cont.has(Pillar)}')
        print(f'has Abstraction? {cont.has(Abstraction)}')
        print(f'has Encapsulation? {cont.has(Encapsulation)}')

        print(f'Room 1...')
        room = Room()
        room.contents.add(Pit)
        print(room)

        print(f'Room 2...')
        room = Room()
        room.contents.add(VisionPotion, HealthPotion)
        print(room)

    example()

# END
