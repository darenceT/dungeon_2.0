import pygame

from .Memo import Memo
from .Settings import *
from .Utility import create_textline

class Drawing: 
    """
    Class for drawing all images onto GUI surface. Sprite objects/images get 
    delivered here for blitting.
    """
    def __init__(self, screen, map_coords, player_controls, hero, sprites) -> None:
        self.screen = screen
        self.map_coords = map_coords
        self.player = player_controls
        self.hero = hero
        self.sprites = sprites
        self.textures = {
                        #  'floor': pygame.image.load('GUI/img/floor.jpg').convert(),
                         'ceiling': pygame.image.load('GUI/img/ceiling3.jpg').convert(),
                         'door': pygame.image.load('GUI/img/door_portal.png').convert(),
                         'wall': pygame.image.load('GUI/img/wall_default2.png').convert_alpha(),
                         'Hi': pygame.image.load('GUI/img/health_icon.png').convert_alpha(),
                         'Vi': pygame.image.load('GUI/img/vision_large.png').convert_alpha(),
                         'Pi': pygame.image.load('GUI/img/pillar.png').convert_alpha(),
                         'S0': pygame.image.load('GUI/img/sword0.png').convert_alpha(),
                         'S1': pygame.image.load('GUI/img/sword1.png').convert_alpha(),
                         'S2': pygame.image.load('GUI/img/sword2.png').convert_alpha()
                        #  'wall': pygame.image.load('GUI/img/wall_vision2.png').convert_alpha()
                         }

    def background(self):
        sky_offset = -5 * math.degrees(self.player.angle) % WIDTH
        self.screen.blit(self.textures['ceiling'], (sky_offset, 0))
        self.screen.blit(self.textures['ceiling'], (sky_offset - WIDTH, 0))
        self.screen.blit(self.textures['ceiling'], (sky_offset + WIDTH, 0))
        pygame.draw.rect(self.screen, DARK_TAN, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))

    def world(self, world_objects): 
        for obj in sorted(world_objects, key=lambda n: n[0], reverse=True):
            if obj[0]:
                _, object, object_pos = obj
                self.screen.blit(object, object_pos)

    def weapon_and_ui(self, clock):
        self.weapon()
        self.hero_health_bar()
        self.enemy_health_bar()
        self.inventory()
        self.mini_map()
        self.fps_display(clock)

    def weapon(self):
        # TODO change weapon "S" based on hero's class
        wep_pos = (WIDTH * 2/5, HEIGHT * 5/8)
        if self.player.attacking and self.weapon_animate < 3:
            weapon = pygame.transform.scale(self.textures[f'S{self.weapon_animate}'], wep_pos)
            self.screen.blit(weapon, wep_pos)
            self.weapon_animate += 1
        else:
            weapon = pygame.transform.scale(self.textures['S0'], wep_pos)
            self.weapon_animate = 1
            self.player.attacking = False
        self.screen.blit(weapon, wep_pos)

    def hero_health_bar(self):
        """
        Display hero's health bar, red as background for health lost, 
        underneath amount of current health
        bar_info = [left_pos, top_pos, width(health amount), height]
        """
        bar_info = [WIDTH - 180, HEIGHT - 60, 150, 30]

        pygame.draw.rect(self.screen, RED, bar_info)
        bar_info[2] *= self.hero.hit_points / 100
        pygame.draw.rect(self.screen, GREEN, bar_info)

    def enemy_health_bar(self):
        """
        Display nearby enemy's health bar
        bar_info = [left_pos, top_pos, width(health amount), height]
        """
        bar_info = [HALF_WIDTH - 100, 80, 150, 40]
        for object in self.sprites.nearby_sprites:
            if object.letter == 'M' and object.visible_health:
                bar_info[2] *= object.hitpoint / 100
                pygame.draw.rect(self.screen, PINK, bar_info)

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