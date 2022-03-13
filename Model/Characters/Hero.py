from .DungeonCharacter import DungeonCharacter
# from DungeonCharacter import DungeonCharacter

class Hero(DungeonCharacter):
    def __init__(self, hero_type, name, hit_points, hit_points_max, attack_speed, chance_to_hit,
                 minimum_damage, maximum_damage, chance_to_block, game=None):
        super().__init__(name, hit_points, hit_points_max, attack_speed, chance_to_hit,
                 minimum_damage, maximum_damage)  
        self.__game = game
        self.__hero_type = hero_type
        self.__chance_to_block = chance_to_block
        self.__special_mana: int = 10
        self.__vision_potions: int = 0
        self.__healing_potions: int = 0
        self.__vision_potions: int = 0
        self.__pillars: set = set()  # empty

    @property
    def special_mana(self):
        return self.__special_mana
    
    @special_mana.setter
    def special_mana(self, add=True):
        if isinstance(add, bool):
            if add:
                self.__special_mana += 2
                if self.__special_mana > 50:
                    self.__special_mana = 50
            else:
                self.__special_mana -= 15
                if self.__special_mana < 0:
                    self.__special_mana = 0
        else:
            raise TypeError('Can only accept boolean type')

    @property
    def game(self):
        """
        Gets the current game
        :return:
        """
        return self.__game

    @property
    def hero_type(self):
        return self.__hero_type

    def take_damage(self, damage: int = 1) -> int:
        """
        Checks to see if damage has lowered hit points to zero or below, if so, ends game. If not, returns new
        number of hit points after damage.
        :param damage: number of hit points to subtract after falling into pit
        :return:
        """
        # Consider moving this to DungeonCharacter. Then adding the heal capability for monster.
        # Could also use Factory to create each sub type character
        # don't declare the same data again, shadowing
        self.hit_points -= damage
        if self.hit_points <= 0:
            self.hit_points = 0
            self.__game.continues = False
        return self.hit_points


    def special_skill(self) -> None:
        pass

    @property
    def chance_to_block(self) -> float:
        return self.__chance_to_block

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
        print(f"Name:    {self.__name}")
        print(f"Health:  {self.__hit_points}")
        print(f"Pillars: {', '.join(self.pillars)}")
        print(f"Potions...")
        print(f"Healing: {self.healing_potions}")
        print(f"Vision:  {self.vision_potions}")

    def gain_healing_potion(self, ):
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
        self.__game.extend_vision()
        return self.vision_potions

    def gain_pillar(self, pillar_name):
        """
        Adds pillar to set of discovered pillars
        :param pillar_name: name of pillar discovered by adventurer
        :return:
        """
        self.pillars.add(pillar_name)

    def __str__(self):
        return f"""
{self.__hero_type.capitalize()} named {self.name}
Stats:
Health Points: {self.hit_points}
Max Health: {self.hit_points_max}
Special Mana: {self.__special_mana}
Attack speed: {self.attack_speed}
Chance to hit: {self.chance_to_hit}
Mininum damage: {self.minimum_damage}
Maximum damage: {self.maximum_damage}
"""