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
        terminated = False

        return self.state, reward, terminated, False, {}

    def sample_action(self):
        return self.action_space.sample(mask=np.ones(4, dtype=np.int8))

    def _act(self, action):
        reverse_transposes = [
            (False, False),
            (True, False),
            (False, True),
            (True, True),
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
