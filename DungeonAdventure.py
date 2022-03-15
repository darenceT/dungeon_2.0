from Compass import Compass, CompassDirection
from Room import Room
from Grid import Grid
from Maze import Maze
from Dungeon import Dungeon
from Model.Characters.Hero import Hero
from Model.Characters.HeroFactory import HeroFactory

class DungeonAdventure:
    """
    Class that creates a game and pulls together all of the gameplay
    """
    default_hit_points_initial: int = 80
    default_hit_points_max: int = 100   
    pit_damage: int = 10

    def __init__(self, map_str: str = None, guild: str = None, name: str = None):
        """
        Initializes DungeonAdventure Class
        :param map_str: String of maze map
        """
        self.__maze = Dungeon(map_str=map_str)
        self.__room = self.maze.ingress
        self.__hero = HeroFactory.create_hero(guild=guild, name=name)
        self.__continues: bool = True

    @property
    def hero(self) -> Hero:
        """
        Returns the Hero from the Adventurer class
        :return:
        """
        return self.__hero

    @hero.setter
    def hero(self, hero: Hero) -> None:
        """
        Sets the Hero from the Adventurer Class
        :param hero: object of type Adventurer, our player
        :return:
        """
        self.__hero = hero

    @property
    def name(self) -> str:
        """ Name of Adventurer.
        Not actually a property of DungeonAdventure class itself.
        But used so often in dialogue, covenient to shorten the path to it.
        Only set once though, so corresponding setter not really warranted.
        :return string
        """
        return self.hero.name

    @property
    def maze(self) -> Maze:
        """
        Gets the maze
        :return:
        """
        return self.__maze

    @maze.setter
    def maze(self, maze: Maze) -> None:
        """
        Sets the maze for the current game
        :param maze: current instance of Maze
        :return:
        """
        self.__maze = maze

    @property
    def room(self) -> Room:
        """
        Gets the room
        :return:
        """
        return self.__room

    @room.setter
    def room(self, room: Room) -> None:
        """
        Sets the current room
        :param room: current instance of Room
        :return:
        """
        self.__room = room

    @property
    def continues(self) -> bool:
        """
        Determines whether or not to end the game. Checks to see if hero is still alive, if they are, continue.
        :return:
        """
        if not self.hero.is_alive:
            return False
        return self.__continues

    @continues.setter
    def continues(self, tallyho: bool) -> None:
        """
        Returns True to continue game
        :param tallyho: boolean value to determine continuation (True)
        :return:
        """
        self.__continues = tallyho

    def prelude(self):
        """
        Silly prelude, followed by prompt for Adventurer's name, and introduction to game.
        :return:
        """
        # intro gag, no actual effect
        option = input("Shall we play a game? (Y/N)\n")
        if option.upper() in ("N", 'NO'):
            print("Commence global thermonuclear war in 3... 2... 1...")
            print(".....haha, not really! That is scheduled for tomorrow.")
            print()
        # actual preamble
        print("Huzzah! Welcome to Dungeon Adventure!")
        name = input("What is your name, brave adventurer?\n")
        self.hero.name = name
        print(f"Oh my. Your parents had some strange ideas, Sir {self.name}.")
        print()  # Blank line for visual separation

        print("Very well then, you have entered a Dungeon, in which there is a Maze.")
        print("There are perilous Pits, potent Potions to purloin, and four Pillars to perceive.")
        self.enter_room(self.room)
        print(str(self.room))
        self.display_menu()

    def finish(self):
        """
        Announces that the game has ended
        :return:
        """
        print(f"Brave Sir {self.name} is at The End.")

    @staticmethod
    def display_menu():
        """
        Displays menu of game play options, excluding hidden ones.
        :return:
        """
        print("\n".join(["Here are your options...",
                         "- Show (I)nventory or (M)ap",
                         "- Move (N)orth, (S)outh, (E)ast, or (W)est",
                         "- Use (V)ision Potion or (H)ealing Potion",
                         "- (Q)uit game in disgust",
                         "- (?) show these options again"]))
        # Do NOT reveal the hidden options:
        # (*) show full map, (@) describe current room

    def prompt(self):
        """
        Prompts user for game play option, and returns corresponding actions.
        :return:
        """
        print()  # empty line to visually separate from preceding stanza
        option = input(f"What would you like to do, brave Sir {self.name}?\n")

        def match(got: str, *wants) -> bool:
            """ Nested utility function. """
            for want in wants:
                if got.lower() == want.lower():
                    return True
            return False

        if option == '?':
            self.display_menu()

        elif match(option, 'Q', 'quit'):
            print("Discretion is the better part of valor.")
            print(f"Three cheers for brave Sir {self.name}!")
            self.continues = False

        elif match(option, 'I', 'inventory'):
            print("Thine Bag of Holding doth weigh upon you most ponderously...")
            self.hero.display_inventory()

        elif match(option, 'M', 'map'):
            print("I'm the Map! I'm the Map! I'M! THE! MAP!!!")
            print(f"{self.maze.str(style=Room.styles.veiled)}")

        elif match(option, '@', 'describe'):
            # Hidden option! Describe current room
            print("There is something about this room...")
            print(str(self.room.describe()))

        elif match(option, '*', 'joshua'):
            # Hidden option! Print full maze
            if match(option, 'joshua'):
                print("A strange game. The only winning move is not to play...")
            else:
                print("There is a sharp pain behind your eyes, then all is revealed...")
            print(self.maze.str(style=Room.styles.tracker))

        elif match(option, 'H', 'healing', 'health'):
            if self.hero.healing_potions <= 0:
                print("Did you suffer a head injury? You do not have any Healing Potions.")
            else:
                print("You guzzle down the sweet, sweet elixir or life.")
                self.hero.use_healing_potion()
                print(f"You have {self.hero.hit_points} hit points now.")

        elif match(option, 'V', 'vision'):
            if self.hero.vision_potions <= 0:
                print("Oblivious as always, you failed to note your lack of Vision Potions.")
            else:
                print("You swig the crystal clear fluid, gasp, then stare in amazement...")
                self.hero.use_vision_potion()

        elif Compass.dir(option):
            _dir: CompassDirection = Compass.dir(option)
            print(f"You take a step to the {_dir.name}... ", end='')
            can_move, next_room = self.maze.can_move(self.room, direction=_dir)
            next_room = self.room.neighbor(option)
            if not can_move:
                print("but are thwarted.")
                print(f"Brave Sir {self.name} didst stare defiantly at his shoes.")
                return
            if next_room is None:
                print("but discover there is void on the other side.")
                print(f"Brave Sir {self.name} steps back from the precipice.")
                return
            print("sailing gracefully into the next room.")
            print(next_room)
            self.enter_room(next_room)

        else:
            print()  # empty line for visual separation
            print("These words that you are using...")
            print("I do not think they mean what you think they mean.")
            print("Perhaps your response should be in the form of a '?'...")
            # no-op

    def play(self):
        """
        Main game play loop
        :return:
        """
        self.prelude()
        while self.continues:
            self.prompt()
        self.finish()

    def find_healing_potion(self):
        """
        Prints a string when user finds a healing potion. Subtracts potion from room, adds potion to
        Adventurer inventory.
        :return:
        """
        print("You find a Healing Potion. Use this to restore some lost hit-points.")
        self.room.healing_potions -= 1
        self.hero.gain_healing_potion()

    def find_vision_potion(self):
        """
        Prints a string when user finds a vision potion. Subtracts potion from room, adds potion to
        Adventurer inventory.
        :return:
        """
        print("You find a Vision Potion. Use this to see surrounding rooms.")
        self.room.vision_potions -= 1
        self.hero.gain_vision_potion()

    def extend_vision(self):
        from_coords = (self.room.coord_x -1, self.room.coord_y - 1)
        extent = Grid(3, 3, from_grid=self.maze, from_coords=from_coords)
        for row in extent.rooms:
            for room in row:
                room.has_crumb = True
        print(f"{extent}")

    def find_pillar(self, pillar: str = None):
        """
        Prints one string when user has already encountered a pillar, and a different string when encountering it
        for the first time. Adds new pillar to Adventurer inventory.
        :param pillar:
        :return:
        """
        if pillar is None and self.room.pillar is not None:
            pillar = self.room.pillar
        if self.hero.has_pillar(pillar):
            print(f"Oh look, the Pillar '{pillar}'. Already seen it. So boring.")
        else:
            print(f"You find the Pillar '{pillar}'. Good job, you!")
            self.hero.gain_pillar(self.room.pillar)

    def fall_into_pit(self):
        """
        Prints a string when the hero encounters a pit. Assigns damage to hero, checks to see if hero is still alive.
        If still alive, print new hit points.
        :return:
        """
        print("You fall into a Pit. The fall is merely frightening... ", end='')
        # TODO: damage is randomly set (?)
        self.hero.take_damage(damage=self.pit_damage)
        if not self.hero.is_alive:
            print("but the landing is fatal.  x_x")
        else:
            print("but the landing hurts. Oof!  >_<")
            print(f"You now have {self.hero.hit_points} hit-points.")

    def find_exit(self):
        """
        Checks to see if room has an exit. If room has exit:
        Prints string and ends game if hero has collected all of the pillars
        Prints string and continues if hero has not collected all pillars and has never found the exit before
        Prints a different string and continues if hero has not collected all of the pillars but has seen the exit before.
        :return:
        """
        if not self.room.is_exit:
            return
        if not self.room.has_crumb:
            print(f"Dilly Dilly! Brave Sir {self.name} has found the Exit!")
        else:
            print(f"Brave Sir {self.name} once again arrives at the exit.")
        if set(self.hero.pillars) == set(Room.pillars):
            print("And with all of the Pillars collected. Bravo!")
            self.__continues = False
        else:
            print("But the mission is not complete! Find the remaining Pillars,")
            print("then return here to the Exit... if you can!")

    def enter_room(self, room) -> None:
        """ Enter a room. Stuff happens and/or is found.
        *** DOES NOT AUTO pickup potions/pit
        When the hero enters a room:
        checks to see if there is a pit, if yes, calls pit function.
            checks to see if hero is no longer alive
        checks to see if room has healing potion,if yes calls find healing potion function
        checks to see if room has vision potion, if yes calls find vision potion function
        :param room:
        :return:
        """
        if self.room is not None:
            self.room.has_hero = False
        self.room = room
        self.room.has_hero = True
        # Falling into pit occurs first. If fatal, do not find other contents.
        # if room.has_pit:
        #     self.fall_into_pit()
        if not self.hero.is_alive:
            return
        # # Collect items
        # if room.healing_potions:
        #     self.find_healing_potion()
        # if room.vision_potions:
            # self.find_vision_potion()
        # Pillars and Exit are each supposed to be sole item in room, if present.
        # Ergo, cannot have both, so order of the following does not matter.
        # if room.pillar:
        #     self.find_pillar()
        # if room.is_exit:
        #     self.find_exit()
        # Drop breadcrumb AFTER finding Pillar or Exit, so announce differently.
        room.has_crumb = True


    def enter_room_OLD(self, room) -> None:
        """ Enter a room. Stuff happens and/or is found.
        When the hero enters a room:
        checks to see if there is a pit, if yes, calls pit function.
            checks to see if hero is no longer alive
        checks to see if room has healing potion,if yes calls find healing potion function
        checks to see if room has vision potion, if yes calls find vision potion function
        :param room:
        :return:
        """
        if self.room is not None:
            self.room.has_hero = False
        self.room = room
        self.room.has_hero = True
        # Falling into pit occurs first. If fatal, do not find other contents.
        if room.has_pit:
            self.fall_into_pit()
        if not self.hero.is_alive:
            return
        # Collect items
        if room.healing_potions:
            self.find_healing_potion()
        if room.vision_potions:
            self.find_vision_potion()
        # Pillars and Exit are each supposed to be sole item in room, if present.
        # Ergo, cannot have both, so order of the following does not matter.
        if room.pillar:
            self.find_pillar()
        if room.is_exit:
            self.find_exit()
        # Drop breadcrumb AFTER finding Pillar or Exit, so announce differently.
        room.has_crumb = True


__demo_map = """
# This is my fine dungeon
+-----+-----+-----+
| i   |     = O   |
+--H--+--H--+-----+
| P   = XV  = HH  |
+-----+-----+-----+
"""

if __name__ == "__main__":

    # FIXME
    g_resp = None
    g_map_str = None
    g_game = DungeonAdventure(map_str=g_map_str)
    g_game.play()

# END
