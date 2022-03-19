from abc import abstractclassmethod
from Model.Characters.DungeonCharacter import DungeonCharacter


class Hero(DungeonCharacter):
    """
    Abstract class that thief, priestess and warrior class will inherit from.
    This abstract class is a child of abstract class DungeonCharacter
    """
    def __init__(self, name: str = 'Sir Robin', guild: str = 'Coward',
                 hit_points: int = 2, hit_points_max: int = 5,
                 attack_speed: int = 1, chance_to_hit: float = 0.1,
                 minimum_damage: int = 1, maximum_damage: int = 2,
                 chance_to_block: float = 0.1, game=None):
        super().__init__(name=name, hit_points=hit_points, hit_points_max=hit_points_max,
                         attack_speed=attack_speed, chance_to_hit=chance_to_hit,
                         minimum_damage=minimum_damage, maximum_damage=maximum_damage)
        self.__game = game
        self.__guild = guild
        self.__chance_to_block = chance_to_block
        self.__special_mana: int = 10
        self.__vision_potions: int = 0
        self.__healing_potions: int = 0
        self.__vision_potions: int = 0
        self.__pillars: set = set()  # empty

    def display_inventory(self):
        """
        prints string representation of all Hero inventory items and stats
        :return: None
        """
        print(f'name:          {self.name}',
              f'guild:         {self.guild}',
              f'hit points:    {self.hit_points} (max: {self.hit_points_max})',
              f'attack speed:  {self.attack_speed}',
              f'attack chance: {self.chance_to_hit}',
              f'attack damage: {self.minimum_damage}-{self.maximum_damage}',
              f'block chance:  {self.chance_to_block}',
              f'special mana:  {self.special_mana}',
              f'vision potion: {self.vision_potions}',
              f'health potion: {self.healing_potions}',
              f'pillars seen:  {self.pillars}',
              sep='\n')

    @property
    def guild(self):
        """
        Gets Hero's Guild
        :return: guild
        """
        return self.__guild

    @property
    def special_mana(self):
        """
        Gets Hero's "mana," special property that determines if Hero is strong enough to use special skill
        :return: specical_mana
        """
        return self.__special_mana
    
    @special_mana.setter
    def special_mana(self, add=True):
        """
        Allows change to mana by boolean, increase ticking by GUI timer in Drawing.py
        and decrease by use in child hero classes
        """
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
        :return: game
        """
        return self.__game

    #@abstractclassmethod
    def special_skill(self) -> None:
        """
        abstract method for which priestess, thief and warriors will have implementation
        """
        pass

    @property
    def chance_to_block(self) -> float:
        """
        Gets hero's chance to block
        :return: chance_to_block
        """
        return self.__chance_to_block

    @property
    def healing_potions(self) -> int:
        """
        Gets number of healing potions
        :return: healing_potions
        """
        return self.__healing_potions

    @healing_potions.setter
    def healing_potions(self, val: int) -> None:
        """
        Sets number of healing potions
        :param val: current number of healing potions
        :return: None
        """
        self.__healing_potions = val

    @property
    def vision_potions(self) -> int:
        """
        Gets number of healing potions
        :return: vision_potions
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
        :return: pillars
        """
        return self.__pillars

    def can_use_special(self):
        """
        Check to see if hero has enough mana to use special skill
        Special case to check HP if hero is priestess
        :return: ready (boolean)
        """
        if self.__guild == "priestess" and self.__special_mana >= 15:
            ready = self.hit_points_max - self.hit_points > 5
        else:
            ready = self.__special_mana >= 15
        return ready

    def has_pillar(self, pillar):
        """
        Checks to see if a pillar has been collected, if so returns True
        :param pillar: One of the four pillars
        :return: boolean
        """
        return bool(pillar in self.pillars)

    def gain_healing_potion(self, ):
        """
        Increases the number of healing potions when Adventurer discovers one.
        :return: None
        """
        self.healing_potions += 1

    def use_healing_potion(self, hit_points: int = 15) -> int:
        """
        Checks to see if Adventurer has any healing potions, if so, increases current hit points by 15 and subtracts
        1 from the number of healing potions in inventory.
        :param hit_points: number of hit points to increase after using vision potion
        :return: healing_potions
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
        :return: vision_potions
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
        :return: None
        """
        self.pillars.add(pillar_name)

    def __str__(self):
        """
        String representation of Hero name
        :returns: string
        """
        return f"{self.guild}({self.name})"


if __name__ == '__main__':
    def example():
        p = Hero()
        print(p)

    example()

# END
