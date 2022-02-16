import pygame

from Settings import *
from Raycast3D import Raycast

class Drawing: 
    def __init__(self, screen, map_coords) -> None:
        self.screen = screen
        self.map_coords = map_coords
        self.textures = {'wall': pygame.image.load('img/wall1.jpg').convert(),
                         '2': pygame.image.load('img/wall1.jpg').convert(),
                         'floor': pygame.image.load('img/floor.jpg').convert(),
                         'ceiling': pygame.image.load('img/ceiling.jfif').convert()
                         }
    
    def background(self, angle):
        sky_offset = -5 * math.degrees(angle) % WIDTH
        self.screen.blit(self.textures['ceiling'], (sky_offset, 0))
        self.screen.blit(self.textures['ceiling'], (sky_offset - WIDTH, 0))
        self.screen.blit(self.textures['ceiling'], (sky_offset + WIDTH, 0))
        pygame.draw.rect(self.screen, 'darkgray', (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))

    def world(self, screen, player_pos, player_angle, world_coords): 
        Raycast.view_3D(screen, player_pos, player_angle, world_coords, self.textures)

    def mini_map(self, player):
        map_surf = pygame.Surface((WIDTH // MAP_SCALE, HEIGHT // MAP_SCALE))
        map_surf.fill('black')
        xx, yy = player.x // MAP_SCALE, player.y // MAP_SCALE
        
        pygame.draw.circle(map_surf, 'green', (xx, yy), 5)
        pygame.draw.line(map_surf, 'green', (xx, yy), (xx + 12 * math.cos(player.angle),
                        yy + 12 * math.sin(player.angle)), 2)
        for x,y in self.map_coords:
            pygame.draw.rect(map_surf, 'gray', (x, y, MAP_TILE, MAP_TILE))
        self.screen.blit(map_surf, MAP_POS)

    def fps_display(self, clock):
        fps = str(int(clock.get_fps()))
        font = pygame.font.SysFont('Monospace Regular', 30)
        fps_surface = font.render(fps, False, (255, 255, 255))
        self.screen.blit(fps_surface, (480, 0))