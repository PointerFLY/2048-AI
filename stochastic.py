from agent import Agent
from state import State
from random import randrange


class StochasticAgent(Agent):
    def __init__(self, state: State):
        self.state = state

    def start(self):
        legal_actions = self.state.legal_actions()
        if not legal_actions:
            return

        idx = randrange(len(legal_actions))
        action = legal_actions[idx]
        self.state.perform_action(action)

        self.start()