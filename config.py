WIN_WIDTH = 900
WIN_HEIGHT = 600
TILESIZE = 32
FPS = 60

tilemap = [
	'BBBBBBBBBBBBBBBBBBBB',
    'B..E...............B',
	'B..................B',
	'B....BBB...........B',
    'B........P.........B',
    'B..................B',
	'B..................B',
	'B.....BBB..........B',
    'B.......B.....E....B',
    'B.......B..........B',
	'B..................B',
	'B..................B',
    'B..................B',
	'B..................B',
	'BBBBBBBBBBBBBBBBBBBB',
]

WORLD_WIDTH = len(tilemap[0]) * TILESIZE * 10
WORLD_HEIGHT = len(tilemap) * TILESIZE * 10

PLAYER_LAYER = 4
ENEMY_LAYER = 3
BLOCK_LAYER = 2
GROUND_LAYER = 1

PLAYER_SPEED = 3
ENEMY_SPEED = 2

RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

