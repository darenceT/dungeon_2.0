from Model.Cell import Cell
from Model.Characters.Monster import Monster
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
        # self.__occupants: list = []

    @property
    def contents(self):
        """
        Gets room contents, grouped by general type
        :return: dictionary of room contents. keys in dict are parents of logical hierarchies:
        Potion, Bomb, Trap, Pillar, Monster. values are lists of instances.
        """
        return self.__contents

    @property
    def ingress(self):
        """
        Gets ingress property - is it the entrance?
        :returns: boolean
        """
        return self.__ingress

    @ingress.setter
    def ingress(self, val: bool):
        """
        Sets ingress property
        param: boolean
        """
        self.__ingress = val

    @property
    def egress(self):
        """
        Gets egress property - is it the exit?
        :returns: boolean
        """
        return self.__egress

    @egress.setter
    def egress(self, val: bool):
        """
        Sets the egress property
        :param: boolean
        """
        self.__egress = val

    @property
    def occupants(self):
        """
        Gets list of non-Hero occupants.
        :return: occupants (list)
        """
        return self[Monster]

    @occupants.setter
    def occupants(self, info):
        """
        Adds room non-Hero occupants. (DEPRECATED)
        :param: info
        """
        # TODO: add check for monster class type else error
        npc, remove = info
        if not isinstance(npc, Monster):
            raise TypeError(f'Room occupants: non-Monster type {type(npc)}')
        if remove:
            # self.__occupants.remove(npc)
            self.pop(npc)
        else:
            # self.__occupants.append(npc)
            self.add(npc)

    @staticmethod
    def _group(obj: Any):
        """
        Maps an object or object type to the appropriate group in Room.contents.
        :param obj: a class or object. Generally, something under either Item or Monster.
        :return: class, which is key in contents dict; or None if obj not valid to add
        """
        is_cls = isinstance(obj, type)
        for group in (Trap, Potion, Bomb, Pillar, Monster):
            if is_cls:
                if issubclass(obj, group):
                    return group
            elif isinstance(obj, group):
                return group
        return None

    def can_have(self, obj: Any):
        """
        Checks to see if the room can have an object
        :param obj: a class or object. Generally, something under either Item or Monster.
        :return: boolean
        """
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

    def get_all(self, obj: Any):
        """
        Fetch all contents of a certain type, or a specific object.
        :param obj: a class or object. Generally, something under either Item or Monster.
        :return: list of items; will be empty, even for invalid obj
        """
        group = self._group(obj=obj)

        # Raw list or singleton (if any) for group
        glist = self.contents.get(group)
        if glist is None:
            return []
        if not isinstance(glist, list):
            return [glist]
        if len(glist) == 0:
            return []

        # Filtered down
        if isinstance(obj, type) and issubclass(obj, group):
            glist = [o for o in glist if isinstance(o, obj)]
            if len(glist) == 0:
                return []
            return glist
        elif isinstance(obj, group):
            if obj not in glist:
                return []
            return [obj]

        # Stuff that can_has() would have prevented
        elif isinstance(obj, type):
            raise ValueError(f'Room get_all: unecognized type {obj}')
        else:
            raise ValueError(f'Room get_all: instance of unecognized type {type(obj)}')

    def get_one(self, obj: Any):
        """
        Fetch any one instance of a specified type, or a specific object, if present.
        :param obj: a class or object. Generally, something under either Item or Monster.
        :return: one Item or Monster instance, or None if not present
        """
        glist = self.get_all(obj=obj)
        if glist is None or not isinstance(glist, list):
            return glist
        if len(glist) == 0:
            return None
        return glist[0]

    def __getitem__(self, item: Any):
        """
        Get something from room contents
        :param: item an Item or Monster type or instance
        :return: get item(s) if present
        """
        i = item
        is_cls = isinstance(i, type)
        if not self.can_have(i):
            if is_cls:
                raise TypeError(f"Room getitem: cannot have type {i}")
            else:
                raise TypeError(f"Room getitem: cannot have instance of type {type(i)}")
        group = self._group(i)
        glist = self.get_all(i)
        if group in (Pillar, Trap):
            if glist:
                return glist[0]
            else:
                return None
        else:  # Potions, Bombs, Monsters
            return glist

    def has(self, obj: Any):
        """
        Does a room contain a particular item?
        :return: boolean
        """
        return bool(self.__getitem__(obj))

    def can_add(self, obj: Any):
        """
        Can a room add a particular item or occupant?
        :return: boolean
        """
        group = self._group(obj)
        if group is Monster:  # can be present by entrance, exit, pillars
            return True
        if self.ingress or self.egress:
            print('Room can_add: nope, has Ingress or Egrress')
            return False
        if group is Pillar:  # cannot be present by entrance, exit
            return True
        if self.has(Pillar):
            print('Room can_add: nope, has Pillar')
            return False
        if group in (Potion, Bomb, Trap):
            return True
        return False

    def add_one(self, obj: Any):
        """
        Get only those items room can add
        :param: group, object
        """
        group = self._group(obj)
        if isinstance(obj, type):
            raise TypeError(f'Room add_one: can only add instance, not type {obj}')
        if not self.contents.get(group):
            self.contents[group] = [obj]
        else:
            self.contents[group].append(obj)
        obj.owner = self

    def make_add_one(self, cls: type):
        """
        Assign the item to a group
        :param: group, cls
        """
        obj = cls()
        self.add_one(obj)

    def add_only(self, obj: Any):
        group = self._group(obj)
        if self.contents.get(group):  # both not None and not len 0
            raise ValueError(f"Room add_only: limited to single {group.__name__}")
        self.add_one(obj)

    def make_add_only(self, cls: type):
        group = self._group(cls)
        if self.contents.get(group):
            raise ValueError(f"Room make_add_only: limited to single {group.__name__}")
        self.make_add_one(cls)

    def add(self, *items) -> None:
        """ Add items to room. Each item may be either an instance of an Item subclass,
        or may be one of those subclasses itself. If specified by class, will be instantiated.
        :param items: Zero or more items to add. Items may be a mix of instances and classes.
        """
        for i in items:
            is_cls = isinstance(i, type)
            group = self._group(i)
            if group is None:
                if is_cls:
                    raise TypeError(f"Room add: invalid type {i}")
                else:
                    raise TypeError(f"Room add: instance of invalid type {type(i)}")
            if not self.can_add(i):
                raise ValueError(f"Room add: mutual exclusion bars {group.__name__}")
                # continue
            if group in (Trap, Pillar):
                if is_cls:
                    self.make_add_only(i)
                else:
                    self.add_only(i)
            elif group in (Potion, Bomb, Monster):
                if is_cls:
                    self.make_add_one(i)
                else:
                    self.add_one(i)

    def can_pop(self, obj: Any) -> bool:
        """
        Can the room item be popped?
        Pillars and Traps cannot!
        :return: boolean
        """
        group = self._group(obj)
        if group in (Bomb, Potion, Monster):
            return True
        return False

    def pop(self, obj: Any) -> Any:
        """
        Pop item from room contents
        :param: object
        :return: item
        """
        is_cls = isinstance(obj, type)
        if not self.can_pop(obj):
            if is_cls:
                raise TypeError(f'Room pop: target is invalid type {obj}')
            else:
                raise TypeError(f'Room pop: target instance is invalid type {type(obj)}')
        group = self._group(obj)
        found = self.get_one(obj)
        if found:
            self.contents[group].remove(found)
            if group is not Monster:
                found.owner = None
            return found
        return None

    def __repr__(self) -> str:
        """
        Representation of room
        :return: obj_repr
        """
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
        # There are also restrictions on what can be present alongside particular type.
        room.add(Pit, VisionPotion)
        print(room)

        # For some item types, can have zero to many: Potions, Bombs.
        # For other item types, only have zero or one: Trip, Pillar.
        print(f'has a Trap? {room.has(Trap)}')
        print(f'has a Snare? {room.has(Snare)}')
        print(f'has a Pit? {room.has(Pit)}')
        try:
            room.add(Pit)
        except ValueError as e:
            print(f"cannot add Pit: {e}")

        # Can have zero to many Bombs.
        print(f'has a Bomb? {room.has(Bomb)}')
        room.add(Bomb)
        obj = Bomb()
        room.add(obj)

        # Can have zero to many of the various Potions.
        print(f'has a Potion? {room.has(Potion)}')
        print(f"how many? {len(room[Potion])}")
        print(f'has a Health Potion? {room.has(HealthPotion)}')
        print(f'has a Vision Potion? {room.has(VisionPotion)}')
        print(f"how many? {len(room[VisionPotion])}")
        print("add 2 more VisionPotions...")
        room.add(VisionPotion)
        obj = VisionPotion()
        room.add(obj)
        print(f"now have ({len(room[VisionPotion])})")
        print(f"pop 1 VisionPotion...")
        obj = room.pop(VisionPotion)
        print(f"popped: {obj}")
        print(f"how many now? {len(room[VisionPotion])}")
        print(f"add 1 VisionPotion...")
        obj = VisionPotion()
        print(obj_repr(obj, show_ids=True))
        room.add(obj)
        print(f"then pop that specific instance...")
        obj2 = room.pop(obj)
        print(f"popped: {obj_repr(obj2, show_ids=True)}")
        print(f"try popping that specific instance again...")
        obj2 = room.pop(obj)
        print(f"popped: {obj_repr(obj2, show_ids=True)}")

        print(f"added 1 Health Potion...")
        room.add(HealthPotion)
        print(f"how many total Potions now? {len(room[Potion])}")

        print("after adding some more items...")
        print(room)

        # Can only have zero or one of the Pillar instances.
        print('\nnew room...')
        room = Room()
        print(f'has a Pillar? {room.has(Pillar)}')
        print(f'has Abstraction? {room.has(Abstraction)}')
        print(f'has Encapsulation? {room.has(Encapsulation)}')
        for pillar in (Abstraction, Encapsulation):
            try:
                print(f"try adding {pillar}...")
                room.add(pillar)
            except ValueError as e:
                print(f"cannot: {e}")
        print(f'has a Pillar? {room.has(Pillar)}')
        print(f'has Abstraction? {room.has(Abstraction)}')
        print(f'has Encapsulation? {room.has(Encapsulation)}')

        # Other items not allowed alongside a Pillar
        for item in (Bomb, Pit, HealthPotion):
            try:
                print(f"try adding {item.__name__}...")
                room.add(item)
            except ValueError as e:
                print(e)

        # Can have zero to many Monsters
        # And they can be alongside Pillar
        print(f'has a Monster? {room.has(Monster)}')
        print(f"how many occupants? {len(room.occupants)}")
        print('add 1 Gremlin, 1 Ogre...')
        gremlin = Gremlin(mtype='gremlin', name='jacko')
        ogre = Ogre(mtype='ogre', name='rocko')
        room.add(gremlin, ogre)
        print(f'has a Monster? {room.has(Monster)}')
        print(f'has a Gremlin? {room.has(Gremlin)}')
        print(f'has a Ogre? {room.has(Ogre)}')
        print(f'has a Skeleton? {room.has(Skeleton)}')
        print(f'occupants now ({len(room.occupants)})...\n{room.occupants}')

    example()

# END
