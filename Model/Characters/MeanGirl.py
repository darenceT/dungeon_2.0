# from .Monster import Monster
from Model.Characters.Monster import Monster


class MeanGirl(Monster):
    """
    TODO docstrings
    """
    def __init__(self, mtype, name, hit_points=100, attack_speed=7, chance_to_hit=0.9,
                 minimum_damage=10, maximum_damage=30, chance_to_heal=0.6, minimum_heal_points=10,
                 maximum_heal_points=30):
        super().__init__(mtype, name, hit_points, attack_speed, chance_to_hit,
                         minimum_damage, maximum_damage, chance_to_heal, minimum_heal_points, maximum_heal_points)
