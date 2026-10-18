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
        self.width = Width 
        self.height = Height

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

    def step(self):
        # 已结束的游戏不再移动
        if self.game_over:
            return

        # 移动蛇
        self._move()

        # 检测碰撞
        if self._is_collision():
            self.game_over = True

    def _apply_action(self, action):
        # 按顺时针排列四个方向
        clockwise = [
            Direction.RIGHT,
            Direction.DOWN,
            Direction.LEFT,
            Direction.UP 
        ]

        # 获取当前方向索引
        idx = clockwise.index(self.direction)
        if action == [1, 0, 0]:
            # 直行
            new_idx = idx
        elif action == [0, 1, 0]:
            # 右转 90 度
            new_idx = (idx + 1) % 4
        elif action == [0, 0, 1]:
            # 左转 90 度 
            new_idx = (idx - 1) % 4
        else:
            raise ValueError(f"Invalid action: {action}")

        # 更新方向
        self.direction = clockwise[new_idx]

    def play_step(self, action):
        # 游戏已经结束，不再执行动作
        if self.game_over:
            return 0, True, self.score

        # 记录移动前的分数
        old_score = self.score

        # 1. Agent 决定移动方向
        self._apply_action(action)

        # 2. 执行游戏更新
        self.step()

        # 3. 计算奖励
        if self.game_over and not self.won:
            reward = -10

        elif self.score > old_score:
            reward = 10
        else:
            reward = 0

        # 4. 返回反馈
        return reward, self.game_over, self.score
