import math


# game settings
SCREEN_HEIGHT = 720
SCREEN_WIDTH = 720
FPS = 60

MAP_SIZE = 4 * 2 + 1        # (input here, 4 for 4x4 rooms) * 2 + 1
TILE_SIZE = int((SCREEN_WIDTH) / MAP_SIZE)
MAX_DEPTH = int(MAP_SIZE * TILE_SIZE)

FOV = math.pi / 3
HALF_FOV = FOV / 2
CASTED_RAYS = 120
STEP_ANGLE = FOV / CASTED_RAYS
SCALE = (SCREEN_WIDTH) / CASTED_RAYS

