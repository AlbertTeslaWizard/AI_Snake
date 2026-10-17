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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

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

if __name__ == '__main__':
    game = SnakeGameAI()
    game.run()
