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
WHITE = (255, 255, 255)
DARK_GRAY = (37, 34, 30)
GRAY = (211, 211, 211)
BLACK = (0, 0, 0)
DARK_TAN = (145, 129, 81)
PINK = (199, 36, 177)
RED = (139, 0, 0)
DARK_RED = (66, 13, 9)
# DARK_RED = (170, 1, 20)
# PURPLE = (128, 0, 128)
GREEN = (57, 255, 20)
# GREEN_NEON = (0, 255, 0)
