from random import random, randrange

class Arena:
    """
    Hero's fighting arena. Allows hero to practice special skill
    and to engage in enemy when nearby (via hero to sprite distance calculation in Sprites class).
    """
    COOL_DOWN = 5
    def __init__(self, player_controls, hero, memo):
        self.__player_crtl = player_controls
        self.__hero = hero
        self.__memo = memo
        self.__fight_timer = 0
        self.__sp_skill_timer = -15
        self.__attack_speed = hero.attack_speed / 3
        self.__hit_chance = hero.chance_to_hit  
        self.__min_dmg = int(hero.minimum_damage  / 4)    
        self.__max_dmg = int(hero.maximum_damage  / 4)  
        self.__block_chance = hero.chance_to_block

    def fight(self, monster=None):
        """
        Let the hero and monster clash, battle of stats
        Monster is optional for fight as hero can 
        practice weapon or special while alone
        :return: None
        TODO: currently attack speed is a damage modifier, will need to modify to time-based
        """
        if monster is not None:
            monst_speed = monster.attack_speed
            monst_hit_chance = monster.chance_to_hit
            monst_min_dmg = monster.minimum_damage
            monst_max_dmg = monster.maximum_damage
            #TODO create monster self heal
            monst_heal_chance = monster.chance_to_heal
            monst_heal_min = monster.minimum_heal_points
            monst_heal_max = monster.maximum_heal_points

            if self.__fight_timer < Arena.COOL_DOWN:
                self.__fight_timer += 1
            else:
                if self.__player_crtl.attacking:
                    if random() < self.__hit_chance:
                        hero_dmg = randrange(self.__min_dmg, self.__max_dmg) * self.__attack_speed
                        monster.hit_points -= hero_dmg
                        print(f"{self.__hero.name} hit {monster.mtype} for {hero_dmg}")
                    else:
                        print(f"{self.__hero.name} attack missed {monster.mtype}")
                if random() > self.__block_chance and random() < monst_hit_chance:
                    monst_dmg = randrange(monst_min_dmg, monst_max_dmg) * monst_speed   
                    self.__hero.hit_points -= monst_dmg
                    print(f"{monster.mtype}'s attack caused {self.__hero.name} to lose {monst_dmg} health")
                else:
                    print(f"{monster.mtype} attack missed {self.__hero.name}")
                self.__fight_timer = 0

        #TODO refactor duplicate code 59-61 and 68-70.
        # problem occurs with delaying effect of special skill as 
        # using it alone loops this method only once while with monster loops many times
        if self.__player_crtl.special_skill_execute:
            if self.__player_crtl.fight_alone:
                hero_sp_dmg, msg = self.__hero.special_skill()
                self.__memo.new_message(msg)
                self.__player_crtl.special_skill_execute = False

            # create short delay before effects of special skill
            else:
                if self.__sp_skill_timer < Arena.COOL_DOWN:
                    self.__sp_skill_timer += 1
                else:
                    hero_sp_dmg, msg = self.__hero.special_skill()
                    self.__memo.new_message(msg)
                    self.__player_crtl.special_skill_execute = False
                    monster.hit_points -= hero_sp_dmg
                    if hero_sp_dmg > 0:
                        self.__memo.new_message(f'Special attack landed on {monster.mtype}')
                        print(f"{self.__hero.name} special attack took out {monster.mtype}'s health by {hero_sp_dmg}")
                    if not monster.is_alive:
                        self.__memo.new_message(f'Defeated a {monster.mtype} monster!')
                    self.__sp_skill_timer = -15


