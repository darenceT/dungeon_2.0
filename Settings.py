import math


# game settings
WIDTH = 720    
HEIGHT = 720
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 60
TILE = 80

# # map settings
# MAP_SIZE = 4 * 2 + 1        # (input here, 4 for 4x4 rooms) * 2 + 1
# TILE_SIZE = int(SCREEN_WIDTH / MAP_SIZE)

FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = 120
MAX_DEPTH = 800
DELTA_ANGLE = FOV / NUM_RAYS
DIST = NUM_RAYS / (2 * math.tan(HALF_FOV))
PROJ_COEFF = 3 * DIST * TILE
SCALE = WIDTH // NUM_RAYS

# # player settings
# player_pos = (HALF_WIDTH, HALF_HEIGHT)
# player_angle = 0
# player_speed = 2