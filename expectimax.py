import logic


class ExpectimaxAgent:
    def __init__(self, logic):
        self.logic = logic

    def start_playing(self):
        matrix = self.logic.matrix
        # evaluate
        self.logic.perform_action(logic.Action.LEFT)