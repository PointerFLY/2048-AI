from agent import Agent


class GreedyAgent(Agent):
    def next_action(self):
        legal_actions = self.state.legal_actions()
        if not legal_actions:
            return

        def get_score(action) -> int:
            old = self.state.score
            new = self.state.direct_successor(action).score
            return new - old

        best_action = max(legal_actions, key=get_score)
        return best_action
