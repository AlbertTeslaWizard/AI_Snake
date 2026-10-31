from replay_buffer import ReplayBuffer

buffer = ReplayBuffer(capacity=3)

for i in range(5):
    state = [i] * 11
    next_state = [i + 1] * 11

    buffer.push(
        state = state,
        action = i % 3,
        reward = float(i),
        next_state = next_state,
        done = False 
    )

print("Buffer 长度:", len(buffer))
print("当前保存的经验:")

for transition in buffer.memory:
    print(transition)

print("\n随机抽取两条经验:")
batch = buffer.sample(batch_size = 2)

for transition in batch:
    print(transition)
