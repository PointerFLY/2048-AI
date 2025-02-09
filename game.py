import pygame
import sys
from state import State

# Constants
WINDOW_SIZE = 500
PADDING = 7
FONT_SIZE = 40

# Colors
BG_COLOR = "#92877d"

BG_COLOR_DICT = {
    0: "#cdc1b5",
    2: "#eee4da",
    4: "#ede0c8",
    8: "#f2b179",
    16: "#f59563",
    32: "#f67c5f",
    64: "#f65e3b",
    128: "#edcf72",
    256: "#edcc61",
    512: "#edc850",
    1024: "#edc53f",
    2048: "#edc22e",
    4096: "#eee4da",
    8192: "#edc22e",
    16384: "#f2b179",
    32768: "#f59563",
    65536: "#f67c5f",
}

FG_COLOR_DICT = {
    0: "#cdc1b5",
    2: "#776e65",
    4: "#776e65",
    8: "#f9f6f2",
    16: "#f9f6f2",
    32: "#f9f6f2",
    64: "#f9f6f2",
    128: "#f9f6f2",
    256: "#f9f6f2",
    512: "#f9f6f2",
    1024: "#f9f6f2",
    2048: "#f9f6f2",
    4096: "#776e65",
    8192: "#f9f6f2",
    16384: "#776e65",
    32768: "#776e65",
    65536: "#f9f6f2",
}

FPS = 60


def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("2048")

        self.state = State()
        self.window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        self.clock = pygame.time.Clock()

        # Initialize font
        self.font = pygame.font.SysFont("Arial", FONT_SIZE, bold=True)

        # Calculate cell size
        self.cell_size = (
            WINDOW_SIZE - (self.state.row_count + 1) * PADDING
        ) // self.state.row_count

    def show(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

            if self.state.ui_dirty:
                self.state.ui_dirty = False
                self._update_display()

            self.clock.tick(FPS)

    def _update_display(self):
        # Fill background
        self.window.fill(hex_to_rgb(BG_COLOR))

        # Update window title with score
        pygame.display.set_caption(f"2048 - Score: {self.state.score}")

        # Draw cells
        for i in range(self.state.row_count):
            for j in range(self.state.row_count):
                number = self.state.matrix[i][j]

                # Calculate cell position
                x = PADDING * (j + 1) + self.cell_size * j
                y = PADDING * (i + 1) + self.cell_size * i

                # Draw cell background
                cell_rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                pygame.draw.rect(
                    self.window, hex_to_rgb(BG_COLOR_DICT[number]), cell_rect
                )

                # Draw number
                if number != 0:
                    text = self.font.render(
                        str(number), True, hex_to_rgb(FG_COLOR_DICT[number])
                    )
                    text_rect = text.get_rect(
                        center=(x + self.cell_size // 2, y + self.cell_size // 2)
                    )
                    self.window.blit(text, text_rect)

        pygame.display.flip()
