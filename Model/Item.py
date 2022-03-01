class Item:
    __fixed: bool = False

    def __init__(self):
        self.__owner = None


class Pit(Item):
    __fixed = True


class Bomb(Item):
    pass


class Potion(Item):
    pass


class VisionPotion(Potion):
    pass


class HealthPotion(Potion):
    pass

# END
