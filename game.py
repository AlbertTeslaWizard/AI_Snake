import pygame
import random
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

        # 创建用于显示得分的字体
        self.font = pygame.font.Font(None, 32)

        # 初始化游戏状态
        self.reset()

    def reset(self):
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

        self.score = 0
        self.game_over = False
        self.won = False
        self.paused = False

        self.food = None 
        self._place_food()

    def _place_food(self):
        available_cells = []
        # 遍历游戏地图上的所有格子
        for x in range(0, self.width, BLOCK_SIZE):
            for y in range(0, self.height, BLOCK_SIZE):
                cell = Point(x, y)
                # 不能把食物放蛇身上
                if cell not in self.snake:
                    available_cells.append(cell)

        if available_cells:
            self.food = random.choice(available_cells)
        else:
            # 整个地图已被占满
            self.food = None
            self.won = True
            self.game_over = True

    def _is_collision(self):
        # 检测是否撞墙
        if self.head.x < 0 or self.head.x >= self.width:
            return True
        if self.head.y < 0 or self.head.y >= self.height:
            return True
        
        # 检测是否碰撞到自己的身体
        if self.head in self.snake[1:]:
            return True
        
        return False

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


        # 绘制食物
        if self.food is not None:
            pygame.draw.rect(
                self.display,
                (220, 50, 50),
                (
                    self.food.x,
                    self.food.y,
                    BLOCK_SIZE,
                    BLOCK_SIZE
                )
            )

        score_text = self.font.render(
            f"Score: {self.score}",
            True,
            (255, 255, 255)
        )

        self.display.blit(score_text, (10, 10))

        # 游戏结束时显示提示
        if self.game_over:
            if self.won:
                message = "You Win!"
            else:
                message = "Game Over!"

            game_over_text = self.font.render(
                message,
                True,
                (255, 255, 255)
            )

            restart_text = self.font.render(
                "Press R to Restart",
                True,
                (255, 255, 255)
            )

            # 把提示绘制在窗口中央
            self.display.blit(
                game_over_text,
                game_over_text.get_rect(
                    center = (self.width // 2, self.height // 2 - 20)
                )
            )

            self.display.blit(
                restart_text,
                restart_text.get_rect(
                    center = (self.width // 2, self.height // 2 + 20)
                )
            )

        # 暂停时显示提示 
        if self.paused and not self.game_over:
            pause_text = self.font.render(
                "PAUSED - Press SPACE to Resume",
                True,
                (255, 255, 255)
            )

            pause_rect = pause_text.get_rect(
                center = (self.width // 2, self.height // 2)
            )

            self.display.blit(pause_text, pause_rect)

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

                    # 游戏结束后，按 R 重新开始
                    elif self.game_over:
                        if event.key == pygame.K_r:
                            self.reset()

                    # Space: 暂停或继续
                    elif event.key == pygame.K_SPACE:
                        self.paused = not self.paused

                    # 正常游戏时处理方向键
                    elif not self.paused and not turned_this_frame:
                        turned_this_frame = self._change_direction(event.key)

            if not running:
                break

            # 没有结束才继续移动
            if not self.game_over and not self.paused:
                self._move()

                # 判断移动后是否发生碰撞
                if self._is_collision():
                    self.game_over = True
            
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

        # 判断是否吃到食物
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            # 没吃到食物则删除蛇尾
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
