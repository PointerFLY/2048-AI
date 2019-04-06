import random

_2_PROBABILITY = 0.9


class Action(int):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4


class Logic:
    def __init__(self):
        self.matrix_updated: callable = None
        self.row_count = 4
        self.matrix = [[0 for _ in range(self.row_count)] for _ in range(self.row_count)]
        for _ in range(2):
            self._generate_next()

    def perform_action(self, action: Action):
        dic = {
            Action.LEFT: self._left,
            Action.RIGHT: self._right,
            Action.UP: self._up,
            Action.DOWN: self._down
        }
        dic[action]()
        # self._generate_next()
        self.matrix_updated(self.matrix)

    def _left(self):
        for i in range(self.row_count):
            stack = []
            merge = []
            for j in range(self.row_count):
                if self.matrix[i][j] == 0:
                    continue

                if stack and merge[-1] and stack[-1] == self.matrix[i][j]:
                    stack.append(2 * stack.pop())
                    merge[-1] = False
                else:
                    stack.append(self.matrix[i][j])
                    merge.append(True)

            for j in range(self.row_count):
                if j < len(stack):
                    self.matrix[i][j] = stack[j]
                else:
                    self.matrix[i][j] = 0

    def _right(self):
        for i in reversed(range(self.row_count)):
            stack = []
            merge = []
            for j in reversed(range(self.row_count)):
                if self.matrix[i][j] == 0:
                    continue

                if stack and merge[-1] and stack[-1] == self.matrix[i][j]:
                    stack.append(2 * stack.pop())
                    merge[-1] = False
                else:
                    stack.append(self.matrix[i][j])
                    merge.append(True)

            for j in reversed(range(self.row_count)):
                stack_idx = self.row_count - 1 - j
                if stack_idx < len(stack):
                    self.matrix[i][j] = stack[stack_idx]
                else:
                    self.matrix[i][j] = 0

    def _up(self):
        for i in range(self.row_count):
            stack = []
            merge = []
            for j in range(self.row_count):
                if self.matrix[j][i] == 0:
                    continue

                if stack and merge[-1] and stack[-1] == self.matrix[j][i]:
                    stack.append(2 * stack.pop())
                    merge[-1] = False
                else:
                    stack.append(self.matrix[j][i])
                    merge.append(True)

            for j in range(self.row_count):
                if j < len(stack):
                    self.matrix[j][i] = stack[j]
                else:
                    self.matrix[j][i] = 0

    def _down(self):
        for i in reversed(range(self.row_count)):
            stack = []
            merge = []
            for j in reversed(range(self.row_count)):
                if self.matrix[j][i] == 0:
                    continue

                if stack and merge[-1] and stack[-1] == self.matrix[j][i]:
                    stack.append(2 * stack.pop())
                    merge[-1] = False
                else:
                    stack.append(self.matrix[j][i])
                    merge.append(True)

            for j in reversed(range(self.row_count)):
                stack_idx = self.row_count - 1 - j
                if stack_idx < len(stack):
                    self.matrix[j][i] = stack[stack_idx]
                else:
                    self.matrix[j][i] = 0

    def _generate_next(self):
        zero_tiles = []
        for i in range(self.row_count):
            for j in range(self.row_count):
                if self.matrix[i][j] == 0:
                    zero_tiles.append((i, j))

        i, j = zero_tiles[random.randrange(len(zero_tiles))]
        self.matrix[i][j] = 2 if random.random() < _2_PROBABILITY else 4
