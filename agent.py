from game import Game
from threading import Thread
import time

_UPDATE_INTERVAL = 0.1


class Agent:
    def __init__(self, game: Game):
        self.game = game
        self.state = game.state

    def start(self):
        thread = Thread(target=self.process)
        thread.start()

    def process(self):
        action = self.next_action()
        if not action:
            return
        self.state.perform_action(action)

        time.sleep(_UPDATE_INTERVAL)
        self.game.update()

        self.process()

    def next_action(self):
        raise NotImplementedError()
