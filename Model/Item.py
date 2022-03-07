from abc import ABCMeta
from collections import namedtuple
from typing import Any


class Item(metaclass=ABCMeta):
    __portable: bool = True

    def __init__(self, owner: Any = None):
        self.__owner = owner

    @property
    def owner(self):
        return self.__owner

    @owner.setter
    def owner(self, val: Any):
        self.__owner = val

    @property
    def portable(self):
        return self.__portable


class Pit(Item):
    __portable = False  # override Item default

    __damage: int = 10

    def __init__(self):
        super().__init__()

    @property
    def damage(self):
        return self.__damage


class Bomb(Item):
    __damage: int = 10

    def __init__(self):
        super().__init__()

    @property
    def damage(self):
        return self.__damage


class Potion(Item, metaclass=ABCMeta):
    """ Abstract base class for potions.
     At present, nothing to distinguish it from Item base class,
     except as a logical superclass of only the Potion classes.
     """
    def __init__(self):
        super().__init__()


class VisionPotion(Potion):
    __radius: int = 1

    def __init__(self):
        super().__init__()

    @property
    def radius(self):
        return self.__radius


class HealthPotion(Potion):
    __points: int = 10

    def __init__(self):
        super().__init__()

    @property
    def points(self):
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

    def __init__(self, name: str):
        super().__init__()
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
        return self.__abbr

    @property
    def name(self):
        return self.__name

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"


Abstraction = Pillar('Abstraction')
Encapsulation = Pillar('Encapsulation')
Inheritance = Pillar('Inheritance')
Polymorphism = Pillar('Polymorphism')
Pillars = (Abstraction, Encapsulation, Inheritance, Polymorphism)


if __name__ == '__main__':

    def example():
        # TODO pit
        # TODO bomb
        # TODO potions
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
