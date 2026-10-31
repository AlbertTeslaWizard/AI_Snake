from collections import namedtuple
from enum import Enum

# 游戏窗口尺寸
WIDTH = 640
HEIGHT = 480

# 每一节蛇身的宽高
BLOCK_SIZE = 20


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple("Point", ["x", "y"])
