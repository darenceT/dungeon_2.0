from .Hero import Hero


class Warrior(Hero):
    """
    TODO docstrings
    """
    def __init__(self, hero_type='warrior', name="Xena", hit_points=125, hit_points_max=150, attack_speed=3, chance_to_hit=.8,
                 minimum_damage=35, maximum_damage=60, chance_to_block=.2, game=None ):
        super().__init__(hero_type, name, hit_points, hit_points_max, attack_speed, chance_to_hit,
                 minimum_damage, maximum_damage, chance_to_block, game=game)
        self.__special_skill = 'Crushing Blow'

    def special_skill(self):
        """
        Crushing blow. First check if can_use (in hero class),
        then returns caller (in Arena) damage effect to monster and memo message
        :return: damage to monster, and memo message
        :rtype: tuple of int and str 
        """
        if self.can_use_special:
            self.special_mana = False   # decreases mana
            return (100, 'Aiyaaaaaaaa, Crushing Blow!')

if __name__ == '__main__':
    t = Warrior()
    print(t)