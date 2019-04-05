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
        self.matrix = [[0 for _ in range(self.row_count)] for _ in range(self.row_count)]

    def perform_action(self, action: Action):
        # merge if possible
        self.generate_next()
        self.matrix_updated(self.matrix)

    def generate_next(self):
        # randomly generate
        pass
