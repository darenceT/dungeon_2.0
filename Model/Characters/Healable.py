from abc import ABC

class Healable(ABC):
    """
    Initializes Healable, utilized by the Monster classes and Priestess hero subclass. Establishes a chance to heal, minimum and maximum heal points.
    """
    def __init__(self, chance_to_heal, minimum_heal_points, maximum_heal_points):
        self.__chance_to_heal = chance_to_heal
        self.__minimum_heal_points = minimum_heal_points
        self.__maximum_heal_points = maximum_heal_points

    @property
    def chance_to_heal(self):
        """
        Gets chance to heal
        :return: chance to heal
        """
        return self.__chance_to_heal

    @property
    def minimum_heal_points(self):
        """
        Gets minimum heal points
        :return: minimum heal points
        """
        return self.__minimum_heal_points

    @property
    def maximum_heal_points(self):
        """
        Gets maximum heal points
        :return: maximum heal points
        """
        return self.__maximum_heal_points
