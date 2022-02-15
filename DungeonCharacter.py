from abc import ABC, abstractmethod

class DungeonCharacter(ABC):

    def name(self):
        pass

    def game(self):
        pass

    def hit_points(self):
        pass

    def hit_points_max(self):
        pass

    def is_alive(self):
        pass

    def take_damage(self):
        pass

    def damage_range(self):
        pass

    def attack_speed(self):
        pass

    def chance_to_hit(self):
        pass

    def attack_behavior(self):
        pass




# END