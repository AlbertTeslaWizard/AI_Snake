from game import SnakeGameAI 
from state import get_state
from agent import DQNAgent

# 1. 创建游戏环境
game = SnakeGameAI()

# 2. 创建智能体
agent = DQNAgent(epsilon = 1.0)

# 3. 获取当前状态
state = get_state(game)

# 4. 选择动作
action_idx, action = agent.select_action(state)

print("当前状态:", state)
print("动作索引:", action_idx)
print("One-Hot 动作:", action)

# 5. 执行动作
reward, done, score = game.play_step(action)

print("奖励:", reward)
print("是否结束:", done)
print("当前分数:", score)


