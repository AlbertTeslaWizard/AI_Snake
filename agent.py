import random 
import torch 

from model import QNetwork

class DQNAgent:
    def __init__(self, epsilon = 1.0, epsilon_min = 0.05, epsilon_decay = 0.995):
        self.model = QNetwork()
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay

    def select_action(self, state):
        # 1.探索: 随机选择动作
        if random.random() < self.epsilon:
            action_idx = random.randint(0, 2)

        # 2.利用: 选择 Q 值最大的动作
        else:
            state_tensor = torch.tensor(
                state,
                dtype = torch.float32
            ).unsqueeze(0)

            with torch.no_grad():
                q_values = self.model(state_tensor)
                action_idx = torch.argmax(q_values, dim = 1).item()

        # 3. 将动作索引转换为 One-Hot
        action = [0, 0, 0]
        action[action_idx] = 1

        return action_idx, action
    
    def decay_epsilon(self):
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

