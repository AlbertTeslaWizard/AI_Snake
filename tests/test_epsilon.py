from snake_ai.rl import DQNAgent

agent = DQNAgent(
    epsilon=1.0,
    epsilon_min=0.05,
    epsilon_decay=0.995
)

for episode in range(1, 501):
    agent.decay_epsilon()

    if episode in [1, 100, 300, 500]:
        print(
            f"Episode {episode}: "
            f"episode = {agent.epsilon:.4f}"
        )

