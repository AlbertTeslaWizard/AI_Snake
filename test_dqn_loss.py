import torch 
import torch.nn as nn

from model import QNetwork

torch.manual_seed(42)

# 1. 创建 Q 网络
model = QNetwork()

# 2. 创建优化器
optimizer = torch.optim.Adam(
    model.parameters(),
    lr = 0.001
)

# 3. 构造一个状态
state = torch.tensor(
    [[0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1]],
    dtype = torch.float32
)

# 4. 假设当前采取了左转动作
action = torch.tensor([[2]])

# 5. 假设这个动作导致游戏结束
target = torch.tensor([[-10.0]])

# 6. 前向传播, 预测三个 Q 值 
q_values = model(state)

# 7. 取出实际执行动作的 Q 值
q_pred = q_values.gather(1, action)

# 8. 计算损失
loss = nn.MSELoss()(q_pred, target)

print("预测Q值:", q_pred.item())
print("目标Q值:", target.item())
print("Loss:", loss.item())

# 9. 反向传播并更新参数
optimizer.zero_grad()
loss.backward()
optimizer.step()
