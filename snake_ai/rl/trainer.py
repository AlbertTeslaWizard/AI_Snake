import torch
from torch import nn


class DQNTrainer:
    def __init__(self, model, target_model, lr = 0.001, gamma = 0.9):
        self.model = model
        self.target_model = target_model
        self.gamma = gamma

        self.optimizer = torch.optim.Adam(
            self.model.parameters(),
            lr = lr
        )

        self.criterion = nn.SmoothL1Loss()

    def train_step(self, batch):
        # 1. 拆分 Mini-Batch
        states, actions, rewards, next_states, dones = zip(*batch, strict=True)

        # 2. 转换为 Tensor
        states = torch.tensor(states, dtype = torch.float32)
        actions = torch.tensor(actions, dtype = torch.long).unsqueeze(1)
        rewards = torch.tensor(rewards, dtype = torch.float32)
        next_states = torch.tensor(next_states, dtype = torch.float32)
        dones = torch.tensor(dones, dtype = torch.float32)

        # 3. Online Network 预测当前 Q 值
        q_values = self.model(states)

        q_pred = q_values.gather(1, actions).squeeze(1)

        # 4. Target Network 计算 Bellman Target
        with torch.no_grad():
            next_q_values = self.target_model(next_states)
            max_next_q = next_q_values.max(dim = 1).values
            q_target = rewards + self.gamma * (1 - dones) * max_next_q

        # 5. 计算 DQN Loss
        loss = self.criterion(q_pred, q_target)

        # 6. 反向传播
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return loss.item()
