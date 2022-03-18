from Model.Characters.Hero import Hero


class Warrior(Hero):
    """
    Initializes Warrior class. Warrior is a subclass of Hero.
    """
    def __init__(self, name: str = 'Xena',
                 hit_points: int = 125, hit_points_max: int = 150,
                 attack_speed: int = 3, chance_to_hit: float = .8,
                 minimum_damage: int = 35, maximum_damage: int = 60,
                 chance_to_block: float = .2, game=None ):
        guild: str = self.__class__.__name__
        super().__init__(guild=guild, name=name,
                         hit_points=hit_points, hit_points_max=hit_points_max,
                         attack_speed=attack_speed, chance_to_hit=chance_to_hit,
                         minimum_damage=minimum_damage, maximum_damage=maximum_damage,
                         chance_to_block=chance_to_block, game=game)
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

# END
