from typing import Callable


class Action(int):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3


class Logic:
    def __init__(self):
        self.matrix_updated: Callable[[list], None] = None
        self.matrix = [[] * 4] * 4

    def perform_action(self, action: Action):
        pass  # Can merge?
        self.matrix_updated(self.matrix)

    def generate_next_tile(self):
        # randomly generate
        self.matrix_updated(self.matrix)
