from agent import Agent
from state import State, Action
from random import randrange

_SAMPLE_PER_ACTION = 100


class MonteCarloAgent(Agent):
    def next_action(self):
        legal_actions = self.state.legal_actions()
        if not legal_actions:
            return None

        best_action = max(legal_actions, key=self.sample)
        return best_action

    def sample(self, action) -> float:
        total_score = 0
        for i in range(_SAMPLE_PER_ACTION):
            state = self.state.copy()
            state.perform_action(action)
            legal_actions = state.legal_actions()
            while legal_actions:
                idx = randrange(len(legal_actions))
                act = legal_actions[idx]
                state.perform_action(act)
                legal_actions = state.legal_actions()

            total_score += state.score

        score = total_score / _SAMPLE_PER_ACTION
        return score

