from game import Game
from threading import Thread
import time
import numpy as np


class Agent:
    def __init__(self, game: Game):
        self.game = game
        self.state = game.state

    def start(self):
        thread = Thread(target=self._time_process)
        thread.start()

    def setup(self):
        pass

    def _time_process(self):
        self.setup()

        start = time.time()
        self.process()
        end = time.time()
        print('Execution time: {} s'.format(end - start))
        print('Final state:')
        print(np.array(self.state.matrix))

    def process(self):
        action = self.next_action()
        if not action:
            return

        self.state.perform_action(action)

        self.process()

    def next_action(self):
        raise NotImplementedError()
