from .Hero import Hero


class Warrior(Hero):

    def __init__(self, hero_type='warrior', name="Xena", hit_points=125, hit_points_max=150, attack_speed=4, chance_to_hit=.8,
                 minimum_damage=35, maximum_damage=60, chance_to_block=.2, game=None ):
        super().__init__(name, hero_type, hit_points, hit_points_max, attack_speed, chance_to_hit,
                 minimum_damage, maximum_damage, chance_to_block, game=game)
        self.__special_skill = 'Crushing Blow'

        def special_skill(self):
            pass

if __name__ == '__main__':
    t = Warrior()
    print(t)