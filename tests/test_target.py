import torch

from snake_ai.rl import DQNAgent

agent = DQNAgent()

# 获取两个网络的第一组参数
online_param = next(agent.model.parameters())
target_param = next(agent.target_model.parameters())

# 1. 初始化后应该相同
print(
    "初始化:",
    torch.equal(online_param, target_param)
)

# 2. 手动修改 Online Network 参数
with torch.no_grad():
    online_param.add_(0.1)

print(
    "Online 更新后:",
    torch.equal(online_param, target_param)
)

# 3. 同步 Target Network
agent.sync_target()

print(
    "同步 Target 后:",
    torch.equal(online_param, target_param)
)
