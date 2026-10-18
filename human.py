import pygame
from game import Direction

class HumanController:
    def __init__(self, game, render, fps=8):
        self.game = game
        self.renderer = render

        # 控制游戏帧率
        self.clock = pygame.time.Clock()
        self.fps = fps

    def run(self):
        running = True

        while running:
            # 每帧最多转向一次
            turned_this_frame = False
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    # ESC: 退出游戏
                    if event.key == pygame.K_ESCAPE:
                        running = False

                    # 游戏结束后按 R 重启
                    elif self.game.game_over:
                        if event.key == pygame.K_r:
                            self.game.reset()

                    # Space: 暂停或继续
                    elif event.key == pygame.K_SPACE:
                        self.game.paused = not self.game.paused

                    elif not self.game.paused and not turned_this_frame:
                        turned_this_frame = self._change_direction(
                            event.key
                        )
            
            if not running:
                break

            # 游戏运行中才执行行动
            if not self.game.game_over and not self.game.paused:
                self.game.step()

            # 绘制游戏画面
            self.renderer.draw(self.game)

            # 控制游戏帧率
            self.clock.tick(self.fps)
        
        pygame.quit()
    
    def _change_direction(self, key):
        # 键盘按键与方向的映射
        key_map = {
            pygame.K_UP: Direction.UP,
            pygame.K_DOWN: Direction.DOWN,
            pygame.K_LEFT: Direction.LEFT,
            pygame.K_RIGHT: Direction.RIGHT
        }

        new_direction = key_map.get(key)
        
        if new_direction is None:
            return False
        
        # 相反方向映射
        opposite = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT

        }

        # 禁止直接反向
        if new_direction == opposite[self.game.direction]:
            return False 

        # 相同方向无需改变
        if new_direction == self.game.direction:
            return False
        
        self.game.direction = new_direction
        return True 
