import random
from typing import Optional

_2_PROBABILITY = 0.9
_ROW_COUNT = 4
_BEGIN_TILE_COUNT = 2


class Action(str):
    LEFT = 'left'
    RIGHT = 'right'
    UP = 'up'
    DOWN = 'down'


class State:
    def __init__(self):
        self.row_count = _ROW_COUNT
        self.two_odds = _2_PROBABILITY
        self.matrix = [[0 for _ in range(self.row_count)] for _ in range(self.row_count)]
        self.ui_dirty = True
        self.score = 0
        self._legal_actions_cache = None
        for _ in range(_BEGIN_TILE_COUNT):
            self._generate_next()

    def get_successors(self, action: Action) -> [('State', int)]:
        direct_state = self.direct_successor(action)
        if not direct_state:
            return []

        successors = []
        for i, j in direct_state.empty_tiles():
            successor = direct_state.copy()
            successor.matrix[i][j] = 2
            successors.append((successor, 2))

            successor = direct_state.copy()
            successor.matrix[i][j] = 4
            successors.append((successor, 4))

        return successors

    def direct_successor(self, action) -> Optional['State']:
        if action not in self.legal_actions():
            return None

        reverse, transpose = self._reverse_transpose(action)

        state = self.copy()
        state._update_matrix(reverse, transpose)
        return state

    def get_merges(self, action) -> {int, int}:
        if action not in self.legal_actions():
            return {}

        reverse, transpose = self._reverse_transpose(action)

        indices = list(range(self.row_count))
        if reverse:
            indices.reverse()

        merges = {}
        for i in indices:
            candidate = None
            for j in indices:
                if self._tile(i, j, transpose) == 0:
                    continue

                number = self._tile(i, j, transpose)
                if candidate and candidate == number:
                    result = candidate * 2
                    if merges.get(result):
                        merges[result] += 1
                    else:
                        merges[result] = 1
                    candidate = None
                else:
                    candidate = number

        return merges

    def empty_tiles(self):
        empty_tiles = []
        for i in range(self.row_count):
            for j in range(self.row_count):
                if self.matrix[i][j] == 0:
                    empty_tiles.append((i, j))

        return empty_tiles

    def legal_actions(self) -> list:
        if not self._legal_actions_cache:
            actions = self._refresh_legal_actions(True)
            actions = actions.union(self._refresh_legal_actions(False))
            self._legal_actions_cache = list(actions)

        return self._legal_actions_cache

    def perform_action(self, action: Action):
        if not self.legal_actions():
            return

        if action not in self.legal_actions():
            return

        reverse, transpose = self._reverse_transpose(action)
        self._update_matrix(reverse, transpose)
        self._generate_next()

        self.ui_dirty = True

    def copy(self):
        state = State()
        state._legal_actions_cache = self._legal_actions_cache
        for i in range(self.row_count):
            for j in range(self.row_count):
                state.matrix[i][j] = self.matrix[i][j]
        return state

    def _reverse_transpose(self, action):
        dic = {
            Action.LEFT: (False, False),
            Action.RIGHT: (True, False),
            Action.UP: (False, True),
            Action.DOWN: (True, True),
        }
        return dic[action]

    def _tile(self, i, j, transpose=False):
        if transpose:
            return self.matrix[j][i]
        else:
            return self.matrix[i][j]

    def _set_tile(self, i, j, value, transpose=False):
        self._legal_actions_cache = None
        if transpose:
            self.matrix[j][i] = value
        else:
            self.matrix[i][j] = value

    def _refresh_legal_actions(self, transpose: bool):
        actions = set()
        for i in range(self.row_count):
            found_zero = False
            found_value = False

            for j in range(self.row_count):
                if self._tile(i, j, transpose) == 0:
                    found_zero = True
                    if found_value:
                        if transpose:
                            actions.add(Action.DOWN)
                        else:
                            actions.add(Action.RIGHT)
                elif self._tile(i, j, transpose) != 0:
                    found_value = True
                    if found_zero:
                        if transpose:
                            actions.add(Action.UP)
                        else:
                            actions.add(Action.LEFT)

                if j < self.row_count - 1:
                    if self._tile(i, j, transpose) != 0 and self._tile(i, j, transpose) == self._tile(i, j + 1, transpose):
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
                if self._tile(i, j, transpose) == 0:
                    continue

                if stack and not merged[-1] and stack[-1] == self._tile(i, j, transpose):
                    v = 2 * stack.pop()
                    stack.append(v)
                    self.score += v
                    merged[-1] = True
                else:
                    stack.append(self._tile(i, j, transpose))
                    merged.append(False)

            for j in indices:
                stack_idx = self.row_count - 1 - j if reverse else j
                if stack_idx < len(stack):
                    self._set_tile(i, j, stack[stack_idx], transpose)
                else:
                    self._set_tile(i, j, 0, transpose)

    def _generate_next(self):
        empty_tiles = self.empty_tiles()
        i, j = empty_tiles[random.randrange(len(empty_tiles))]
        self.matrix[i][j] = 2 if random.random() < self.two_odds else 4
