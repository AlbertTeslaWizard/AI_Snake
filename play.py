import pygame
import torch

from snake_ai.config import MODEL_PATH
from snake_ai.game import SnakeGameAI, get_state
from snake_ai.rl import DQNAgent
from snake_ai.ui import GameRenderer

FPS = 10

def play():
    # 1. 初始化游戏
    game = SnakeGameAI()
    renderer = GameRenderer(
        game.width,
        game.height
    )

    # 2. 创建 Agent, 关闭随机搜索
    agent = DQNAgent(epsilon = 0.0)

    # 3. 加载训练好的模型参数
    agent.model.load_state_dict(
        torch.load(
            MODEL_PATH,
            map_location = "cpu",
            weights_only = True
        )
    )

    # 4. 切换为推理模式
    agent.model.eval()

    clock = pygame.time.Clock()
    running = True

    # 5. 开始游戏
    while running:
        # 处理窗口事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    game.reset()

        if not running:
            break

        # 6. Agent 自动选择动作
        if not game.game_over:
            state = get_state(game)
            _, action = agent.select_action(state)

            game.play_step(action)

        # 7. 渲染游戏
        renderer.draw(game)
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    play()
