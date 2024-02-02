import io
import sys
import typing

import gymnasium as gym
import numpy as np
from gymnasium import spaces


class Gym2048(gym.Env[typing.Tuple, np.int64]):
    metadata = {
        "render.modes": ["human"],
    }
    action_space = spaces.Discrete(4)
    observation_space = spaces.Tuple((spaces.Discrete(16) for _ in range(16)))

    def reset(self):
        self.state = np.zeros((4, 4), dtype=np.int32)
        self._add_tile()
        self._add_tile()
        self.score = 0
        return self.state, {}

    def step(self, action):
        assert self.action_space.contains(action)
        prev_score = self.score

        self._act(action)
        self._add_tile()

        reward = self.score - prev_score
        terminated = self._is_terminated()

        return self.state, reward, terminated, False, {}

    def highest_tile(self):
        return np.max(self.state)

    def sample_action(self):
        actions = self._legal_actions(False)
        actions = actions.union(self._legal_actions(True))
        return np.random.choice(list(actions))

    def _is_terminated(self):
        return not self._legal_actions(False) and not self._legal_actions(True)

    def _act(self, action):
        reverse_transposes = [
            (False, False),  # left
            (True, False),  # right
            (False, True),  # up
            (True, True),  # down
        ]
        reverse, transpose = reverse_transposes[action]
        self._update_state(reverse, transpose)

    def _update_state(self, reverse: bool, transpose: bool):
        indices = list(range(self.state.shape[0]))
        if reverse:
            indices.reverse()

        for i in indices:
            stack = []  # Use stack to track tiles
            merged = []  # Each tile can only merge once
            for j in indices:
                if self._tile(i, j, transpose) == 0:
                    continue

                if (
                    stack
                    and not merged[-1]
                    and stack[-1] == self._tile(i, j, transpose)
                ):
                    v = 2 * stack.pop()
                    stack.append(v)
                    self.score += v
                    merged[-1] = True
                else:
                    stack.append(self._tile(i, j, transpose))
                    merged.append(False)

            for j in indices:
                stack_idx = self.state.shape[0] - 1 - j if reverse else j
                if stack_idx < len(stack):
                    self._set_tile(i, j, stack[stack_idx], transpose)
                else:
                    self._set_tile(i, j, 0, transpose)

    def _legal_actions(self, transpose: bool):
        actions = set()
        for i in range(self.state.shape[0]):
            found_zero = False
            found_value = False

            for j in range(self.state.shape[0]):
                if self._tile(i, j, transpose) == 0:
                    found_zero = True
                    if found_value:
                        if transpose:
                            actions.add(3)
                        else:
                            actions.add(2)
                elif self._tile(i, j, transpose) != 0:
                    found_value = True
                    if found_zero:
                        if transpose:
                            actions.add(2)
                        else:
                            actions.add(0)

                if j < self.state.shape[0] - 1:
                    if self._tile(i, j, transpose) != 0 and self._tile(
                        i, j, transpose
                    ) == self._tile(i, j + 1, transpose):
                        if transpose:
                            actions.add(2)
                            actions.add(3)
                        else:
                            actions.add(0)
                            actions.add(1)

                if len(actions) == 2:
                    return actions

        return actions

    def _tile(self, i, j, transpose=False):
        if transpose:
            return self.state[j, i]
        else:
            return self.state[i, j]

    def _set_tile(self, i, j, value, transpose=False):
        if transpose:
            self.state[j, i] = value
        else:
            self.state[i, j] = value

    def _add_tile(self):
        rows, cols = np.where(self.state == 0)
        i = np.random.choice(rows)
        j = np.random.choice(cols)
        self.state[i, j] = 2 if np.random.random() < 0.9 else 4

    def render(self, mode="human"):
        pass

    def close(self):
        pass
