from Room import Room
from Grid import Grid
from Maze import Maze
from Model.Characters.MonsterSpawn import MonsterSpawn
from random import randrange


class Dungeon(Maze):
    """
    Thin subclass Maze that handles autofilling of items, etc.
    """
    ITEM_CHANCE: int = 40  # percent chance given item type appears in room

    def __init__(self, *args, **kwargs):
        """ Create a Dungeon. Same usage as Maze constructor. """
        super().__init__(*args, **kwargs)
        self.validate_in_out()
        MonsterSpawn.create_database()
        self.add_boss()
        self.add_pillars_and_monsters()
        self.add_contents()

    def validate_in_out(self) -> None:
        """ Confirm has Entrance and Exit; either creator of imported map
        or Maze.generate() method should have taken care to include those.
        :return: None
        :exception: ValueError, if validation fails
        """
        if not self.ingress or not self.egress:
            raise ValueError("Maze must have an entrance and one exit")
        ins = []
        outs = []
        for row in self.rooms:
            for room in row:
                if room.is_entrance and room.is_exit:
                    raise ValueError("Dungeon maze entrance and exit must be different rooms")
                if room.is_entrance:
                    ins.append(room)
                if room.is_exit:
                    outs.append(room)
        if len(ins) > 1:
            raise ValueError("Dungeon maze must only have a single entrance")
        if len(outs) > 1:
            raise ValueError("Dungeon maze must only have a single exit")
        return

    def add_boss(self) -> None:
        """
        Add boss Mean Girl at exit
        """
        self.egress.occupants = (MonsterSpawn.make('mgirl'), True)

    def add_pillars_and_monsters(self) -> None:
        """ Check for Pillars, add ANY that are missing.
        :return: None
        :exception: ValueError, if validation fails, i.e. multiples of some Pillar.
        """
        def __add_monster(room):
            types = ('ogre', 'skeleton', 'gremlin')
            mtype = types[randrange(3)]    
            room.occupants = (MonsterSpawn.make(mtype), True)

        pillars = dict([(_p, []) for _p in Room.pillars])
        for row in self.rooms:
            for room in row:
                if room.pillar:
                    _p = room.pillar
                    if _p not in pillars:
                        raise ValueError(f"Dungeon maze has unrecognized Pillar {repr(_p)}")
                    pillars[_p].append(room)              
        dups = [_p for _p in pillars if len(pillars[_p]) > 1]
        if len(dups) > 0:
            raise ValueError(f"Dungeon maze contains dups for Pillar {repr(dups[0])}")
        missing = [_p for _p in pillars if len(pillars[_p]) == 0]
        if len(missing) == 0:
            # Exactly one of each
            return

        # Some are missing, add them now to random empty rooms
        empties = self.get_empty_rooms()
        if len(empties) < len(missing):
            raise ValueError("Dungeon maze has no empty Rooms in which to add missing Pillars")
        for pillar in missing:
            i = randrange(len(empties))
            room = empties.pop(i)
            room.pillar = pillar
            __add_monster(room)
        return

    def get_empty_rooms(self) -> list[Room]:
        empties: list[Room] = []
        for row in self.rooms:
            for room in row:
                if room.is_empty and not room.is_entrance and not room.is_exit:
                    empties.append(room)
        return empties

    def prep_room(self, room: Room) -> None:
        """ Add items to room, according to formula
        :param room: Room to have some random item(s) added.
        :return: None
        """
        if randrange(60) < Dungeon.ITEM_CHANCE:
            room.has_pit = True
        if randrange(100) < 40:
            room.healing_potions += 1
        if randrange(150) < Dungeon.ITEM_CHANCE:
            room.vision_potions += 1

    def add_contents(self) -> None:
        """ Check for other items, add if NONE are present.
        To be clear, if ANY are present, assume was intentional, so add nothing.
        :return: None
        """
        for row in self.rooms:
            for room in row:
                if not room.is_empty and not room.pillar:
                    return
        # Fill 'er up!
        empties = self.get_empty_rooms()
        for room in empties:
            self.prep_room(room)


if __name__ == '__main__':
    print("Greetings from Dungeon!\n")

    print("randomly generated:")
    Grid.set_style_default(Room.styles.open)
    g_d = Dungeon()
    print(f"{g_d}")

# END
