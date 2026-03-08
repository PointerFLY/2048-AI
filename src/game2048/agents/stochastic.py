from random import randrange

from game2048.agents.agent import Agent


class StochasticAgent(Agent):
    def next_action(self):
        legal_actions = self.state.legal_actions()
        if not legal_actions:
            return None

        idx = randrange(len(legal_actions))
        action = legal_actions[idx]
        return action
