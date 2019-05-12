from game import Game
from threading import Thread
import time


class Agent:
    def __init__(self, game: Game):
        self.game = game
        self.state = game.state
        self.show_ui = True

    def start(self):
        thread = Thread(target=self._time_process)
        thread.start()

    def _time_process(self):
        start = time.time()
        self.process()
        end = time.time()
        print('Execution time: {} s'.format(end - start))

    def process(self):
        action = self.next_action()
        if not action:
            return

        if self.show_ui:
            self.game.call_on_main(lambda: self.state.perform_action(action))
            time.sleep(self.game.ui_interval / 1000)

        self.process()

    def next_action(self):
        raise NotImplementedError()
