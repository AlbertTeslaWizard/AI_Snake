from game import SnakeGameAI
from renderer import GameRenderer
from human import HumanController

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
