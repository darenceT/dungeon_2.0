from abc import ABCMeta
from collections import namedtuple
from typing import Any

from Model.Util import obj_repr


class Item:  # (metaclass=ABCMeta):
    __portable: bool = True
    """
    Class representing the (non character) items in the maze
    """
    def __init__(self, owner: Any = None):
        # super().__init__()
        self.__owner = owner

    @property
    def owner(self):
        """
        Gets the item owner, this can be a room or a hero
        :return: owner
        """
        return self.__owner

    @owner.setter
    def owner(self, val: Any):
        """
        Sets the item owner, this can be a room or a hero
        param: value
        """
        self.__owner = val

    @property
    def portable(self):
        """
        Gets portable property, is item portable? Set to true by default so hero can collect items
        :return: portable
        """
        return self.__portable

    def __repr__(self):
        """
        Gets representation of item
        :return: obj_repr
        """
        return obj_repr(self)


class Trap(Item):
    """
    The trap that our hero may fall into and take damage
    """
    __portable = False  # override Item default
    __damage: int = 10

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def damage(self):
        """
        Get damage caused by trap
        :return: damage
        """
        return self.__damage


class Pit(Trap):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Snare(Trap):
    """ Another subclass of Trap, not (yet) implemented in game. """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Bomb(Item):
    """
    For possible future implementation: a bomb that can do damage to the hero
    """
    __damage: int = 10

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def damage(self):
        """
        Get damage caused by bomb
        :return: damage
        """
        return self.__damage


class Potion(Item):  # , metaclass=ABCMeta):
    """ Abstract base class for potions.
     At present, nothing to distinguish it from Item base class,
     except as a logical superclass of only the Potion classes.
     """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class VisionPotion(Potion):
    """
    A potion that allows the hero to see a larger portion of the map
    """
    __radius: int = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def radius(self):
        """
        Gets the radius of vision
        :return: radius
        """
        return self.__radius


class HealthPotion(Potion):
    """
    A potion that allows the hero to heal and recover some hit points
    """
    __points: int = 10

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def points(self):
        """
        Gets healing points
        :return: points
        """
        return self.__points


class Pillar(Item):
    """ The physical embodiment of one of the Pillars of Object-Oriented design.
    Sort of like a Badge of Participation. Except it is not portable.
    Perhaps more a Monument of Objectification? In any case...
    there are exactly four instances, each unique.
     """
    __portable = False

    __tmpl = namedtuple('__template', 'abbr name')
    __templates: list[__tmpl] = [
        __tmpl('A', 'Abstraction'),
        __tmpl('E', 'Encapsulation'),
        __tmpl('I', 'Inheritance'),
        __tmpl('P', 'Polymorphism'),
    ]
    __instances = []

    def __init__(self, name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for inst in Pillar.__instances:
            if name == inst.name:
                raise ValueError(f"Pillar '{name}' already instantiated")
        tmpl: Pillar.__tmpl
        for tmpl in Pillar.__templates:
            if name in tmpl:
                self.__abbr: str = tmpl.abbr
                self.__name: str = name
                Pillar.__instances.append(self)
                return
        raise ValueError(f"Pillar '{name}' is not valid")

    @property
    def abbr(self):
        """
        Gets pillar abbreviation
        :return: abbr
        """
        return self.__abbr

    @property
    def name(self):
        """
        Gets pillar name
        :return: name
        """
        return self.__name

    def __repr__(self):
        """
        Gets string representation of pillar
        :return: string (Pillar and pillar name)
        """
        return f"{self.__class__.__name__}({self.name})"


Abstraction = Pillar('Abstraction')
Encapsulation = Pillar('Encapsulation')
Inheritance = Pillar('Inheritance')
Polymorphism = Pillar('Polymorphism')
Pillars = (Abstraction, Encapsulation, Inheritance, Polymorphism)


if __name__ == '__main__':

    def example():
        print('instantiates various stuff...')
        stuff = dict()
        stuff[Trap] = Pit()
        stuff[Bomb] = [Bomb(), Bomb()]
        stuff[VisionPotion] = [VisionPotion()]
        stuff[HealthPotion] = [HealthPotion()]
        print(stuff)

        class Owner:
            def __init__(self, *args, **kw):
                super().__init__(*args, **kw)
                self.stuff: dict = {}

            def __repr__(self):
                return obj_repr(self)

        print('their soon-to-be owner...')
        owner = Owner()
        print(owner)

        print('their owner, though stuff does not know yet...')
        owner.stuff = stuff
        print(owner)

        print('their owner, after updating Pit instance with its owner...')
        owner.stuff[Trap].owner = owner
        print(owner)

        print("The Pillars of OO...")
        for p in Pillars:
            print(p)
        for name in ('Obfuscation', 'Abstraction'):
            print(f"Try to create pillar '{name}'...")
            try:
                p = Pillar(name)
                print(p)
            except ValueError as e:
                print(f'Nope! {e}')

    example()

# END
