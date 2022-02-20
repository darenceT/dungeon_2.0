from Monster import *

class Ogre(Monster):
    def __init__(self, game, name, hit_points, hit_points_max, attack_speed, attack_behavior, chance_to_hit,
                 minimum_damage, maximum_damage, chance_to_heal, minimum_heal_points, maximum_heal_points):
        super().__init__(game, name, hit_points, hit_points_max, attack_speed, attack_behavior, chance_to_hit,
                 minimum_damage, maximum_damage, chance_to_heal, minimum_heal_points, maximum_heal_points)
        self.__hit_points = 200
        self.__attack_speed = 2
        self.__chance_to_hit = 0.6
        self.__minimum_damage = 30
        self.__maximum_damage = 60
        self.__chance_to_heal = 0.1
        self.__minimum_heal_points = 30
        self.__maximum_heal_points = 60
