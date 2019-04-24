from agent import Agent
from game import Game
from state import Action


class HumanAgent(Agent):
    def __init__(self, game: Game):
        self.game = game
        self.state = game.state

    def start(self):
        self.game.bind('<Key>', self._key_down)

    def _key_down(self, event):
        dic = {
            'Left': Action.LEFT,
            'Right': Action.RIGHT,
            'Up': Action.UP,
            'Down': Action.DOWN,
        }

        try:
            action = dic[event.keysym]
            self.state.perform_action(action)
        except KeyError:
            pass
