from typing import Union

# from .Ogre import Ogre
# from .Skeleton import Skeleton
# from .Gremlin import Gremlin
# from .MeanGirl import MeanGirl
from Model.Characters.Ogre import Ogre
from Model.Characters.Skeleton import Skeleton
from Model.Characters.Gremlin import Gremlin
from Model.Characters.MeanGirl import MeanGirl


class MonsterFactory:

    @staticmethod
    def create_monster(mtype: str, name: str, hit_points: int, attack_speed: int,
                       chance_to_hit: float, minimum_damage: int, maximum_damage: int, chance_to_heal: float,
                       minimum_heal_points: int, maximum_heal_points: int) -> Union[Ogre, Skeleton, Gremlin, MeanGirl]:
        """
        Creates a monster of the specified type using the necessary data
        for building that monster and returns that monster. e.g.:
        my_monster = MonsterFactory.create_monster("Skeleton", hit_points etc...),
        :param mtype: Name of a Monster subclass.
        :param monster_data: stats for the relevant monster.
        :return: newly created monster
        """
        if mtype == "ogre":
            maker = MonsterFactory.create_ogre
        elif mtype == "skeleton":
            maker = MonsterFactory.create_skeleton
        elif mtype == "gremlin":
            maker = MonsterFactory.create_gremlin
        elif mtype == "mgirl":
            maker = MonsterFactory.create_meangirl
        else:
            raise ValueError(f"does not support monster_name {mtype}")
        monster = maker(mtype, name, hit_points, attack_speed,
                       chance_to_hit, minimum_damage, maximum_damage, chance_to_heal,
                       minimum_heal_points, maximum_heal_points)
        return monster

    @staticmethod
    def create_ogre(mtype, name, hit_points, attack_speed,
                       chance_to_hit, minimum_damage, maximum_damage, chance_to_heal,
                       minimum_heal_points, maximum_heal_points) -> Ogre:
        """
        Builds a new Ogre.
        :param monster_data: monster stats.
        :return: newly created Ogre.
        """
        return Ogre(mtype, name, hit_points, attack_speed,
                       chance_to_hit, minimum_damage, maximum_damage, chance_to_heal,
                       minimum_heal_points, maximum_heal_points)

    @staticmethod
    def create_skeleton(mtype, name, hit_points, attack_speed,
                       chance_to_hit, minimum_damage, maximum_damage, chance_to_heal,
                       minimum_heal_points, maximum_heal_points) -> Skeleton:
        """
        Builds a new Skeleton.

        :param monster_data: monster stats.
        :return: newly created Skeleton.
        """
        return Skeleton(mtype, name, hit_points, attack_speed,
                       chance_to_hit, minimum_damage, maximum_damage, chance_to_heal,
                       minimum_heal_points, maximum_heal_points)

    @staticmethod
    def create_gremlin(mtype, name, hit_points, attack_speed,
                       chance_to_hit, minimum_damage, maximum_damage, chance_to_heal,
                       minimum_heal_points, maximum_heal_points) -> Gremlin:
        """
        Builds a new Gremlin.

        :param monster_data: monster stats.
        :return: newly created Gremlin.
        """
        return Gremlin(mtype, name, hit_points, attack_speed,
                       chance_to_hit, minimum_damage, maximum_damage, chance_to_heal,
                       minimum_heal_points, maximum_heal_points)

    @staticmethod
    def create_meangirl(mtype, name, hit_points, attack_speed,
                       chance_to_hit, minimum_damage, maximum_damage, chance_to_heal,
                       minimum_heal_points, maximum_heal_points) -> MeanGirl:
        """
        Builds a new MeanGirl.

        :param monster_data: monster stats.
        :return: newly created MeanGirl.
        """
        hit_points = 600        # temporary for boss
        minimum_damage = 20
        maximum_damage = 30
        return MeanGirl(mtype, name, hit_points, attack_speed,
                       chance_to_hit, minimum_damage, maximum_damage, chance_to_heal,
                       minimum_heal_points, maximum_heal_points)

# END
