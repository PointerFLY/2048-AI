import tkinter as tk
from tkinter import messagebox
from state import State
import queue as q

_VIEW_WIDTH = 500
_PADDING = 7
_FONT = ('Verdana', 40, 'bold')

_BG_COLOR = '#92877d'

_BG_COLOR_DICT = {
    0: '#cdc1b5', 2: '#eee4da', 4: '#ede0c8', 8: '#f2b179', 16: '#f59563', 32: '#f67c5f', 64: '#f65e3b', 128: '#edcf72',
    256: '#edcc61', 512: '#edc850', 1024: '#edc53f', 2048: '#edc22e', 4096: '#eee4da', 8192: '#edc22e',
    16384: '#f2b179', 32768: '#f59563', 65536: '#f67c5f'
}

_FG_COLOR_DICT = {
    0: '#cdc1b5', 2: '#776e65', 4: '#776e65', 8: '#f9f6f2', 16: '#f9f6f2', 32: '#f9f6f2', 64: '#f9f6f2', 128: '#f9f6f2',
    256: '#f9f6f2', 512: '#f9f6f2', 1024: '#f9f6f2', 2048: '#f9f6f2', 4096: '#776e65', 8192: '#f9f6f2',
    16384: '#776e65', 32768: '#776e65', 65536: '#f9f6f2'
}

_UI_INTERVAL = 16


class Game(tk.Tk):
    def __init__(self):
        super(Game, self).__init__()
        self.state = State()

        self.title('2048')

        x = (self.winfo_screenwidth() - _VIEW_WIDTH) / 2
        y = (self.winfo_screenheight() - _VIEW_WIDTH) / 2
        self.geometry('%dx%d+%d+%d' % (_VIEW_WIDTH, _VIEW_WIDTH, x, y))

        self.labels = []
        self._setup_cells()
        self._update_cells()

    def show(self):
        self.after(_UI_INTERVAL, self.periodic_call)
        self.mainloop()

    def periodic_call(self):
        self._update_cells()
        self.after(_UI_INTERVAL, self.periodic_call)

    def _setup_cells(self):
        background = tk.Frame(self, bg=_BG_COLOR, padx=_PADDING, pady=_PADDING)
        background.place(relwidth=1, relheight=1)

        for i in range(self.state.row_count):
            tk.Grid.columnconfigure(background, i, weight=1)
            tk.Grid.rowconfigure(background, i, weight=1)

            row = []
            for j in range(self.state.row_count):
                cell = tk.Frame(background)
                cell.grid(row=i, column=j, padx=_PADDING, pady=_PADDING, sticky=tk.NSEW)

                label = tk.Label(cell, font=_FONT)
                label.place(relwidth=1, relheight=1)
                row.append(label)

            self.labels.append(row)

    def _update_cells(self):
        for i in range(self.state.row_count):
            for j in range(self.state.row_count):
                number = self.state.matrix[i][j]
                self.labels[i][j].configure(text=str(number), bg=_BG_COLOR_DICT[number], fg=_FG_COLOR_DICT[number])