from agent import Agent

_DEPTH = 3


class ExpectimaxAgent(Agent):
    def next_action(self):
        legal_actions = self.state.legal_actions()
        if not legal_actions:
            return None

        best_action = self.best(self.state, _DEPTH)[0]
        return best_action

    def best(self, state, depth):
        if not state.legal_actions():
            return None, 0

        def get_score(action) -> int:
            score = 0
            merges = self.state.get_merges(action)
            for k, v in merges.items():
                score += k * v
            score += self.expect(state, action, depth)
            return score

        best_score = 0
        best_action = state.legal_actions()[0]
        for action in state.legal_actions():
            score = get_score(action)
            if score > best_score:
                best_action = action
                best_score = score

        return best_action, best_score

    def expect(self, state, action, depth):
        depth -= 1
        if depth == 0:
            return 0

        successors = state.get_successors(action)

        score = 0
        for successor in successors:
            state = successor[0]
            value = successor[1]

            if value == 2:
                score += self.best(state, depth)[1] * self.state.two_odds
            else:
                score += self.best(state, depth)[1] * (1 - self.state.two_odds)

        return score
