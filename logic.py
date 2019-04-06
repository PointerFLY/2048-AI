import random


class Action(int):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3


class Logic:
    def __init__(self):
        self.matrix_updated: callable = None

        self.row_count = 4
        self.matrix = [[2 for _ in range(self.row_count)] for _ in range(self.row_count)]

    def perform_action(self, action: Action):
        self._right()
        self.matrix_updated(self.matrix)
        print(self.matrix)

    def _right(self):
        i = 0
        while i < self.row_count:
            j = self.row_count - 2
            while j >= 0:
                if self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j+1]:
                    self.matrix[i][j+1] += self.matrix[i][j]
                    self.matrix[i][j] = 0
                    j -= 1
                j -= 1

            zero_index = None
            j = self.row_count - 1
            while j > 0:
                if self.matrix[i][j] == 0:
                    if not zero_index:
                        zero_index = j
                elif zero_index:
                    self.matrix[i][zero_index] = self.matrix[i][j]
                    self.matrix[i][j] = 0
                    zero_index -= 1
                j -= 1

            i += 1

    def _generate_next(self):
        # randomly generate1
        pass
