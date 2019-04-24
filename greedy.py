from agent import Agent


class GreedyAgent(Agent):
    def next_action(self):
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
        return best_action
