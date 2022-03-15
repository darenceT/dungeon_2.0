from random import random, randrange

class Arena:
    """
    Hero's fighting arena. Allows hero to practice special skill
    and to engage in enemy when nearby (via hero to sprite distance calculation in Sprites class).
    """
    def __init__(self, player_controls, hero, memo):
        self.__player_controls = player_controls
        self.__hero = hero
        self.__memo = memo
        self.__cool_down = 5
        self.__fight_timer = 0
        self.__sp_skill_timer = -15
        self.attack_speed = 4 / 4   # will be from hero
        self.chance_to_hit = 0.8    # will be from hero
        self.min_damage = int(hero.minimum_damage  /4)      # will be from hero
        self.max_damage = int(hero.maximum_damage  /4)       # will be from hero
        self.chance_to_block = 0.2  # will be from hero

    def fight(self, monster=None):
        """
        Let the hero and monster clash, battle of stats
        Monster is optional for fight as hero can 
        practice weapon or special while alone
        TODO print combat log, hero and monster attack stats into terminal
        """
        #TODO refactor duplicate code 31-33 and 40-42.
        # problem occurs with delaying effect of special skill as 
        # using it alone loops this method only once while with monster loops many times
        if self.__player_controls.special_skill_execute:
            if self.__player_controls.fight_alone:
                hero_sp_dmg, msg = self.__hero.special_skill()
                self.__memo.new_message(msg)
                self.__player_controls.special_skill_execute = False

            # create short delay before effects of special skill
            else:
                if self.__sp_skill_timer < self.__cool_down:
                    self.__sp_skill_timer += 1
                else:
                    hero_sp_dmg, msg = self.__hero.special_skill()
                    self.__memo.new_message(msg)
                    self.__player_controls.special_skill_execute = False
                    monster.hit_points -= hero_sp_dmg
                    self.__sp_skill_timer = -15

        # timer to slow down fighting
        if monster is not None:
            if self.__fight_timer < self.__cool_down:
                self.__fight_timer += 1
            else:
                if self.__player_controls.attacking and random() < self.chance_to_hit:
                    monster.hit_points -= randrange(self.min_damage, self.max_damage) * self.attack_speed
                if random() > self.chance_to_block and random() < monster.chance_to_hit: 
                    self.__hero.hit_points -= randrange(monster.minimum_damage, monster.maximum_damage) * 2 / 40  # min, max, speed(2) from monster
                self.__fight_timer = 0
