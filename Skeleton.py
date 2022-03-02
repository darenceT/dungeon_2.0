from Monster import *
from Healable import *


class Gremlin(Monster):
    def __init__(self, game, name, hit_points=70, attack_speed=5, chance_to_hit=0.8,
                 minimum_damage=15, maximum_damage=30, chance_to_heal=0.4, minimum_heal_points=20, maximum_heal_points=40):
        super().__init__(game, name, hit_points, attack_speed, chance_to_hit,
                         minimum_damage, maximum_damage, chance_to_heal, minimum_heal_points, maximum_heal_points)
