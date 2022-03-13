import pygame

# from .Memo import Memo
from .Settings import *
from .Utility import create_textline

class Drawing: 
    """
    Class for drawing all images onto GUI surface. Sprite objects/images get 
    delivered here for blitting.
    """
    def __init__(self, screen, sound, hero_class, map_coords, player_controls, hero, sprites) -> None:
        self.screen = screen
        self.sound = sound
        self.hero_class = hero_class
        self.map_coords = map_coords
        self.player = player_controls
        self.hero = hero
        self.sprites = sprites
        self.__weapon_animate = 1
        self.__wep_time = 0
        self.__special_tick = 0
        self.__special_animate = 0
        self.__special_time = 0
        # TODO only load current hero class weapons/special
        self.textures = {
                        #  'floor': pygame.image.load('GUI/img/floor.jpg').convert(),
                         'ceiling': pygame.image.load('GUI/img/ceiling3.jpg').convert(),
                         'door': pygame.image.load('GUI/img/door_portal.png').convert(),
                         'wall': pygame.image.load('GUI/img/wall_default2.png').convert_alpha(),
                         'Hi': pygame.image.load('GUI/img/health_icon.png').convert_alpha(),
                         'Vi': pygame.image.load('GUI/img/vision_icon.png').convert_alpha(),
                         'Pi': pygame.image.load('GUI/img/pillar.png').convert_alpha(),
                         'warrior0': pygame.image.load('GUI/img/sword0.png').convert_alpha(),
                         'warrior1': pygame.image.load('GUI/img/sword1.png').convert_alpha(),
                         'warrior2': pygame.image.load('GUI/img/sword2.png').convert_alpha(),
                         'warrior3': pygame.image.load('GUI/img/sword3.png').convert_alpha(),
                         'priest0': pygame.image.load('GUI/img/staff0.png').convert_alpha(),
                         'priest1': pygame.image.load('GUI/img/staff1.png').convert_alpha(),
                         'priest2': pygame.image.load('GUI/img/staff2.png').convert_alpha(),
                         'priest3': pygame.image.load('GUI/img/staff3.png').convert_alpha(),
                         'thief0': pygame.image.load('GUI/img/dagger0.png').convert_alpha(),
                         'thief1': pygame.image.load('GUI/img/dagger1.png').convert_alpha(),
                         'thief2': pygame.image.load('GUI/img/dagger2.png').convert_alpha(),
                         'thief3': pygame.image.load('GUI/img/dagger3.png').convert_alpha(),
                         'heal0': pygame.image.load('GUI/img/heal0.png').convert_alpha(),
                         'heal1': pygame.image.load('GUI/img/heal1.png').convert_alpha(),
                         'heal2': pygame.image.load('GUI/img/heal2.png').convert_alpha(),                         
                        #  'wall': pygame.image.load('GUI/img/wall_vision2.png').convert_alpha()
                         }

    def background(self):
        sky_offset = -5 * math.degrees(self.player.angle) % WIDTH
        self.screen.blit(self.textures['ceiling'], (sky_offset, 0))
        self.screen.blit(self.textures['ceiling'], (sky_offset - WIDTH, 0))
        self.screen.blit(self.textures['ceiling'], (sky_offset + WIDTH, 0))
        pygame.draw.rect(self.screen, DARK_TAN, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))

    def world(self, world_objects): 
        if self.player.win_game:
            return
        for obj in sorted(world_objects, key=lambda n: n[0], reverse=True):
            if obj[0]:
                _, object, object_pos = obj
                self.screen.blit(object, object_pos)

    def weapon_and_ui(self, clock):
        self.weapon_animation()
        self.hero_health_bar()
        self.special_bar()
        self.special_animation()
        self.enemy_health_bar()
        self.inventory()
        self.mini_map()
        self.fps_display(clock)

    def weapon_animation(self):
        """
        Animation of weapon using a timer (cool_down) to adjust animation speed
        """
        if self.__weapon_animate == 1:
            self.sound.weapon()
        
        wep_pos = (WIDTH * 2/5, HEIGHT - 280)
        wep_size = (HALF_WIDTH, HALF_HEIGHT)
        cool_down = 4
        if self.player.attacking and self.__weapon_animate < 3:
            if self.__wep_time < cool_down:
                self.__wep_time += 1
            else:
                self.__weapon_animate += 1
                self.__wep_time = 0
        else: 
            self.__weapon_animate = 0
        weapon = pygame.transform.scale(self.textures[f'{self.hero.hero_type}{self.__weapon_animate}'], wep_size)
        self.screen.blit(weapon, wep_pos)

    def hero_health_bar(self):
        """
        Display hero's health bar, red as background for health lost, 
        underneath amount of current health
        bar_info = [left_pos, top_pos, width(health amount), height]
        """
        bar_info = [WIDTH - 180, HEIGHT - 60, 150, 30]
        border = [WIDTH - 184, HEIGHT - 64, 158, 38]

        pygame.draw.rect(self.screen, BLACK, border)
        pygame.draw.rect(self.screen, RED, bar_info)
        bar_info[2] *= self.hero.hit_points / self.hero.hit_points_max
        pygame.draw.rect(self.screen, GREEN, bar_info)

        text = 'Health'
        hp_txt, hp_pos = create_textline(text, 
                                         pos=(WIDTH - 145, HEIGHT - 46),
                                         font_type='GUI/font/28DaysLater.ttf', 
                                         size=20,
                                         color=BLACK)
        self.screen.blit(hp_txt, hp_pos)

    def enemy_health_bar(self):
        """
        Display nearby enemy's health bar
        bar_info = [left_pos, top_pos, width(health amount), height]
        """
        bar_x = 20
        bar_y = HALF_HEIGHT - 40
        width = 220
        height = 40
        name_x = bar_x + 5
        name_y = bar_y + 3
        bar_info = [bar_x, bar_y, width, height]
        border_offset = 3
        borders = [bar_x - border_offset, bar_y - border_offset, 
                   width + border_offset * 2, height + border_offset * 2]
        
        count = 0
        offset = 50
        
        for sprite in self.sprites.nearby_sprites:
            if sprite.visible_health and sprite.object.is_alive:
                if count > 0: 
                    name_y -= offset
                    bar_info[1] -= offset
                    borders[1] = bar_info[1] - border_offset
                bar_info[2] *= sprite.object.hit_points / sprite.object.hit_points_max
                borders[2] = bar_info[2] + border_offset * 2
                pygame.draw.rect(self.screen, BLACK, borders)
                pygame.draw.rect(self.screen, PINK, bar_info)

                name, name_pos = create_textline(str(sprite.object.name), 
                                                    pos=(name_x, name_y),
                                                    font_type='GUI/font/Titillium.ttf', 
                                                    size=20,
                                                    color=BLACK,
                                                    pos_type='xy')
                self.screen.blit(name, name_pos)
                count += 1

    def special_bar(self):
        """
        Creates display for special skill mana & timer for mana ticking/increasing over time
        """
        cool_down = 60
        if self.__special_tick < cool_down:
            self.__special_tick += 1
        else:
            self.__special_tick = 0
            self.hero.special_mana=True

        width = 30
        height = self.hero.special_mana * 4
        x_pos = WIDTH - 58
        y_bottom = HEIGHT - 100
        y_pos = y_bottom - height
        
        column = [x_pos, y_pos, width, height]    
        
        if self.hero.special_mana < 50:
            text = ' Special'        # replace with hero skill name
        else:
            text = ' Press R !'
            border_offset = 6
            border = [x_pos - border_offset, y_pos - border_offset, 
                      width + border_offset * 2, height + border_offset * 2]
            pygame.draw.rect(self.screen, RED, border)

        pygame.draw.rect(self.screen, YELLOW, column)
        s_txt, _ = create_textline(text, 
                                    pos=(x_pos, y_bottom),
                                    font_type='GUI/font/28DaysLater.ttf', 
                                    size=23,
                                    color=BLACK)
        s_txt = pygame.transform.rotate(s_txt, 90)
        txt_pos = s_txt.get_rect()
        padding = 4
        txt_pos.bottomleft = (x_pos + padding, y_bottom - padding)                           
        self.screen.blit(s_txt, txt_pos)

    def special_animation(self):
        '''
        Shows animation of special skill
        TODO make animation specific to hero class
        '''
        if self.player.special_skill and self.__special_animate < 2:
            special_pos = (HALF_WIDTH / 2, HALF_HEIGHT - 100)
            special_size = (HALF_WIDTH, HALF_HEIGHT)
            cool_down = 12
            if self.__special_time < cool_down:
                self.__special_time += 1
            else:
                self.__special_animate += 1
                self.__special_time = 0
            weapon = pygame.transform.scale(self.textures[f'heal{self.__special_animate}'], special_size)
            self.screen.blit(weapon, special_pos)    
        else: 
            self.player.special_skill = False
            self.__special_animate = 0
        
    def inventory(self):
        """
        Display inventory counts of pillars, vision potion & healing potions
        above the memo box. First half of code displays the iconds then
        displays counts of each.
        param: None, obtains info from self.textures and self.hero's inventory
        return: None
        """
        background_size = (45, HALF_HEIGHT + 185, 195, 38)
        pygame.draw.rect(self.screen, BLACK, background_size)        

        icon_size = (30, 30)
        y_pos = HALF_HEIGHT + 190
        x_pos = 50
        x_offset = 60
        pillar_pos = (x_pos, y_pos)
        pillar = pygame.transform.scale(self.textures['Pi'], icon_size)
        self.screen.blit(pillar, pillar_pos)

        v_pot_pos = (x_pos + x_offset, y_pos)
        v_pot = pygame.transform.scale(self.textures['Vi'], icon_size)
        self.screen.blit(v_pot, v_pot_pos)

        h_pot_pos = (x_pos + x_offset * 2, y_pos)
        h_pot = pygame.transform.scale(self.textures['Hi'], icon_size)
        self.screen.blit(h_pot, h_pot_pos)

        count_y_pos = y_pos + 13
        count_x_offset = 45
        pillar_count, p_pos = create_textline(str(len(self.hero.pillars)), 
                                            pos=(x_pos + count_x_offset, count_y_pos),
                                            font_type='GUI/font/28DaysLater.ttf', 
                                            size=30,
                                            color=YELLOW)
        self.screen.blit(pillar_count, p_pos)

        v_pot_count, vpc_pos = create_textline(str(self.hero.vision_potions), 
                                            pos=(x_pos + x_offset + count_x_offset, count_y_pos),
                                            font_type='GUI/font/28DaysLater.ttf', 
                                            size=30,
                                            color=WHITE)
        self.screen.blit(v_pot_count, vpc_pos)

        h_pot_count, hpc_pos = create_textline(str(self.hero.healing_potions), 
                                            pos=(x_pos + x_offset * 2 + count_x_offset, count_y_pos),
                                            font_type='GUI/font/28DaysLater.ttf', 
                                            size=30,
                                            color=RED)
        self.screen.blit(h_pot_count, hpc_pos)

    def mini_map(self):
        if self.player.show_map:
            map_surf = pygame.Surface((WIDTH // MAP_SCALE, HEIGHT // MAP_SCALE))
            xx, yy = self.player.x // MAP_SCALE, self.player.y // MAP_SCALE

            # Draws visited path
            for x, y in self.player.map_visited:
                pygame.draw.rect(map_surf, 'red', (x-8, y-8, MAP_TILE * 2, MAP_TILE * 2))

            # Draws wall (can use to reveal entire map)
            for x,y in self.map_coords:
                pygame.draw.rect(map_surf, 'black', (x, y, MAP_TILE, MAP_TILE))

            pygame.draw.circle(map_surf, 'green', (xx, yy), 5)
            pygame.draw.line(map_surf, 'green', (xx, yy), (xx + 12 * math.cos(self.player.angle),
                            yy + 12 * math.sin(self.player.angle)), 2)

            self.screen.blit(map_surf, MAP_POS)

    def fps_display(self, clock):
        fps_text = 'FPS ' + str(int(clock.get_fps()))
        fps_txt, fps_pos = create_textline(fps_text, 
                                            pos=(WIDTH-45, 15),
                                            font_type='GUI/font/28DaysLater.ttf', 
                                            size=30,
                                            color=WHITE)
        self.screen.blit(fps_txt, fps_pos)