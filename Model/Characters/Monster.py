# from .DungeonCharacter import DungeonCharacter
# from .Healable import Healable
from Model.Characters.DungeonCharacter import DungeonCharacter
from Model.Characters.Healable import Healable


class Monster(DungeonCharacter, Healable):
    """
    Base class for all monsters, inherits from DungeonCharacter and Healable
    """
    def __init__(self, mtype, name, hit_points, attack_speed, chance_to_hit,
                 minimum_damage, maximum_damage, chance_to_heal, minimum_heal_points, maximum_heal_points):
        super().__init__(name, hit_points, hit_points, attack_speed, chance_to_hit,
                 minimum_damage, maximum_damage) 
        '''
        (delete upon receiving this message) 2nd super is for Healable, 
        first param "DungeonCharacter" causes super to skip over DungeonCharacter
        '''
        super(DungeonCharacter, self).__init__(chance_to_heal, minimum_heal_points, maximum_heal_points)
        self.__mtype = mtype

    @property
    def mtype(self):
        """
        gets the monster type
        :return: mtype
        """
        return self.__mtype

    def __str__(self):
        """
        Returns a string representation of the monster's stats.
        :return: string
        """
        return f"""
{self.mtype.capitalize()} named {self.name}
Stats:
Health Points: {self.hit_points}
Max Health: {self.hit_points_max}
Attack speed: {self.attack_speed}
Chance to hit: {self.chance_to_hit}
Mininum damage: {self.minimum_damage}
Maximum damage: {self.maximum_damage}
Chance to Heal: {self.chance_to_heal}
Minimum healing points: {self.minimum_heal_points}
Maximum healing points: {self.maximum_heal_points}
"""
