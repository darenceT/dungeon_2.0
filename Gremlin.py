from Monster import *


class Gremlin(Monster):
    def __init__(self, game, name, hit_points, hit_points_max, attack_speed, attack_behavior, chance_to_hit,
                 minimum_damage, maximum_damage, chance_to_heal, minimum_heal_points, maximum_heal_points):
        super().__init__(game, name, hit_points, hit_points_max, attack_speed, attack_behavior, chance_to_hit,
                         minimum_damage, maximum_damage, chance_to_heal, minimum_heal_points, maximum_heal_points)
        self.__hit_points = 70
        self.__attack_speed = 5
        self.__chance_to_hit = 0.8
        self.__minimum_damage = 15
        self.__maximum_damage = 30
        self.__chance_to_heal = 0.4
        self.__minimum_heal_points = 20
        self.__maximum_heal_points = 40
