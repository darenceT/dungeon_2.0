from typing import Union

from Ogre import Ogre
from Skeleton import Skeleton
from Gremlin import Gremlin
from MeanGirl import MeanGirl


class MonsterFactory:

    @staticmethod
    def create_monster(mtype: str, *monster_data) -> Union[Ogre, Skeleton, Gremlin, MeanGirl]:
        """
        Creates a monster of the specified type using the necessary data
        for building that monster and returns that monster. e.g.:
        my_monster = MonsterFactory.create_monster("Skeleton", hit_points etc...),
        :param mtype: Name of a Monster subclass.
        :param monster_data: stats for the relevant monster.
        :return: newly created monster
        """
        if mtype == "Ogre":
            maker = MonsterFactory.create_ogre
        elif mtype == "Skeleton":
            maker = MonsterFactory.create_skeleton
        elif mtype == "Gremlin":
            maker = MonsterFactory.create_gremlin
        elif mtype == "MeanGirl":
            maker = MonsterFactory.create_meangirl
        else:
            raise ValueError(f"does not support monster_name {mtype}")
        monster = maker(*monster_data)
        return monster

    @staticmethod
    def create_ogre(*monster_data) -> Ogre:
        """
        Builds a new Ogre.
        :param monster_data: monster stats.
        :return: newly created Ogre.
        """
        return Ogre(*monster_data)

    @staticmethod
    def create_skeleton(*monster_data) -> Skeleton:
        """
        Builds a new Skeleton.

        :param monster_data: monster stats.
        :return: newly created Skeleton.
        """
        return Skeleton(*monster_data)

    @staticmethod
    def create_gremlin(*monster_data) -> Gremlin:
        """
        Builds a new Gremlin.

        :param monster_data: monster stats.
        :return: newly created Gremlin.
        """
        return Gremlin(*monster_data)

    @staticmethod
    def create_meangirl(*monster_data) -> MeanGirl:
        """
        Builds a new MeanGirl.

        :param monster_data: monster stats.
        :return: newly created MeanGirl.
        """
        return MeanGirl(*monster_data)

# END
