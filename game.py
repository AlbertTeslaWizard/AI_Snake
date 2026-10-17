import pygame
from enum import Enum
from collections import namedtuple

# 游戏窗口尺寸
Width = 640
Height = 480

# 每一节蛇身的宽高
BLOCK_SIZE = 20

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple("Point", ["x", "y"])


class SnakeGameAI:
    def __init__(self):
        pygame.init()
        self.width = Width 
        self.height = Height

        # 创建游戏窗口
        self.display = pygame.display.set_mode(
            (self.width, self.height)
        )
        pygame.display.set_caption("Snake AI")

        # 控制帧率
        self.clock = pygame.time.Clock()

        # 初始化蛇的方向和身体
        self.direction = Direction.RIGHT

        self.head = Point(
            self.width // 2,
            self.height // 2
        )

        self.snake = [
            self.head,
            Point(self.head.x - BLOCK_SIZE, self.head.y),
            Point(self.head.x - 2 * BLOCK_SIZE, self.head.y)
        ]

    def draw(self):
        # 清空窗口
        self.display.fill((20, 20, 20))

        # 绘制每一节蛇身
        for segment in self.snake:
            pygame.draw.rect(
                self.display,
                (0, 200, 100),
                (
                    segment.x,
                    segment.y,
                    BLOCK_SIZE,
                    BLOCK_SIZE
                )
            )

        pygame.display.flip()

    def run(self):
        running = True

        while running:
            # 当前游戏帧是否已经转向
            turned_this_frame = False
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    # 按 ESC 退出
                    if event.key == pygame.K_ESCAPE:
                        running = False

                    # 每一帧最多改变一次方向
                    elif not turned_this_frame:
                        turned_this_frame = self._change_direction(event.key)

            if not running:
                break

            # 更新蛇的位置
            self._move()
            
            # 绘制游戏画面
            self.draw()

            # 控制帧率
            self.clock.tick(8)
        
        pygame.quit()

    def _move(self):
        x = self.head.x
        y = self.head.y

        # 根据当前方向更新蛇头坐标
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        
        # 创建新的蛇头
        self.head = Point(x, y)

        # 将新蛇头放到列表开头
        self.snake.insert(0, self.head)

        # 删除最后一节蛇尾
        self.snake.pop()

    def _change_direction(self, key):
        # 将键盘按键映射到移动方向
        key_map = {
            pygame.K_UP: Direction.UP,
            pygame.K_DOWN: Direction.DOWN,
            pygame.K_LEFT: Direction.LEFT,
            pygame.K_RIGHT: Direction.RIGHT
        }

        new_direction = key_map.get(key)

        # 不是方向键不处理
        if new_direction is None:
            return False 

        # 定义每个方向的相反方向
        opposite = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT 
        }
        
        # 禁止直接反向或者重复转向
        if new_direction == opposite[self.direction]:
            return False
        
        if new_direction == self.direction:
            return False
        
        self.direction = new_direction
        return True

if __name__ == '__main__':
    game = SnakeGameAI()
    game.run()
