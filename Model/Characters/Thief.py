from .Hero import Hero


class Thief(Hero):
    """
    TODO docstrings
    """
    def __init__(self, hero_type='thief', name="Timmy", hit_points=75, hit_points_max=120, attack_speed=6, chance_to_hit=.8,
                 minimum_damage=25, maximum_damage=45, chance_to_block=.4, game=None):
        super().__init__(hero_type, name, hit_points, hit_points_max, attack_speed, chance_to_hit,
                 minimum_damage, maximum_damage, chance_to_block, game=game)
        self.__special_skill = 'Surprise Attack'

    def special_skill(self):
        """
        Shower of daggers. First check if can_use (in hero class),
        then returns caller (in Arena) damage effect to monster and memo message
        :return: damage to monster, and memo message
        :rtype: tuple of int and str 
        """
        if self.can_use_special:
            self.special_mana = False   # decreases mana
            return (80, 'Your Surprise Attack: Triple Daggers!')

if __name__ == '__main__':
    t = Thief()
    print(t)