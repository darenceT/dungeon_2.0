from Model.Characters.Hero import Hero


class Thief(Hero):
    """
    TODO docstrings
    """
    def __init__(self, name: str = "Timmy",
                 hit_points: int = 75, hit_points_max: int = 120,
                 attack_speed: int = 6, chance_to_hit: float = .8,
                 minimum_damage: int = 25, maximum_damage: int = 45,
                 chance_to_block: float = .4, game=None):
        guild: str = self.__class__.__name__
        super().__init__(guild=guild, name=name,
                         hit_points=hit_points, hit_points_max=hit_points_max,
                         attack_speed=attack_speed, chance_to_hit=chance_to_hit,
                         minimum_damage=minimum_damage, maximum_damage=maximum_damage,
                         chance_to_block=chance_to_block, game=game)
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

# END
