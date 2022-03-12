from random import random, randrange

class Arena:
    def __init__(self, sound, player_controls, hero):
        self.sound = sound
        self.player_controls = player_controls
        self.hero = hero
        self.cool_down = 5
        self.count = 0
        self.attack_speed = 4 / 4   # will be from hero
        self.chance_to_hit = 0.8    # will be from hero
        self.min_damage = 35        # will be from hero
        self.max_damage = 60        # will be from hero
        self.chance_to_block = 0.2  # will be from hero

    def fight(self, monster):
        """
        Let the hero and monster stats clash.
        TODO: convert attack speed to time-based using pygame.get_ticks() 
        """

        if self.count < self.cool_down:
            self.count += 1
        else:
            if self.player_controls.attacking and random() < self.chance_to_hit:

                monster.hitpoint -= randrange(self.min_damage, self.max_damage) * self.attack_speed
            if random() > self.chance_to_block and random() < 0.6: 
                    
                self.hero.hit_points -= randrange(30, 60) * 2 / 40  # min, max, speed(2) from monster
            self.count = 0

"""
 Ogre:
 hit_points=200, attack_speed=2, chance_to_hit=0.6,
                 minimum_damage=30, maximum_damage=60

"""