from typing import Any

from Model.Cell import Cell
from Model.Characters.Monster import Monster
from Model.Characters.MonsterFactory import MonsterFactory
from Model.Item import *
from Model.Util import obj_repr


class Room(Cell):
    """
    A room, i.e. a cell and its contents.
    """

    def __init__(self):
        super().__init__()
        self.__ingress: bool = False
        self.__egress: bool = False
        self.__contents: dict = {}
        self.__occupants: list = []

    @property
    def contents(self):
        return self.__contents

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
    def occupants(self):
        return self.__occupants

    @occupants.setter
    def occupants(self, info):
        # TODO: add check for monster class type else error
        npc, remove = info
        if npc is not None:
            if remove:
                self.__occupants.remove(npc)
            else:
                self.__occupants.append(npc)

    def can_have(self, obj: Any):
        if isinstance(obj, type) and issubclass(obj, Monster):
            return True
        elif isinstance(obj, Monster):
            return True
        if self.ingress or self.egress:
            return False
        else:
            if isinstance(obj, type):
                if issubclass(obj, Item):
                    return True
            elif isinstance(obj, Item):
                return True
        return False

    def __getitem__(self, item: Any):
        i = item
        if not self.can_have(i):
            # TODO raising exception mauybe too extreme, but at least log somewhere
            raise TypeError(f"room cannot have {i}")
            # return None
        if isinstance(i, type):
            if issubclass(i, Pit):
                return self.contents.get(Pit)
            elif issubclass(i, VisionPotion):
                return self.contents.get(VisionPotion)
            elif issubclass(i, HealthPotion):
                return self.contents.get(HealthPotion)
            elif i is Potion:
                all_potions = []
                for i in (HealthPotion, VisionPotion):
                    p = self.contents.get(i)
                    if p:
                        all_potions += p
                if all_potions:
                    return all_potions
                return None
            elif issubclass(i, Bomb):
                return self.contents.get(Bomb)
            elif issubclass(i, Pillar):
                return self.contents.get(Pillar)
            elif issubclass(i, Monster):
                # TODO Monster subclass
                # return self.occupants.get(i)
                # return self.occupants
                return [o for o in self.occupants if isinstance(o, i)]
        elif isinstance(i, Pillar):
            pillar = self.contents.get(Pillar)
            if pillar and i is pillar:
                return pillar
        return None

    def has(self, obj: Any):
        return bool(self.__getitem__(obj))

    def can_add(self, obj: Any):
        if isinstance(obj, type) and issubclass(obj, Monster):
            return True
        elif isinstance(obj, Monster):
            return True
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

    def add_only(self, group: type, obj: Any):
        if self.contents.get(group):
            raise ValueError(f"room already has a {group.__name__}")
        self.contents[group] = obj
        obj.owner = self

    def make_add_only(self, group: type, cls: type):
        if self.contents.get(group):
            raise ValueError(f"room already has a {group.__name__}")
        obj = cls()
        self.contents[group] = obj
        obj.owner = self

    def add_one(self, group: type, obj: Any):
        if not self.contents.get(group):
            self.contents[group] = [obj]
        else:
            self.contents[group].append(obj)
        obj.owner = self

    def make_add_one(self, group: type, cls: type):
        obj = cls()
        self.add_one(group, obj)

    def add(self, *items) -> None:
        """ Add items to room. Each item may be either an instance of an Item subclass,
        or may be one of those subclasses itself. If specified by class, will be instantiated.
        :param items: Zero or more items to add. Items may be a mix of instances and classes.
        """
        # TODO assign self as owner of each added item
        for i in items:
            if not self.can_add(i):
                # TODO raising exception mauybe too extreme, but at least log somewhere
                raise TypeError(f"room cannot add {i}")
                # continue
            if isinstance(i, type):
                if issubclass(i, Pit):
                    self.make_add_only(Pit, i)
                elif issubclass(i, HealthPotion):
                    self.make_add_one(HealthPotion, i)
                elif issubclass(i, VisionPotion):
                    self.make_add_one(VisionPotion, i)
                elif issubclass(i, Bomb):
                    self.make_add_one(Bomb, i)
                # TODO get rid of separate __occupants, add Monster as __contents group
                # elif issubclass(i, Monster):
                #     self.make_add_one(Monster, i)
                else:
                    raise TypeError(f"room add, unrecognized class {i}")
            elif isinstance(i, Pit):
                self.add_only(Pit, i)
            elif isinstance(i, HealthPotion):
                self.add_one(HealthPotion, i)
            elif isinstance(i, VisionPotion):
                self.add_one(VisionPotion, i)
            elif isinstance(i, Bomb):
                self.add_one(Bomb, i)
            elif isinstance(i, Pillar):
                self.add_only(Pillar, i)
            elif isinstance(i, Monster):
                # TODO get rid of separate __occupants, add Monster as __contents group
                # self.add_one(Monster, i)
                self.__occupants.append(i)
                # Monsters have no owner; skip setting
                continue
            else:
                raise TypeError(f"room add, instance of unrecognized type {type(i)}")
            i.owner = self

    @staticmethod
    def can_pop(obj: Any) -> bool:
        if isinstance(obj, type):
            if isinstance(obj, Bomb):
                return True
            # Not allowed to "pop" abstract Potion, only its subclass
            if issubclass(obj, VisionPotion):
                return True
            if issubclass(obj, HealthPotion):
                return True
            if issubclass(obj, Monster):
                return True
        if isinstance(obj, Monster):
            return True
        return False

    def pop(self, obj: Any) -> Any:
        if not self.can_pop(obj):
            return None  # TODO raise exception and/or log error?
        # Monsters
        # TODO replace __occupants with a Monster group in __contents
        if (isinstance(obj, type) and issubclass(obj, Monster)) or isinstance(obj, Monster):
            have = self.occupants
            if not have:
                return None  # TODO log error? depends whether caller expected to first check has()
            monster = have.pop()
            return monster
        # Items
        have = self.contents.get(obj)
        if not have:
            return None  # TODO log error? depends whether caller expected to first check has()
        item = have.pop()
        obj.owner = None
        return item

    def __repr__(self) -> str:
        return obj_repr(self)


if __name__ == '__main__':

    from Model.Characters.Gremlin import Gremlin
    from Model.Characters.Ogre import Ogre
    from Model.Characters.Skeleton import Skeleton

    def example():
        """Example code"""
        room = Room()
        # Can add multiple items in single call.
        # These may be class names and/or instances thereof.
        # Pillar is unique; can only add one of its fixed set of instances.
        room.add(Pit, VisionPotion, Abstraction)
        print(room)

        # For some item types, can have zero to many: Potions, Bombs.
        # For other item types, only have zero or one: Pit, Pillar.
        print(f'has a Pit? {room.has(Pit)}')
        try:
            room.add(Pit)
        except ValueError as e:
            print(f"cannot add Pit: {e}")
        print(f'has a Bomb? {room.has(Bomb)}')

        # Can have zero to many Bombs.
        room.add(Bomb)
        obj = Bomb()
        room.add(obj)

        # Can have zero to many of the various Potions.
        print(f'has a Potion? {room.has(Potion)}')
        print(f"how many? {len(room[Potion])}")
        print(f'has a Health Potion? {room.has(HealthPotion)}')
        print(f'has a Vision Potion? {room.has(VisionPotion)}')
        print(f"how many? {len(room[VisionPotion])}")
        room.add(VisionPotion)
        obj = VisionPotion()
        room.add(obj)
        print(f"added 2 more, now have {len(room[VisionPotion])}")
        obj = room.pop(VisionPotion)
        print(f"popped 1: {obj}")
        print(f"how many now? {len(room[VisionPotion])}")
        room.add(HealthPotion)
        print(f"added 1 Health Potion")
        print(f"how many total Potions now? {len(room[Potion])}")

        # Can only have zero or one of the Pillar instances.
        print(f'has a Pillar? {room.has(Pillar)}')
        print(f'has Abstraction? {room.has(Abstraction)}')
        print(f'has Encapsulation? {room.has(Encapsulation)}')
        try:
            room.add(Encapsulation)
        except ValueError as e:
            print(f"cannot add Encapsulation: {e}")

        # Can have zero to many Monsters
        print(f'has a Monster? {room.has(Monster)}')
        print(f"how many occupants? {len(room.occupants)}")
        gremlin = Gremlin(mtype='gremlin', name='jacko')
        ogre = Ogre(mtype='ogre', name='rocko')
        room.add(gremlin, ogre)
        # TODO replace __occupants with Monster group in __contents
        # print(f"added 2, now have {len(room[Monster])}")
        print('added 2')
        print(f'has a Monster? {room.has(Monster)}')
        print(f'has a Gremlin? {room.has(Gremlin)}')
        print(f'has a Skeleton? {room.has(Skeleton)}')
        print(f'occupants now ({len(room.occupants)})...')
        for o in room.occupants:
            print(o)

        print("after adding some more items...")
        print(room)

    example()

# END
