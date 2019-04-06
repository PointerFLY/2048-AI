import random
import enum

_2_PROBABILITY = 0.9
_ROW_COUNT = 4
_BEGIN_TILE_COUNT = 2


class Action(str):
    LEFT = 'left'
    RIGHT = 'right'
    UP = 'up'
    DOWN = 'down'


class Logic:
    def __init__(self):
        self.tiles_updated: callable = None
        self.game_ended: callable = None
        self.row_count = _ROW_COUNT
        self._matrix = [[0 for _ in range(self.row_count)] for _ in range(self.row_count)]
        self._available_actions_cache = None
        for _ in range(_BEGIN_TILE_COUNT):
            self._generate_next()

    def tile(self, i, j, transpose=False):
        if transpose:
            return self._matrix[j][i]
        else:
            return self._matrix[i][j]

    def _set_tile(self, i, j, value, transpose=False):
        self._available_actions_cache = None
        if transpose:
            self._matrix[j][i] = value
        else:
            self._matrix[i][j] = value

    def available_actions(self) -> list:
        if not self._available_actions_cache:
            actions = self._refresh_available_actions(True)
            actions = actions.union(self._refresh_available_actions(False))
            self._available_actions_cache = list(actions)

        return self._available_actions_cache

    def perform_action(self, action: Action):
        if not self.available_actions():
            self.game_ended()
            return

        if action not in self.available_actions():
            return

        dic = {
            Action.LEFT: (False, False),
            Action.RIGHT: (True, False),
            Action.UP: (False, True),
            Action.DOWN: (True, True),
        }

        reverse, transpose = dic[action]
        self._update_matrix(reverse, transpose)

        self._generate_next()
        self.tiles_updated()

        if not self.available_actions():
            self.game_ended()

    def _refresh_available_actions(self, transpose: bool):
        actions = set()
        for i in range(self.row_count):
            found_zero = False
            found_value = False

            for j in range(self.row_count):
                if self.tile(i, j, transpose) == 0:
                    found_zero = True
                    if found_value:
                        if transpose:
                            actions.add(Action.DOWN)
                        else:
                            actions.add(Action.RIGHT)
                elif self.tile(i, j, transpose) != 0:
                    found_value = True
                    if found_zero:
                        if transpose:
                            actions.add(Action.UP)
                        else:
                            actions.add(Action.LEFT)

                if j < self.row_count - 1:
                    if self.tile(i, j, transpose) != 0 and self.tile(i, j, transpose) == self.tile(i, j + 1, transpose):
                        if transpose:
                            actions.add(Action.UP)
                            actions.add(Action.DOWN)
                        else:
                            actions.add(Action.LEFT)
                            actions.add(Action.RIGHT)

                if len(actions) == 2:
                    return actions

        return actions

    def _update_matrix(self, reverse: bool, transpose: bool):
        indices = list(range(self.row_count))
        if reverse:
            indices.reverse()

        for i in indices:
            stack = []  # Use stack to track tiles
            merged = []  # Each tile can only merge once
            for j in indices:
                if self.tile(i, j, transpose) == 0:
                    continue

                if stack and not merged[-1] and stack[-1] == self.tile(i, j, transpose):
                    stack.append(2 * stack.pop())
                    merged[-1] = True
                else:
                    stack.append(self.tile(i, j, transpose))
                    merged.append(False)

            for j in indices:
                stack_idx = self.row_count - 1 - j if reverse else j
                if stack_idx < len(stack):
                    self._set_tile(i, j, stack[stack_idx], transpose)
                else:
                    self._set_tile(i, j, 0, transpose)

    def _generate_next(self):
        zero_tiles = []
        for i in range(self.row_count):
            for j in range(self.row_count):
                if self._matrix[i][j] == 0:
                    zero_tiles.append((i, j))

        i, j = zero_tiles[random.randrange(len(zero_tiles))]
        self._matrix[i][j] = 2 if random.random() < _2_PROBABILITY else 4
