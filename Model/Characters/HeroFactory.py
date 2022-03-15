from Model.Characters.Hero import Hero
from Model.Characters.Thief import Thief
from Model.Characters.Priestess import Priestess
from Model.Characters.Warrior import Warrior


class HeroFactory:

    guilds = {
        'Priestess': Priestess,
        'Thief': Thief,
        'Warrior': Warrior,
    }

    @staticmethod
    def create_hero(guild: str = None, *args, **kwargs):
        """
        Hero factory. Instantiates specified `guild` subclass or base `Hero` class.
        :param guild: name of guild, one of the keys in `Hero.guilds`; or `None`
        :returns: instance of `Hero` subclass corresponding to `guild` in `Hero.guilds`;
          or if `guild` is either `None` or "Coward", then of base `Hero` class.
        """
        if guild is None or guild.capitalize() == 'Coward':
            return Hero(*args, **kwargs)
        guild = guild.capitalize()
        if guild in HeroFactory.guilds:
            subcls = HeroFactory.guilds[guild]
            return subcls(*args, **kwargs)
        raise ValueError(f"unrecognized Hero guild '{guild}'")


if __name__ == '__main__':

    def example():
        hero = HeroFactory.create_hero()
        print(hero)
        for guild in HeroFactory.guilds:
            hero = HeroFactory.create_hero(guild=guild)
            print(hero)

    example()

# END
