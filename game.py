import tkinter as tk

import logic

VIEW_SIZE = 400
PADDING = 10

BG_COLOR = "#92877d"

BG_COLOR_DICT = {
    0: "#9e948a", 2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563", 32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72",
    256: "#edcc61", 512: "#edc850", 1024: "#edc53f", 2048: "#edc22e", 4096: "#eee4da", 8192: "#edc22e",
    16384: "#f2b179", 32768: "#f59563", 65536: "#f67c5f"
}

FG_COLOR_DICT = {
    0: "#9e948a", 2: "#776e65", 4: "#776e65", 8: "#f9f6f2", 16: "#f9f6f2", 32: "#f9f6f2", 64: "#f9f6f2", 128: "#f9f6f2",
    256: "#f9f6f2", 512: "#f9f6f2", 1024: "#f9f6f2", 2048: "#f9f6f2", 4096: "#776e65", 8192: "#f9f6f2",
    16384: "#776e65", 32768: "#776e65", 65536: "#f9f6f2"
}


class GameUI(tk.Frame):
    def __init__(self):
        super(GameUI, self).__init__()
        self.logic = logic.Logic()
        self.logic.matrix_updated = lambda x: self._update_cells()

        self.grid()
        self.master.title('2048')
        self.master.bind('<Key>', self._key_down)

        self.labels = []
        self._setup_cells()
        self._update_cells()

    def show(self):
        self.mainloop()

    def _setup_cells(self):
        background = tk.Frame(self, bg=BG_COLOR, width=VIEW_SIZE, height=VIEW_SIZE)
        background.grid()

        for i in range(self.logic.row_count):
            row = []
            for j in range(self.logic.row_count):
                cell = tk.Frame(background, width=VIEW_SIZE / self.logic.row_count, height=VIEW_SIZE / self.logic.row_count)
                cell.grid(row=i, column=j, padx=PADDING, pady=PADDING)

                label = tk.Label(cell, justify=tk.CENTER, width=5, height=5)
                label.grid()
                row.append(label)

            self.labels.append(row)

    def _update_cells(self):
        for i in range(self.logic.row_count):
            for j in range(self.logic.row_count):
                number = self.logic.matrix[i][j]
                self.labels[i][j].configure(text=str(number), bg=BG_COLOR_DICT[number], fg=FG_COLOR_DICT[number])

        self.update_idletasks()

    def _key_down(self, event):
        dic = {
            'Up': logic.Action.UP,
            'Down': logic.Action.DOWN,
            'Left': logic.Action.UP,
            'Right': logic.Action.DOWN
        }

        action = dic.get(event.keysym)
        if action:
            self.logic.perform_action(action)

