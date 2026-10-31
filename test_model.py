import torch 
from model import QNetwork

# 创建网络
model = QNetwork()

# 构造一个 11 维状态
state = torch.tensor(
    [[0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1]],
    dtype = torch.float32
)

# 前向传播
q_values = model(state)

print("输入形状:", state.shape)
print("输出形状:", q_values.shape)
print("Q值:", q_values)

# 选择 Q 值最大的动作
action = torch.argmax(q_values, dim = 1).item()
print("选择动作:", action)
