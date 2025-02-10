from agent import Agent
from montecarlo import MonteCarloAgent
from expectimax import ExpectimaxAgent


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
