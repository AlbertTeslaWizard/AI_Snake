from game import SnakeGameAI
from renderer import GameRenderer

def main():
    # 创建游戏对象
    game = SnakeGameAI()

    # 创建图形渲染器
    renderer = GameRenderer(
        game.width,
        game.height
    )

    game.run(renderer)

if __name__ == '__main__':
    main()
