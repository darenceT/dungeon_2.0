import pygame
from pygame import mixer
from pathlib import Path
from random import randrange

class Sound:
    """
    Constructor/instance included so that a tracker can be used for sound options,
    to turn off and on the sound & music.
    (intro, in-game, gremlin, mgirl, lose) from https://www.chosic.com/free-music/all/
    (healing special, pickup potions) from https://mixkit.co/free-sound-effects/
    (defeat monster) from https://freesound.org/people/MrFossy/sounds/521900/
    Remaining sounds from https://www.zapsplat.com/sound-effect-categories/
    """
    def __init__(self):
        """
        is_running keeps track of whether music & sound is on to 
        allow sound option to turn off or on. 
        Set initial background music and sounds to medium level.
        """
        pygame.init()
        mixer.music.set_volume(0.4)
        mixer.Channel(0).set_volume(0.75)
        self.__is_running = True
        self.__monster_sounds = []

    @property
    def is_running(self):
        """
        Getter for is_running status of all sounds
        :return: status of whether sounds are on
        :rtype: bool
        """
        return self.__is_running

    @is_running.setter
    def is_running(self, change):
        """
        Setter for is_running status of all sounds
        :param change: switching off or on of all sounds
        :type change: bool
        :raises: if param is not a boolean
        """
        if isinstance(change, bool):
            self.__is_running = change
        else:
            raise TypeError("Only boolean param accepted")

    @property
    def monster_sounds(self):
        """
        Getter to obtain list of sounds involved in combat:
        :return: said list
        :rtype: list[str]
        """
        return self.__monster_sounds

    @monster_sounds.setter
    def monster_sounds(self, info): 
        """
        Setter to add or remove monster sounds involved in combat
        :param info: monster class and whether to remove or add
        :param type: tuple(str, bool)
        :return: None
        """
        npc_name, remove = info
        if remove:
            self.monster_sounds.remove(npc_name)
        else:
            self.monster_sounds.append(npc_name)

    def turn_off(self):
        """
        Turn off all sounds
        :return: None
        """
        self.__is_running = False
        mixer.quit()

    def turn_on(self, in_game=False):
        """
        Turn on all sounds, play intro music or in-game music depending
        on when this is called
        :param in_game: whether this is accessed at intro or in-game
        :type in_game: bool
        :raises: if param is not a boolean type
        """
        if isinstance(in_game, bool):
            self.__is_running = True
            mixer.init()
            mixer.music.set_volume(0.4)
            if in_game:
                self.in_game()
            else:
                self.intro()
        else:
            raise TypeError("Only boolean param accepted")

    def intro(self):
        """
        Play intro music. 
        :return: None
        """
        if self.__is_running:
            mixer.music.load(Path('GUI/sound/Kai-Engel-Low-Horizon_s.mp3'))
            mixer.music.play(-1)

    def in_game(self):
        """
        Play in-game music. 
        :return: None
        """
        if self.__is_running:
            mixer.music.load(Path('GUI/sound/Komiku_-_52_-_Cave_of_time_s.mp3'))
            mixer.music.play(-1)

    def pause_menu(self, resume=False):
        """
        Pause music while in pause menu
        :param resume: allow resuming game music
        :type resume: bool
        """
        if resume:
            mixer.music.unpause()
        else:
            mixer.music.pause()

    def lose(self):
        """
        Music with player loses
        :return: None
        """
        if self.__is_running:
            mixer.music.load(Path('GUI/sound/lose.mp3'))
            mixer.music.play(-1)

    def win(self):
        """
        Music with player wins
        :return: None
        """
        if self.__is_running:
            mixer.music.load(Path('GUI/sound/zapsplat_win.mp3'))
            mixer.music.play(-1)

    def pickup(self):
        """
        Sound for collecting potions
        :return: None
        """
        if self.__is_running:
            mixer.Channel(2).play(pygame.mixer.Sound(Path('GUI', 'sound', 'mixkit-pickup.wav')))

    def pillar(self):
        """
        Sound for finding/"touching" pillar
        :return: None
        """
        if self.__is_running:
            mixer.Channel(4).play(pygame.mixer.Sound(Path('GUI', 'sound', 'zapsplat_pillar.mp3')))

    def health_potion(self):
        """
        Sound for consuming health potion
        :return: None
        """
        if self.__is_running:
            mixer.Channel(1).play(pygame.mixer.Sound(Path('GUI', 'sound', 'zapsplat_health_pot.mp3')))

    def vision_potion(self):
        """
        Sound for effects of vision potion
        :return: None
        """
        if self.__is_running:
            mixer.Channel(1).play(pygame.mixer.Sound(Path('GUI', 'sound', 'zapsplat_vision.mp3')))
    
    def weapon(self):
        """
        Sound for using main weapon
        :return: None
        """
        if self.__is_running:
            mixer.Channel(1).play(pygame.mixer.Sound(Path('GUI','sound', 'zapsplat_wep_hit.mp3')))
    
    def special_skill(self, h_class):
        """
        Sound for special skill for each hero class
        :param h_class: hero class/guild
        :param type: str
        :return: None
        """
        if self.__is_running:
            mixer.Channel(3).play(pygame.mixer.Sound(Path('GUI','sound', f'{h_class}sp.mp3')))

    def monster_play(self, mtype, off=False):
        """
        Noise from monsters when engaged, specific the monster type
        :param mtype: monster class
        :param type: str
        :param off: allows method to turn off sound if True
        :param type: bool
        :return: None
        """
        if mtype in ('mgirl', 'ogre', 'gremlin', 'skeleton') and self.__is_running:
            channel = self.__monster_sounds.index(mtype) + 4
            if off:
                mixer.Channel(channel).stop()
            else:
                mixer.Channel(channel).play(pygame.mixer.Sound(Path('GUI','sound', f'{mtype}.mp3')))

    def defeat_monster(self):
        """
        Sound for defeating monster
        :return: None
        """
        if self.__is_running:
            mixer.Channel(5).play(pygame.mixer.Sound(Path('GUI','sound', f'defeat_monster{randrange(4)}.wav')))
