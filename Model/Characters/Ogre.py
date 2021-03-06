from Model.Characters.Monster import Monster


class Ogre(Monster):
    """
    Initializes Ogre, a subclass of Monster. Default field values provided for testing, but values are pulled from database.
    """
    def __init__(self, mtype, name, hit_points=200, attack_speed=2, chance_to_hit=0.6,
                 minimum_damage=30, maximum_damage=60, chance_to_heal=0.1, minimum_heal_points=30,
                 maximum_heal_points=60):
        super().__init__(mtype, name, hit_points, attack_speed, chance_to_hit,
                         minimum_damage, maximum_damage, chance_to_heal, minimum_heal_points, maximum_heal_points)

if __name__ == '__main__':
    o = Ogre(mtype="ogre", name="joe")
    print(o)
