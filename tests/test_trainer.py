from snake_ai.game import SnakeGameAI, get_state
from snake_ai.rl import DQNAgent, DQNTrainer, ReplayBuffer

# 1. 创建游戏、Agent、Replay Buffer
game = SnakeGameAI()
agent = DQNAgent(epsilon = 1.0)
memory = ReplayBuffer(capacity = 1000)

# 2. 创建 Trainer
trainer = DQNTrainer(
    model = agent.model,
    target_model = agent.target_model
)

# 3. 收集 100 条真实交互经验
for _ in range(100):
    state = get_state(game)
    action_idx, action = agent.select_action(state)
    reward, done, score = game.play_step(action)

    next_state = get_state(game)

    memory.push(
        state,
        action_idx,
        reward,
        next_state,
        done
    )

    if done:
        game.reset()

# 4. 随机采样 32 条经验
batch = memory.sample(batch_size = 32)

# 5. 执行一次 DQN 参数更新
loss = trainer.train_step(batch)

print("Replay Buffer 长度:", len(memory))
print("DQN Loss:", loss)
