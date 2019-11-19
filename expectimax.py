from agent import Agent

_DEPTH = 3


class ExpectimaxAgent(Agent):
    def next_action(self):
        legal_actions = self.state.legal_actions()
        if not legal_actions:
            return None

        best_action = self.best(self.state, _DEPTH)[0]
        return best_action

    def evaluate(self, state):
        return state.score

    def best(self, state, depth):
        if not state.legal_actions():
            return None, 0

        best_eval = 0
        best_action = state.legal_actions()[0]
        for action in state.legal_actions():
            eval_ = self.expect(state, action, depth)
            if eval_ > best_eval:
                best_action = action
                best_eval = eval_

        return best_action, best_eval

    def expect(self, state, action, depth):
        depth -= 1
        if depth == 0:
            return self.evaluate(state.direct_successor(action))

        successors = state.get_successors(action)

        eval_ = 0
        for successor in successors:
            state = successor[0]
            value = successor[1]

            if value == 2:
                eval_ += self.best(state, depth)[1] * self.state.two_odds
            else:
                eval_ += self.best(state, depth)[1] * (1 - self.state.two_odds)

        return eval_
