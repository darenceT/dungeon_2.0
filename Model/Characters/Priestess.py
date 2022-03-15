from Model.Characters.Hero import Hero
from Model.Characters.Healable import Healable


class Priestess(Hero, Healable):
    """
    TODO docstrings
    """
    def __init__(self, name: str = "Lena",
                 hit_points: int = 75, hit_points_max: int = 120,
                 attack_speed: int = 5, chance_to_hit: float = .7,
                 minimum_damage: int = 25, maximum_damage: int = 45,
                 chance_to_block: int = .3,
                 chance_to_heal: int = 0.5,
                 minimum_heal_points: int = 30, maximum_heal_points: int = 50,
                 game=None):
        guild: str = self.__class__.__name__
        super().__init__(guild=guild, name=name,
                         hit_points=hit_points, hit_points_max=hit_points_max,
                         attack_speed=attack_speed, chance_to_hit=chance_to_hit,
                         minimum_damage=minimum_damage, maximum_damage=maximum_damage,
                         chance_to_block=chance_to_block, game=game)
        Healable.__init__(self, chance_to_heal=chance_to_heal,
                          minimum_heal_points=minimum_heal_points,
                          maximum_heal_points=maximum_heal_points)
        self.__special_skill = 'Heal'
        
    def special_skill(self):
        """
        Use special skill of healing. First check if can_use (in hero class),
        heals self, returns caller (in Arena) damage effect to monster and memo message
        :return: damage to monster, and memo message
        :rtype: tuple of int and str 
        """
        if self.can_use_special:
            self.special_mana = False   # decreases mana
            self.hit_points += 20
            if self.hit_points > self.hit_points_max:   
                self.hit_points = self.hit_points_max
            return (0, 'You healed yourself by 20 points!')


if __name__ == '__main__':
    p = Priestess()
    print(p)

# END
