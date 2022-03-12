from .Hero import Hero


class Thief(Hero):
    def __init__(self, hero_type='thief', name="Timmy", hit_points=75, hit_points_max=120, attack_speed=6, chance_to_hit=.8,
                 minimum_damage=20, maximum_damage=40, chance_to_block=.4, game=None):
        super().__init__(hero_type, name, hit_points, hit_points_max, attack_speed, chance_to_hit,
                 minimum_damage, maximum_damage, chance_to_block, game=game)
        self.__special_skill = 'Surprise Attack'

        def special_skill(self):
            pass

if __name__ == '__main__':
    t = Thief()
    print(t)