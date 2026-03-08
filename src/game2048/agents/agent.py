import logging
import time
from threading import Thread

import numpy as np

from game2048.core.game import Game

logger = logging.getLogger(__name__)


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
        logger.info(f"Execution time: {end - start:.4f} s")
        logger.info(f"Final state:\n{np.array(self.state.matrix)}")

    def process(self):
        action = self.next_action()
        if not action:
            return

        self.state.perform_action(action)

        self.process()

    def next_action(self):
        raise NotImplementedError()
