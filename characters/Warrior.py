from Hero import *


class Warrior(Hero):

    def __init__(self, game, name, hit_points, hit_points_max, attack_speed, attack_behavior, chance_to_hit,
                 minimum_damage, maximum_damage, chance_to_block, special_skill):
        super().__init__(self, game, name, hit_points, hit_points_max, attack_speed, attack_behavior, chance_to_hit,
                 minimum_damage, maximum_damage, chance_to_block, special_skill)
        self.__hit_points = 125
        self.__attack_speed = 4
        self.__chance_to_hit = .8
        self.__minimum_damage = 35
        self.__maximum_damage = 60
        self.__chance_to_block = .2
        self.__special_skill = 'Crushing Blow'