from DungeonCharacter import *
from Healable import *


class Monster(ABC, DungeonCharacter):
    def __init__(self, game, name, hit_points, hit_points_max, attack_speed, attack_behavior, chance_to_hit,
                 minimum_damage, maximum_damage, chance_to_heal, minimum_heal_points, maximum_heal_points):
        super().__init__(game, name, hit_points, hit_points_max, attack_speed, attack_behavior, chance_to_hit,
                 minimum_damage, maximum_damage, chance_to_heal, minimum_heal_points, maximum_heal_points)




from DungeonCharacter import *
from Healable import *


class Monster(ABC, DungeonCharacter):
    def __init__(self, game, name, hit_points, hit_points_max, attack_speed, attack_behavior, chance_to_hit,
                 minimum_damage, maximum_damage, chance_to_heal, minimum_heal_points, maximum_heal_points):
        super().__init__(game, name, hit_points, hit_points_max, attack_speed, attack_behavior, chance_to_hit,
                 minimum_damage, maximum_damage, chance_to_heal, minimum_heal_points, maximum_heal_points)

