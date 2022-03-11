from abc import ABC

class Healable(ABC):

    def __init__(self, chance_to_heal, minimum_heal_points, maximum_heal_points):
        self.__chance_to_heal = chance_to_heal
        self.__minimum_heal_points = minimum_heal_points
        self.__maximum_heal_points = maximum_heal_points

    @property
    def chance_to_heal(self):
        return self.__chance_to_heal

    @property
    def minimum_heal_points(self):
        return self.__minimum_heal_points

    @property
    def maximum_heal_points(self):
        return self.__maximum_heal_points