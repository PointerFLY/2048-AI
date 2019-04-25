from agent import Agent

_DEPTH = 4


class ExpectimaxAgent(Agent):
    def next_action(self):
        legal_actions = self.state.legal_actions()
        if not legal_actions:
            return None

        best_action = max(legal_actions, key=lambda x: self.depth_limit_search(x, _DEPTH - 1))
        return best_action

    def depth_limit_search(self, action, depth) -> float:
        score = 0
        merges = self.state.get_merges(action)
        for k, v in merges.items():
            score += k * v

        depth -= 1
        if depth == 0:
            return score

        successors = self.state.get_successors(action)
        for successor in successors:
            state = successor[0]
            value = successor[1]

            if value == 2:
                for action in state.legal_actions():
                    increment = self.depth_limit_search(action, depth)
                    if value == 2:
                        increment *= self.state.two_odds * 2.0 / len(successors)
                    else:
                        increment *= (1 - self.state.two_odds) * 2.0 / len(successors)
                    score += increment
        return score
