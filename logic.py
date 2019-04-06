import random

_2_PROBABILITY = 0.9
_ROW_COUNT = 4
_BEGIN_TILE_COUNT = 2


class Action(int):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4


class Logic:
    def __init__(self):
        self.matrix_updated: callable = None
        self.row_count = _ROW_COUNT
        self.matrix = [[0 for _ in range(self.row_count)] for _ in range(self.row_count)]
        for _ in range(_BEGIN_TILE_COUNT):
            self._generate_next()

    def perform_action(self, action: Action):
        dic = {
            Action.LEFT: (False, False),
            Action.RIGHT: (True, False),
            Action.UP: (False, True),
            Action.DOWN: (True, True),
        }

        reverse, transpose = dic[action]
        self._update_matrix(reverse, transpose)

        self._generate_next()
        self.matrix_updated(self.matrix)

    def _update_matrix(self, reverse: bool, transpose: bool):
        indices = list(range(self.row_count))
        if reverse:
            indices.reverse()

        if transpose:
            def get_tile(i, j):
                return self.matrix[j][i]

            def set_tile(i, j, number):
                self.matrix[j][i] = number
        else:
            def get_tile(i, j):
                return self.matrix[i][j]

            def set_tile(i, j, number):
                self.matrix[i][j] = number

        for i in indices:
            stack = []  # Use stack to track tiles
            merged = []  # Each tile can only merge once
            for j in indices:
                if get_tile(i, j) == 0:
                    continue

                if stack and not merged[-1] and stack[-1] == get_tile(i, j):
                    stack.append(2 * stack.pop())
                    merged[-1] = True
                else:
                    stack.append(get_tile(i, j))
                    merged.append(False)

            for j in indices:
                stack_idx = self.row_count - 1 - j if reverse else j
                if stack_idx < len(stack):
                    set_tile(i, j, stack[stack_idx])
                else:
                    set_tile(i, j, 0)

    def _generate_next(self):
        zero_tiles = []
        for i in range(self.row_count):
            for j in range(self.row_count):
                if self.matrix[i][j] == 0:
                    zero_tiles.append((i, j))

        i, j = zero_tiles[random.randrange(len(zero_tiles))]
        self.matrix[i][j] = 2 if random.random() < _2_PROBABILITY else 4
