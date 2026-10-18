from game import Direction, Point, BLOCK_SIZE

def next_point(point, direction):
    offsets = {
        Direction.RIGHT: (BLOCK_SIZE, 0),
        Direction.DOWN: (0, BLOCK_SIZE),
        Direction.LEFT: (-BLOCK_SIZE, 0),
        Direction.UP: (0, -BLOCK_SIZE)
    }

    dx, dy = offsets[direction]

    return Point(point.x + dx, point.y + dy)

def get_state(game):
    clockwise = [
        Direction.RIGHT,
        Direction.DOWN,
        Direction.LEFT,
        Direction.UP,
    ]

    idx = clockwise.index(game.direction)

    # 当前朝向及相对左右方向
    direction_straight = clockwise[idx]
    direction_right = clockwise[(idx + 1) % 4]
    direction_left = clockwise[(idx - 1) % 4]

    # 检查三个候选位置是否危险
    danger_straight = game._is_collision(
        next_point(game.head, direction_straight)
    )

    danger_right = game._is_collision(
        next_point(game.head, direction_right)
    )

    danger_left = game._is_collision(
        next_point(game.head, direction_left)
    )

    # 当前移动方向
    direction_l = game.direction == Direction.LEFT
    direction_r = game.direction == Direction.RIGHT
    direction_u = game.direction == Direction.UP
    direction_d = game.direction == Direction.DOWN

    # 食物相对于蛇头的位置
    food_l = (
        game.food is not None and game.food.x < game.head.x
    )

    food_r = (
        game.food is not None and game.food.x > game.head.x 
    )

    food_u = (
        game.food is not None and game.food.y < game.head.y 
    )

    food_d = (
        game.food is not None and game.food.y > game.head.y
    )

    state = [
        danger_straight,
        danger_right,
        danger_left,

        # 移动方向 
        direction_l,
        direction_r,
        direction_u,
        direction_d,

        # 食物方向
        food_l,
        food_r,
        food_u,
        food_d
    ]

    return [int(value) for value in state]
