import pygame

# from .Memo import Memo
# TODO import or create Memo here
from .Settings import *
from .Utility import convert_coords_to_map, create_textline

class Drawing: 
    """
    Class for drawing all images onto GUI surface. Sprite objects/images get 
    delivered here for blitting.
    """
    def __init__(self, screen, sound, map_coords, player_controls, hero, sprites, exit_coords) -> None:
        self.__screen = screen
        self.__sound = sound
        self.__map_coords = map_coords
        self.__player = player_controls
        self.__hero = hero
        self.__sprites = sprites
        self.__exit_coords = exit_coords
        self.__weapon_animate = 1
        self.__wep_time = 0
        self.__special_tick = 0
        self.__special_animate = 0
        self.__special_time = 0
        self.__vision_pot_tick = 0
        self.__textures = {
                         'ceiling': pygame.image.load('GUI/img/lava_sky3.png').convert(),
                         'door': pygame.image.load('GUI/img/door_portal2.png').convert(),
                         'wall': pygame.image.load('GUI/img/wall_d1.png').convert_alpha(),
                         'Hi': pygame.image.load('GUI/img/health_icon.png').convert_alpha(),
                         'Vi': pygame.image.load('GUI/img/vision_icon.png').convert_alpha(),
                         'Pi': pygame.image.load('GUI/img/pillar.png').convert_alpha(),
                         'exit': pygame.image.load('GUI/img/exit_icon.png').convert_alpha(),
                         f'{self.__hero.guild}w0': pygame.image.load(f'GUI/img/{self.__hero.guild}wep0.png').convert_alpha(),
                         f'{self.__hero.guild}w1': pygame.image.load(f'GUI/img/{self.__hero.guild}wep1.png').convert_alpha(),
                         f'{self.__hero.guild}w2': pygame.image.load(f'GUI/img/{self.__hero.guild}wep2.png').convert_alpha(),
                         f'{self.__hero.guild}w3': pygame.image.load(f'GUI/img/{self.__hero.guild}wep3.png').convert_alpha(),
                         f'{self.__hero.guild}s0': pygame.image.load(f'GUI/img/{self.__hero.guild}sp0.png').convert_alpha(),
                         f'{self.__hero.guild}s1': pygame.image.load(f'GUI/img/{self.__hero.guild}sp1.png').convert_alpha(),
                         f'{self.__hero.guild}s2': pygame.image.load(f'GUI/img/{self.__hero.guild}sp2.png').convert_alpha(),
                         f'{self.__hero.guild}s3': pygame.image.load(f'GUI/img/{self.__hero.guild}sp3.png').convert_alpha(),
                        #  'wall': pygame.image.load('GUI/img/wall_vision2.png').convert_alpha()
                         }

    @property
    def textures(self):
        return self.__textures

    def background(self):
        """
        Create "open" ceiling and floor
        TODO: as future implementation, add floor texture and shadows reflected on floor
        """
        sky_offset = -5 * math.degrees(self.__player.angle) % WIDTH
        self.__screen.blit(self.__textures['ceiling'], (sky_offset, 0))
        self.__screen.blit(self.__textures['ceiling'], (sky_offset - WIDTH, 0))
        self.__screen.blit(self.__textures['ceiling'], (sky_offset + WIDTH, 0))
        pygame.draw.rect(self.__screen, DARK_TAN, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))

    def world(self, world_objects): 
        """
        Allows win painting of sprites and walls on GUI surface
        :param world_objects: walls and sprites passed from Main
        :param type: list [walls + SpriteObjects]
        :return: None
        """
        if self.__player.win_game:
            return
        for obj in sorted(world_objects, key=lambda n: n[0], reverse=True):
            if obj[0]:
                _, object, object_pos = obj
                self.__screen.blit(object, object_pos)

    def weapon_and_ui(self, clock):
        """
        Method to organize this class. Called by Main.game_loop() to run these methods
        :return: None
        """
        self.__weapon_animation()
        self.__hero_health_bar()
        self.__special_bar()
        self.__special_animation()
        self.__enemy_health_bar()
        self.__inventory()
        self.__mini_map()
        self.__fps_display(clock)

    def __weapon_animation(self):
        """
        Animation of weapon using a timer (cool_down) to adjust animation speed
        :return: None
        """
        if self.__weapon_animate == 1:
            self.__sound.weapon()
        
        wep_pos = (WIDTH * 2/5, HEIGHT - 280)
        wep_size = (HALF_WIDTH, HALF_HEIGHT)
        cool_down = 4
        if self.__player.attacking and self.__weapon_animate < 3:
            if self.__wep_time < cool_down:
                self.__wep_time += 1
            else:
                self.__weapon_animate += 1
                self.__wep_time = 0
        else: 
            self.__weapon_animate = 0
        weapon = pygame.transform.scale(self.__textures[f'{self.__hero.guild}w{self.__weapon_animate}'], wep_size)
        self.__screen.blit(weapon, wep_pos)

    def __hero_health_bar(self):
        """
        Display hero's health bar, red as background for health lost, 
        underneath amount of current health
        bar_info = [left_pos, top_pos, width(health amount), height]
        :return: None
        """
        bar_info = [WIDTH - 180, HEIGHT - 60, 150, 30]
        border = [WIDTH - 184, HEIGHT - 64, 158, 38]

        pygame.draw.rect(self.__screen, BLACK, border)
        pygame.draw.rect(self.__screen, RED, bar_info)
        bar_info[2] *= self.__hero.hit_points / self.__hero.hit_points_max
        pygame.draw.rect(self.__screen, GREEN, bar_info)

        hp_txt, hp_pos = create_textline(self.__hero.name, 
                                         pos=(WIDTH - 173.5, HEIGHT - 55),
                                         font_type='GUI/font/28DaysLater.ttf', 
                                         size=20, 
                                         color=BLACK, 
                                         pos_type= 'xy')
        self.__screen.blit(hp_txt, hp_pos)

    def __enemy_health_bar(self):
        """
        Display nearby enemy's health bar
        bar_info = [left_pos, top_pos, width(health amount), height]
        :return: None
        """
        bar_x = 20
        bar_y = HALF_HEIGHT - 40
        width = 240
        height = 40
        name_x = bar_x + 5
        name_y = bar_y + 2
        bar_info = [bar_x, bar_y, width, height]
        border_offset = 3
        borders = [bar_x - border_offset, bar_y - border_offset, 
                   width + border_offset * 2, height + border_offset * 2]
        
        count = 0
        offset = 50
        
        for sprite in self.__sprites.nearby_sprites:
            if sprite.visible_health and sprite.object.is_alive:
                if count > 0: 
                    name_y -= offset
                    bar_info[1] -= offset
                    borders[1] = bar_info[1] - border_offset
                bar_info[2] *= sprite.object.hit_points / sprite.object.hit_points_max
                borders[2] = bar_info[2] + border_offset * 2
                pygame.draw.rect(self.__screen, BLACK, borders)
                pygame.draw.rect(self.__screen, PINK, bar_info)

                name, name_pos = create_textline(str(sprite.object.name), 
                                                    pos=(name_x, name_y),
                                                    font_type='GUI/font/Titillium.ttf', 
                                                    size=22,
                                                    color=BLACK,
                                                    pos_type='xy')
                self.__screen.blit(name, name_pos)
                count += 1

                # create boss label
                if sprite.name == 'mgirl':
                    boss_bar = bar_info.copy()
                    boss_bar[1] -= offset
                    boss_bar[2] = 155
                    boss_bar_border = borders.copy()
                    boss_bar_border[1] = boss_bar[1] - border_offset
                    boss_bar_border[2] = 160
                    pygame.draw.rect(self.__screen, BLACK, boss_bar_border)
                    pygame.draw.rect(self.__screen, YELLOW, boss_bar)

                    boss_x = boss_bar[0] + 5
                    boss_y = boss_bar[1] + 2
                    boss, boss_pos = create_textline("Boss: Mean Girl", 
                                                        pos=(boss_x, boss_y),
                                                        font_type='GUI/font/Titillium.ttf', 
                                                        size=22,
                                                        color=BLACK,
                                                        pos_type='xy')
                    self.__screen.blit(boss, boss_pos)

    def __special_bar(self):
        """
        Creates display for special skill mana & timer for mana ticking/increasing over time
        :return: None
        """
        cool_down = 60
        if self.__special_tick < cool_down:
            self.__special_tick += 1
        else:
            self.__special_tick = 0
            self.__hero.special_mana=True

        width = 30
        height = self.__hero.special_mana * 4
        x_pos = WIDTH - 58
        y_bottom = HEIGHT - 100
        y_pos = y_bottom - height
        
        column = [x_pos, y_pos, width, height]    
        
        if self.__hero.special_mana < 50:
            text = ' Special'        # replace with hero skill name
        else:
            text = ' Press R !'
            border_offset = 6
            border = [x_pos - border_offset, y_pos - border_offset, 
                      width + border_offset * 2, height + border_offset * 2]
            pygame.draw.rect(self.__screen, RED, border)

        pygame.draw.rect(self.__screen, YELLOW, column)
        s_txt, _ = create_textline(text, 
                                    pos=(x_pos, y_bottom),
                                    font_type='GUI/font/28DaysLater.ttf', 
                                    size=23,
                                    color=BLACK)
        s_txt = pygame.transform.rotate(s_txt, 90)
        txt_pos = s_txt.get_rect()
        padding = 4
        txt_pos.bottomleft = (x_pos + padding, y_bottom - padding)                           
        self.__screen.blit(s_txt, txt_pos)

    def __special_animation(self):
        '''
        Shows animation of special skill, used by all 3 different hero classes
        :return: None
        '''
        if self.__special_animate == 1:
            self.__sound.special_skill(self.__hero.guild)

        if self.__player.special_skill_animate and self.__special_animate < 3:
            special_pos = (HALF_WIDTH / 2, HALF_HEIGHT - 100)
            special_size = (HALF_WIDTH, HALF_HEIGHT)
            cool_down = 9
            if self.__special_time < cool_down:
                self.__special_time += 1
            else:
                self.__special_animate += 1
                self.__special_time = 0
            weapon = pygame.transform.scale(self.__textures[f'{self.__hero.guild}s{self.__special_animate}'], special_size)
            self.__screen.blit(weapon, special_pos)    
        else: 
            self.__player.special_skill_animate = False
            self.__special_animate = 0
        
        
    def __inventory(self):
        """
        Display inventory counts of pillars, vision potion & healing potions
        above the memo box. First half of code displays the iconds then
        displays counts of each.
        param: None, obtains info from self.textures and self.hero's inventory
        return: None
        """
        background_size = (45, HALF_HEIGHT + 185, 195, 38)
        pygame.draw.rect(self.__screen, BLACK, background_size)        

        icon_size = (30, 30)
        y_pos = HALF_HEIGHT + 190
        x_pos = 50
        x_offset = 60
        pillar_pos = (x_pos, y_pos)
        pillar = pygame.transform.scale(self.__textures['Pi'], icon_size)
        self.__screen.blit(pillar, pillar_pos)

        v_pot_pos = (x_pos + x_offset, y_pos)
        v_pot = pygame.transform.scale(self.__textures['Vi'], icon_size)
        self.__screen.blit(v_pot, v_pot_pos)

        h_pot_pos = (x_pos + x_offset * 2, y_pos)
        h_pot = pygame.transform.scale(self.__textures['Hi'], icon_size)
        self.__screen.blit(h_pot, h_pot_pos)

        count_y_pos = y_pos + 13
        count_x_offset = 45
        pillar_count, p_pos = create_textline(str(len(self.__hero.pillars)), 
                                            pos=(x_pos + count_x_offset, count_y_pos),
                                            font_type='GUI/font/28DaysLater.ttf', 
                                            size=30,
                                            color=YELLOW)
        self.__screen.blit(pillar_count, p_pos)

        v_pot_count, vpc_pos = create_textline(str(self.__hero.vision_potions), 
                                            pos=(x_pos + x_offset + count_x_offset, count_y_pos),
                                            font_type='GUI/font/28DaysLater.ttf', 
                                            size=30,
                                            color=WHITE)
        self.__screen.blit(v_pot_count, vpc_pos)

        h_pot_count, hpc_pos = create_textline(str(self.__hero.healing_potions), 
                                            pos=(x_pos + x_offset * 2 + count_x_offset, count_y_pos),
                                            font_type='GUI/font/28DaysLater.ttf', 
                                            size=30,
                                            color=RED)
        self.__screen.blit(h_pot_count, hpc_pos)

    def __mini_map(self):
        """
        Reveal map at top left corner when user holds down TAB key
        Also reveals vision of nearby rooms for several seconds after using vision potion
        TODO add pillars when found or when using vision potion
        """
        if self.__player.show_map:
            map_surf = pygame.Surface((WIDTH // MAP_SCALE, HEIGHT // MAP_SCALE))
            px, py = self.__player.x // MAP_SCALE, self.__player.y // MAP_SCALE

            # Draws visited path
            for x, y in self.__player.rooms_visited:
                x, y = convert_coords_to_map((x, y))    
                pygame.draw.rect(map_surf, RED, (x, y, MAP_TILE * 2, MAP_TILE * 2))

            # vision potion
            extra_rooms_visible = set()    # for seeing exit while using potion
            if self.__player.vision_pot_used:
                if self.__vision_pot_tick < 150:
                    pygame.draw.circle(map_surf, RED, (px, py), MAP_TILE * 3.15)
                    pygame.draw.circle(map_surf, WHITE, (px, py), MAP_TILE * 3)
                    self.__vision_pot_tick += 1
                    x, y = self.__player.cur_room.coords
                    if x > 0:
                        extra_rooms_visible.add((x - 1, y))
                    if x < 3:                # replace with width of maze to scale game
                        extra_rooms_visible.add((x + 1, y))
                    if y > 0:
                        extra_rooms_visible.add((x, y - 1))
                    if y < 3:                 # replace with height of maze to scale game
                        extra_rooms_visible.add((x, y - 1))
                else:
                    extra_rooms_visible = set()
                    self.__player.vision_pot_used = False
                    self.__vision_pot_tick = 0

            # Draws wall
            for x,y in self.__map_coords:
                pygame.draw.rect(map_surf, BLACK, (x, y, MAP_TILE, MAP_TILE))

            # exit icon
            if self.__exit_coords in self.__player.rooms_visited or \
                self.__exit_coords in extra_rooms_visible:
                map_size = (30, 30)
                exit = pygame.transform.scale(self.__textures['exit'], map_size)
                exit_x, exit_y = convert_coords_to_map(self.__exit_coords)
                map_surf.blit(exit, (exit_x, exit_y))

            # hero location & perspective
            pygame.draw.circle(map_surf, GREEN, (px, py), 5)
            pygame.draw.line(map_surf, GREEN, (px, py), (px + 12 * math.cos(self.__player.angle),
                            py + 12 * math.sin(self.__player.angle)), 2)

            self.__screen.blit(map_surf, MAP_POS)

    def __fps_display(self, clock):
        """
        Show active FPS, great to monitor software and hardware performance
        :param clock: pygame clock passed from Main
        :param type: pygame Clock object
        :return: None
        """
        fps_text = 'FPS ' + str(int(clock.get_fps()))
        fps_txt, fps_pos = create_textline(fps_text, 
                                            pos=(WIDTH-45, 15),
                                            font_type='GUI/font/28DaysLater.ttf', 
                                            size=30,
                                            color=WHITE)
        self.__screen.blit(fps_txt, fps_pos)