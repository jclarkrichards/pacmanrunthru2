from vectors import Vector2D

UP = Vector2D(0, -1)
DOWN = Vector2D(0, 1)
LEFT = Vector2D(-1, 0)
RIGHT = Vector2D(1, 0)
STOP = Vector2D()

YELLOW = (255, 255, 0)

WIDTH = 16
HEIGHT = 16
NROWS = 36
NCOLS = 28
SCREENSIZE = (NCOLS*WIDTH, NROWS*HEIGHT)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


MAZEDATA = {}
MAZEDATA[0] = {}
MAZEDATA[0]["file"] = "maze1.txt"
MAZEDATA[0]["portal"] = {(0, 17*HEIGHT):(27*WIDTH, 17*HEIGHT)}
