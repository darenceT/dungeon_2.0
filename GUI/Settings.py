import math

PI = math.pi

# game settings
WIDTH = 720    
HEIGHT = 720
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 40
TILE = 80
FPS_POS = (WIDTH - 65, 5)

# player control settings
def convert_coords_to_pixel(coord: int):
    adjust_center = 120
    #TODO Variable for 2
    return int(2 * coord * WIDTH / TEXTURE_SCALE + adjust_center)

# minimap settings
MAP_SCALE = 5
MAP_TILE = TILE // MAP_SCALE
MAP_POS = (0, 0) # (0, HEIGHT - HEIGHT // MAP_SCALE) # bottom left

# raycast settings
FOV = PI / 3
HALF_FOV = FOV / 2
NUM_RAYS = 180
MAX_DEPTH = 800
DELTA_ANGLE = FOV / NUM_RAYS
DIST = NUM_RAYS / (2 * math.tan(HALF_FOV))
PROJ_COEFF = 3 * DIST * TILE
SCALE = WIDTH // NUM_RAYS


# texture settings
TEXTURE_WIDTH = 720
TEXTURE_HEIGHT = 720
TEXTURE_SCALE = TEXTURE_WIDTH // TILE


# sprite settings
DOUBLE_PI = PI * 2
CENTER_RAY = NUM_RAYS // 2 - 1
FAKE_RAYS = 100
FAKE_RAYS_RANGE = NUM_RAYS - 1 + 2 * FAKE_RAYS


# colors for drawing.py
DARK_TAN = (145, 129, 81)
RED = (139,0,0)
GREEN = (57, 255, 20)
PINK = (199,36,177)
WHITE = (255, 255, 255)