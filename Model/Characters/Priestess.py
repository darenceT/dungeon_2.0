from .Hero import Hero
from .Healable import Healable
# from Hero import Hero
# from Healable import Healable

class Priestess(Hero, Healable):
    def __init__(self, hero_type='priest', name="Lena", hit_points=75, hit_points_max=120, attack_speed=5, chance_to_hit=.7,
                 minimum_damage=25, maximum_damage=45, chance_to_block=.3, chance_to_heal=0.5, minimum_heal_points=30,
                 maximum_heal_points=50, game=None):
        super().__init__(hero_type, name, hit_points, hit_points_max, attack_speed, chance_to_hit,
                         minimum_damage, maximum_damage, chance_to_block, game=game)
        Healable.__init__(self, chance_to_heal, minimum_heal_points, maximum_heal_points)
        self.__special_skill = 'Heal'
        
    def special_skill(self):
        mana_cost = 15
        
        if self.special_mana > mana_cost and self.hit_points_max - self.hit_points > 5:
            self.special_mana = False
            self.hit_points += 20
            if self.hit_points > self.hit_points_max:   
                self.hit_points = self.hit_points_max
            return 'You healed yourself by 20 points!'

if __name__ == '__main__':
    p = Priestess()
    print(p)