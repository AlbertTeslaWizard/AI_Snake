
import unittest

from game import SnakeGameAI, Direction, Point
from state import get_state


class TestState(unittest.TestCase):

    def setUp(self):
        self.game = SnakeGameAI()

        # 固定测试环境，避免随机食物位置影响结果
        self.game.head = Point(320, 240)
        self.game.direction = Direction.RIGHT
        self.game.snake = [
            self.game.head,
            Point(300, 240),
            Point(280, 240),
        ]
        self.game.food = Point(360, 260)

    def test_open_space(self):
        state = get_state(self.game)

        expected = [
            0, 0, 0,
            0, 1, 0, 0,
            0, 1, 0, 1,
        ]

        self.assertEqual(state, expected)

    def test_body_ahead(self):
        # 构造一个蛇身绕到前方和右侧的局面
        self.game.snake = [
            self.game.head,
            Point(300, 240),
            Point(300, 260),
            Point(320, 260),
            Point(340, 260),
            Point(340, 240),
            Point(360, 240),
        ]

        state = get_state(self.game)

        expected = [
            1, 1, 0,
            0, 1, 0, 0,
            0, 1, 0, 1,
        ]

        self.assertEqual(state, expected)

    def test_state_length(self):
        state = get_state(self.game)

        self.assertEqual(len(state), 11)
        self.assertTrue(
            all(value in (0, 1) for value in state)
        )


if __name__ == "__main__":
    unittest.main()

