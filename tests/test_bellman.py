import torch

# 当前动作获得的奖励
reward = torch.tensor([0.0])

# 下一状态是否为终止状态
done = torch.tensor([False])

# 下一状态三个动作对应的 Q 值
next_q_values = torch.tensor([[1.2, 3.0, 2.0]])

# 折扣因子
gamma = 0.9

# 计算 Bellman Target
with torch.no_grad():
    max_next_q = next_q_values.max(dim = 1).values
    target = reward + gamma * (1 - done.float()) * max_next_q

print("Bellman Target:", target)
