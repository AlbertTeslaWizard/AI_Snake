import random
from collections import deque

class ReplayBuffer:
    def __init__(self, capacity=100000):
        self.memory = deque(maxlen = capacity)

    def push(self, state, action, reward, next_state, done):
        transition = (
            state.copy(),
            int(action),
            float(reward),
            next_state.copy(),
            bool(done)
        )

        self.memory.append(transition)

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)
    
    def __len__(self):
        return len(self.memory)
