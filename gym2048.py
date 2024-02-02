import typing
import numpy as np
import gymnasium as gym
from gymnasium import spaces


class Gym2048(gym.Env[typing.Tuple, np.int64]):
    metadata = {
        "render.modes": ["human"],
        "render_fps": 10,
    }
    action_space = spaces.Discrete(4)
    observation_space = spaces.Tuple((spaces.Discrete(16) for _ in range(16)))

    def reset(self):
        self.state = np.zeros((4, 4), dtype=np.int32)
        self._add_tile()
        self._add_tile()
        return self.state

    def step(self, action):
        assert self.action_space.contains(action)
        self._act(action)

        terminated = False
        truncated = False
        reward = 0

        return self.state, reward, terminated, truncated, {}

    def _act(self, action):
        pass

    def _add_tile(self):
        pass

    def render(self):
        pass

    def close(self):
        pass
