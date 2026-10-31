from snake_ai.game import SnakeGameAI
from snake_ai.ui import GameRenderer, HumanController


def main():
    # 创建游戏对象
    game = SnakeGameAI()

    # 创建图形渲染器
    renderer = GameRenderer(
        game.width,
        game.height
    )

    controller = HumanController(
        game,
        renderer,
        fps=8
    )

    # 启动游戏
    controller.run()

if __name__ == '__main__':
    main()
