from Hero import *
from Healable import *


class Priestess(Hero, Healable):
    def __init__(self, game, name, hit_points, attack_speed, chance_to_hit,
                 minimum_damage, maximum_damage, chance_to_block, special_skill, chance_to_heal, minimum_heal_points,
                 maximum_heal_points):
        super().__init__(self, game, name, hit_points, attack_speed, chance_to_hit,
                         minimum_damage, maximum_damage, chance_to_block, special_skill)
        super().__init__(self, chance_to_heal, minimum_heal_points, maximum_heal_points)
        self.__hit_points = 75
        self.__attack_speed = 5
        self.__chance_to_hit = .7
        self.__minimum_damage = 25
        self.__maximum_damage = 45
        self.__chance_to_block = 0.3
        self.__special_skill = 'Heal'
        self.__chance_to_heal = 0.5
        self.__minimum_heal_points = 30
        self.__maximum_heal_points = 50
        
