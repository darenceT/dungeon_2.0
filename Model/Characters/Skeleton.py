from .Monster import Monster


class Skeleton(Monster):
    """
     Initializes Skeleton, a subclass of Monster. Default field values provided for testing, but values are pulled from database.
    """
    def __init__(self, mtype, name, hit_points=100, attack_speed=3, chance_to_hit=0.8,
                 minimum_damage=30, maximum_damage=50, chance_to_heal=0.3, minimum_heal_points=30,
                 maximum_heal_points=50):
        super().__init__(mtype, name, hit_points, attack_speed, chance_to_hit,
                         minimum_damage, maximum_damage, chance_to_heal, minimum_heal_points, maximum_heal_points)
