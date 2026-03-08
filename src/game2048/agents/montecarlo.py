import multiprocessing as mp
from functools import lru_cache
from random import randrange
from time import time

import numpy as np

from game2048.agents.agent import Agent
from game2048.agents.expectimax import ExpectimaxAgent

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


class SmartMonteCarloAgent(MonteCarloAgent):
    def __init__(self, state):
        super().__init__(state)
        self.expectimax = ExpectimaxAgent(state)

    @staticmethod
    @lru_cache(maxsize=10000)
    def _simulate(state) -> float:
        """Override simulation to use Expectimax evaluation instead of score"""
        legal_actions = state.legal_actions()
        count = 0
        # Run simulation until no moves left or max depth reached
        while legal_actions and count < 20:  # Limit depth to avoid too deep simulations
            idx = randrange(len(legal_actions))
            state.perform_action(legal_actions[idx])
            legal_actions = state.legal_actions()
            count += 1

        # Use Expectimax evaluation function instead of score
        eval_value = ExpectimaxAgent.evaluate(ExpectimaxAgent(state), state)
        return eval_value

    def __del__(self):
        super().__del__()


class HybridAgent(Agent):
    def __init__(self, state):
        super().__init__(state)
        self.monte_carlo = MonteCarloAgent(state)
        self.expectimax = ExpectimaxAgent(state)

    def next_action(self):
        legal_actions = self.state.legal_actions()
        if not legal_actions:
            return None

        # Update state for both agents
        self.monte_carlo.state = self.state
        self.expectimax.state = self.state

        # Use Expectimax for early/mid game, Monte Carlo for late game
        if self._should_use_montecarlo():
            return self.monte_carlo.next_action()
        return self.expectimax.next_action()

    def _should_use_montecarlo(self):
        """
        Determine whether to use Monte Carlo based on:
        1. Number of empty cells (less empty cells = more complex)
        2. Maximum tile value (higher values = more complex)
        """
        empty_count = sum(1 for row in self.state.matrix for cell in row if cell == 0)
        max_value = max(max(row) for row in self.state.matrix)

        # Switch to Monte Carlo when:
        # - Less than 6 empty cells, or
        # - Maximum tile value is 512 or greater
        return empty_count < 6 or max_value >= 512

    def __del__(self):
        # Clean up Monte Carlo resources
        if hasattr(self, "monte_carlo"):
            self.monte_carlo.__del__()
