from agent import Agent
from state import State


class ExpectimaxAgent(Agent):
    def __init__(self, state: State):
        self.state = state

    def start(self):
        pass