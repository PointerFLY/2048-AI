from montecarlo import MonteCarloAgent
from expectimax import ExpectimaxAgent
from state import State
from functools import lru_cache


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
