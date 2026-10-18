import pygame
from game import BLOCK_SIZE

class GameRenderer:
    def __init__(self, width, height):
        pygame.init()

        # 创建游戏窗口
        self.display = pygame.display.set_mode(
            (width, height) 
        )
        pygame.display.set_caption("Snake AI")

        # 创建字符
        self.font = pygame.font.Font(None, 32)

    def draw(self, game):
        # 清空窗口
        self.display.fill((20, 20, 20))

        # 绘制蛇身
        for segment in game.snake:
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
        if game.food is not None:
            pygame.draw.rect(
                self.display,
                (220, 50, 50),
                (
                    game.food.x,
                    game.food.y,
                    BLOCK_SIZE,
                    BLOCK_SIZE 
                )
            )

        # 绘制分数
        score_text = self.font.render(
            f"Score: {game.score}",
            True,
            (255, 255, 255)
        )
        self.display.blit(score_text, (10, 10))

        # 游戏结束时显示提示
        if game.game_over:
            if game.won:
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
                    center = (game.width // 2, game.height // 2 - 20)
                )
            )
        
            self.display.blit(
                restart_text,
                restart_text.get_rect(
                    center = (game.width // 2, game.height // 2 + 20)
                )
            )
        
        # 暂停时显示提示 
        if game.paused and not game.game_over:
            pause_text = self.font.render(
                "PAUSED - Press SPACE to Resume",
                True,
                (255, 255, 255)
            )
        
            pause_rect = pause_text.get_rect(
                center = (game.width // 2, game.height // 2)
            )
        
            self.display.blit(pause_text, pause_rect)

        # 刷新画面
        pygame.display.flip()


