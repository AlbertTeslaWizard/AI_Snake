from pathlib import Path

# 项目根目录（snake_ai/ 的上一级）
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 训练好的模型权重存放位置
CHECKPOINT_DIR = PROJECT_ROOT / "checkpoints"
MODEL_PATH = CHECKPOINT_DIR / "snake_dqn.pth"
