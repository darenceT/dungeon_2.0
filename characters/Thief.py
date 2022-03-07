from Hero import *


class Thief(Hero):
    def __init__(self, game, name, hit_points, hit_points_max, attack_speed, attack_behavior, chance_to_hit,
                 minimum_damage, maximum_damage, chance_to_block, special_skill):
        super().__init__(self, game, name, hit_points, hit_points_max, attack_speed, attack_behavior, chance_to_hit,
                         minimum_damage, maximum_damage, chance_to_block, special_skill)
        self.__hit_points = 75
        self.__attack_speed = 6
        self.__chance_to_hit = .8
        self.__minimum_damage = 20
        self.__maximum_damage = 40
        self.__chance_to_block = .4
        self.__special_skill = 'Surprise Attack'
