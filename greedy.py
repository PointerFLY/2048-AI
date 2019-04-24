from agent import Agent
from state import State


class GreedyAgent(Agent):
    def __init__(self, state: State):
        self.state = state

    def start(self):
        legal_actions = self.state.legal_actions()
        if not legal_actions:
            return

        def get_score(action) -> int:
            score = 0
            merges = self.state.get_merges(action)
            for k, v in merges.items():
                score += k * v

            return score

        best_action = max(legal_actions, key=get_score)
        self.state.perform_action(best_action)

        self.start()