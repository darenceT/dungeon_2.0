from Monster import *

class MeanGirl(Monster):
    def __init__(self, game, name, hit_points, hit_points_max, attack_speed, attack_behavior, chance_to_hit,
                 minimum_damage, maximum_damage, chance_to_heal, minimum_heal_points, maximum_heal_points):
        super().__init__(game, name, hit_points, hit_points_max, attack_speed, attack_behavior, chance_to_hit,
                 minimum_damage, maximum_damage, chance_to_heal, minimum_heal_points, maximum_heal_points)
        self.__hit_points = 100
        self.__attack_speed = 7
        self.__chance_to_hit = 0.9
        self.__minimum_damage = 10
        self.__maximum_damage = 30
        self.__chance_to_heal = 0.6
        self.__minimum_heal_points = 30
        self.__maximum_heal_points = 50