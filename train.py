import random

import torch

from snake_ai.config import MODEL_PATH
from snake_ai.game import SnakeGameAI, get_state
from snake_ai.rl import DQNAgent, DQNTrainer, ReplayBuffer

# 训练配置
EPISODES = 500
BATCH_SIZE = 64
MEMORY_SIZE = 100000
WARMUP_STEPS = 1000
TARGET_UPDATE = 500
MAX_STEPS_PER_EPISODE = 500

def train():
    # 1. 固定随机种子
    random.seed(42)
    torch.manual_seed(42)

    # 2. 初始化环境和智能体
    game = SnakeGameAI()
    agent = DQNAgent()

    memory = ReplayBuffer(capacity = MEMORY_SIZE)
    trainer = DQNTrainer(model = agent.model, target_model = agent.target_model)

    scores = []
    train_steps = 0

    # 3. 开始训练
    for episode in range(1, EPISODES + 1):
        game.reset()
        episode_reward = 0
        episode_losses = []
        current_epsilon = agent.epsilon
        score = 0

        #4. 当前 Episode 的交互过程
        for _ in range(MAX_STEPS_PER_EPISODE):
            # 获取当前状态
            state = get_state(game)

            # Agent 选择动作
            action_idx, action = agent.select_action(state)

            # 环境执行动作
            reward, done, score = game.play_step(action)

            # 获取下一状态
            next_state = get_state(game)

            # 保存经验
            memory.push(
                state,
                action_idx,
                reward,
                next_state,
                done
            )

            episode_reward += reward

            # 5. Replay Buffer 预热后开始训练
            if len(memory) >= max(WARMUP_STEPS, BATCH_SIZE):
                batch = memory.sample(BATCH_SIZE)
                loss = trainer.train_step(batch)
                episode_losses.append(loss)

                train_steps += 1

                # 6. 定期同步 Target Network
                if train_steps % TARGET_UPDATE == 0:
                    agent.sync_target()

            # 游戏结束
            if done:
                break

        # 7. 当前 Episode 结束
        scores.append(score)

        # 更新探索率
        agent.decay_epsilon()

        # 计算最近 50 局平均得分
        avg_score = sum(scores[-50:]) / len(scores[-50:])

        # 计算当前 Episode 平均 Loss
        avg_loss = (
            sum(episode_losses) / len(episode_losses)
            if episode_losses else None
        )

        loss_text = (
            f"{avg_loss:.4f}"
            if avg_loss is not None else "warmup"
        )

        print(
            f"Episode {episode:4d} | "
            f"Score: {score:2d} | "
            f"Avg50: {avg_score:.2f} | "
            f"Epsilon: {current_epsilon: .3f} | "
            f"Loss: {loss_text}"
        )

    # 8. 保存训练后的模型
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        agent.model.state_dict(),
        MODEL_PATH
    )

    print("Training finished!")

if __name__ == "__main__":
    train()

