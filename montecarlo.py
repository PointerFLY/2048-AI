from agent import Agent
from state import State, Action
from random import randrange
import multiprocessing as mp
from time import time
from functools import lru_cache
import numpy as np

_TIME_LIMIT = 0.25  # seconds
_CONFIDENCE_THRESHOLD = 0.95


class MonteCarloAgent(Agent):
    def __init__(self, state):
        super().__init__(state)
        self.pool = mp.Pool(processes=mp.cpu_count())

    def next_action(self):
        legal_actions = self.state.legal_actions()
        if not legal_actions:
            return None

        start_time = time()
        action_scores = {action: [] for action in legal_actions}

        while time() - start_time < _TIME_LIMIT:
            samples = [(self.state.copy(), action) for action in legal_actions]
            results = self.pool.starmap(self._sample_single, samples)

            for action, score in zip(legal_actions, results):
                action_scores[action].append(score)

            # Early termination if we have a clear winner
            if (
                len(action_scores[legal_actions[0]]) > 30
            ):  # Minimum samples before checking
                scores = [np.mean(scores) for scores in action_scores.values()]
                max_score = max(scores)
                confidence = sum(1 for s in scores if max_score - s > max_score * 0.1)
                if confidence / len(scores) >= _CONFIDENCE_THRESHOLD:
                    break

        return max(legal_actions, key=lambda a: np.mean(action_scores[a]))

    @staticmethod
    def _sample_single(state, action) -> float:
        state.perform_action(action)
        return MonteCarloAgent._simulate(state)

    @staticmethod
    @lru_cache(maxsize=10000)
    def _simulate(state) -> float:
        legal_actions = state.legal_actions()
        while legal_actions:
            idx = randrange(len(legal_actions))
            state.perform_action(legal_actions[idx])
            legal_actions = state.legal_actions()
        return state.score

    def __del__(self):
        self.pool.close()
        self.pool.join()
