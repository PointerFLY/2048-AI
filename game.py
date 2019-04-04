import tkinter as tk
import logic


class GameUI(tk.Frame):
    def __init__(self):
        super(GameUI, self).__init__()
        self.grid()
        self.master.title('2048')
        self.master.bind('<Key>', self._key_event)
        self._create_grid()

        self.logic = logic.Logic()
        self.logic.matrix_updated = self._matrix_update

    def show(self):
        self.mainloop()

    def _create_grid(self):
        background = tk.Frame(self)
        background.grid()

    def _key_event(self, event):
        self.logic.perform_action(logic.Action.LEFT)

    def _matrix_update(self):
        pass # update UI
