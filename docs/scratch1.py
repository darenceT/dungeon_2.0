class DungeonAdventure:

    def __init__(self):

        # preamble, collection of setup options
        io = AdventurerInput()
        io.start()
        name = io.get_name()
        size = io.get_size()
        sir = Adventurer(name)
        maze = Dungeon(size)

        # off to the races!
        # loop that ping/pongs with AdventurerInput
        while True:
            # TODO method dispatch
            # TODO pass back outcome info to AdventureInput? Somehow...?
            pass

    def move(self, direction):
        # TODO check whether direction legal; if not return some sort of failure
        pass

    def drink_vision(self):
        # TODO check whether have a potion
        # TODO else... attain enlightenment!
        pass

    def drink_health(self):
        # TODO check whether have a potion
        # TODO else... feel better!
        pass

    def quit