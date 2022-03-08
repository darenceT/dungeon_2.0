from abc import ABC, abstractmethod


class DungeonCharacter(ABC):

    def __init__(self, game, name, hit_points, attack_speed, chance_to_hit,
                 minimum_damage, maximum_damage):
        self.__game = game
        self.__name: str = name
        self.__hit_points: int = hit_points
        self.__attack_speed: int = attack_speed
        self.__chance_to_hit: float = chance_to_hit
        self.__minimum_damage: int = minimum_damage
        self.__maximum_damage: int = maximum_damage

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
    def is_alive(self) -> bool:
        """
        Checks to see if our brave adventurer is still breathing, if current hit points greater than zero, returns True.
        :return:
        """
        return self.hit_points > 0

    @property
    def minimum_damage(self):
        return self.__minimum_damage

    @minimum_damage.setter
    def minimum_damage(self, val: int) -> None:
        """
        Checks to see if maximum value is already set, if not, sets default start value of maximum points.
        :param val: maximum value of allowed hit points
        :return:
        """
        if val is not None:
            self.__minimum_damage = val
        elif self.game is not None:
            self.__minimum_damage = self.game.default_minimum_damage

    @property
    def maximum_damage(self):
        return self.maximum_damage

    @maximum_damage.setter
    def maximum_damage(self, val: int) -> None:
        """
        Checks to see if maximum value is already set, if not, sets default start value of maximum points.
        :param val: maximum value of allowed hit points
        :return:
        """
        if val is not None:
            self.__maximum_damage = val
        elif self.game is not None:
            self.__maximum_damage = self.game.default_maximum_damage

    @property
    def attack_speed(self):
        return self.__attack_speed

    @attack_speed.setter
    def attack_speed(self, val: int) -> None:
        """
        Checks to see if maximum value is already set, if not, sets default start value of maximum points.
        :param val: maximum value of allowed hit points
        :return:
        """
        if val is not None:
            self.__attack_speed = val
        elif self.game is not None:
            self.__attack_speed = self.game.default_attack_speed

    @property
    def chance_to_hit(self):
        return self.__chance_to_hit

    @chance_to_hit.setter
    def chance_to_hit(self, val: float) -> None:
        """
        Checks to see if maximum value is already set, if not, sets default start value of maximum points.
        :param val: maximum value of allowed hit points
        :return:
        """
        if val is not None:
            self.__chance_to_hit = val
        elif self.game is not None:
            self.__chance_to_hit = self.game.chance_to_hit

# END