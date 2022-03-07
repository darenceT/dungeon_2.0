class Adventurer:
    """
    Our brave hero. Sets up and updates game player, their inventory, potions and hit points.
    """
    default_hit_points_initial = 80
    default_hit_points_max = 100

    def __init__(self, game=None, name: str = None, hit_points: int = None, hit_points_max: int = None):
        """
        Initializes Adventurer Class
        :param game: initializes game
        :param name: initializes name as a string
        :param hit_points: initializes hit points as an integer
        :param hit_points_max:
        """
        self.__game = game
        self.__name: str = name
        self.__hit_points: int = hit_points
        self.__hit_points_max: int = hit_points_max
        self.__healing_potions: int = 0
        self.__vision_potions: int = 0
        self.__pillars: set = set()  # empty

    @property
    def name(self) -> str:
        """
        Gets the name
        :return:
        """
        return self.__name

    @name.setter
    def name(self, val: str) -> None:
        """
        Sets the name according to the value provided
        :param val: The value provided by the player
        :return:
        """
        self.__name = val

    @property
    def game(self):
        """
        Gets the current game
        :return:
        """
        return self.__game

    @property
    def hit_points(self) -> int:
        """
        Gets the current hit points
        :return:
        """
        return self.__hit_points

    @hit_points.setter
    def hit_points(self, val: int) -> None:
        """
        Checks to see if there are current hit points, if not, sets them to the default beginning value
        :param val: current hit points, if any
        :return:
        """
        if val is not None:
            self.__hit_points = val
        elif self.game is not None:
            self.__hit_points = self.game.default_hit_points_initial

    @property
    def hit_points_max(self) -> int:
        """
        Returns the maximum value of allowed hit points
        :return:
        """
        return self.__hit_points_max

    @hit_points_max.setter
    def hit_points_max(self, val: int) -> None:
        """
        Checks to see if maximum value is already set, if not, sets default start value of maximum points.
        :param val: maximum value of allowed hit points
        :return:
        """
        if val is not None:
            self.__hit_points_max = val
        elif self.game is not None:
            self.__hit_points_max = self.game.default_hit_points_max

    @property
    def is_alive(self) -> bool:
        """
        Checks to see if our brave adventurer is still breathing, if current hit points greater than zero, returns True.
        :return:
        """
        return self.hit_points > 0

    @property
    def healing_potions(self) -> int:
        """
        Gets number of healing potions
        :return:
        """
        return self.__healing_potions

    @healing_potions.setter
    def healing_potions(self, val: int) -> None:
        """
        Sets number of healing potions
        :param val: current number of healing potions
        :return:
        """
        self.__healing_potions = val

    @property
    def vision_potions(self) -> int:
        """
        Gets number of healing potions
        :return:
        """
        return self.__vision_potions

    @vision_potions.setter
    def vision_potions(self, val: int) -> None:
        """
        Sets number of healing potions
        :param val: current number of healing potions
        :return:
        """
        self.__vision_potions = val

    @property
    def pillars(self) -> set:
        """
        Gets current pillars
        :return:
        """
        return self.__pillars

    def has_pillar(self, pillar):
        """
        Checks to see if a pillar has been collected, if so returns True
        :param pillar: One of the four pillars
        :return:
        """
        return bool(pillar in self.pillars)

    def display_inventory(self):
        """
        Displays the player's current inventory of items, and hit points
        :return:
        """
        # Keeps a list of items in inventory
        print(f"Name:    {self.name}")
        print(f"Health:  {self.hit_points}")
        print(f"Pillars: {', '.join(self.pillars)}")
        print(f"Potions...")
        print(f"Healing: {self.healing_potions}")
        print(f"Vision:  {self.vision_potions}")

    def take_damage(self, damage: int = 1) -> int:
        """
        Checks to see if damage has lowered hit points to zero or below, if so, ends game. If not, returns new
        number of hit points after damage.
        :param damage: number of hit points to subtract after falling into pit
        :return:
        """
        self.hit_points -= damage
        if self.hit_points <= 0:
            self.hit_points = 0
            self.game.continues = False
        return self.hit_points

    def gain_healing_potion(self,):
        """
        Increases the number of healing potions when Adventurer discovers one.
        :return:
        """
        self.healing_potions += 1

    def use_healing_potion(self, hit_points: int = 15) -> int:
        """
        Checks to see if Adventurer has any healing potions, if so, increases current hit points by 15 and subtracts
        1 from the number of healing potions in inventory.
        :param hit_points: number of hit points to increase after using vision potion
        :return:
        """
        if self.healing_potions <= 0:
            return -1
        self.healing_potions -= 1
        self.hit_points += hit_points
        if self.hit_points > self.hit_points_max:
            self.hit_points = self.hit_points_max
        return self.healing_potions

    def gain_vision_potion(self):
        """
        Increases number of visions potions when Adventurer discovers one.
        :return:
        """
        self.vision_potions += 1

    def use_vision_potion(self) -> int:
        """
        Checks to see if adventurer has any vision potions, if so adjusts visible rooms and decreases number of
        vision potions in inventory by one.
        :return:
        """
        if self.vision_potions <= 0:
            return -1
        self.vision_potions -= 1
        self.game.extend_vision()
        return self.vision_potions

    def gain_pillar(self, pillar_name):
        """
        Adds pillar to set of discovered pillars
        :param pillar_name: name of pillar discovered by adventurer
        :return:
        """
        self.pillars.add(pillar_name)

# END
