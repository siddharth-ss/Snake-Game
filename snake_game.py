"""A small, dependency-free Snake game built with Tkinter."""

from __future__ import annotations

import random
import tkinter as tk


CELL_SIZE = 24
COLUMNS = 24
ROWS = 20
WIDTH = CELL_SIZE * COLUMNS
HEIGHT = CELL_SIZE * ROWS
START_SPEED = 130
MIN_SPEED = 55
MAX_SPEED = 220

BACKGROUND = "#101820"
GRID = "#1c2a35"
SNAKE = "#59d98e"
HEAD = "#b8ffcf"
FOOD = "#ff5c77"
TEXT = "#f3f7fa"


class SnakeGame:
    """Manage game state, input, and drawing."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Snake")
        self.root.resizable(False, False)
        self.score_label = tk.Label(
            root, text="Score: 0", font=("Arial", 14, "bold"),
            bg=BACKGROUND, fg=TEXT, pady=10
        )
        self.score_label.pack(fill="x")
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BACKGROUND,
                                highlightthickness=0)
        self.canvas.pack()
        self.help_label = tk.Label(
            root, text="Arrow keys / WASD to move   •   R to restart",
            font=("Arial", 10), bg=BACKGROUND, fg="#aebbc5", pady=10
        )
        self.help_label.pack(fill="x")

        root.configure(bg=BACKGROUND)
        root.bind("<KeyPress>", self.handle_key)
        self.job: str | None = None
        self.reset()

    def reset(self) -> None:
        if self.job:
            self.root.after_cancel(self.job)
        center = (COLUMNS // 2, ROWS // 2)
        self.snake = [center, (center[0] - 1, center[1]), (center[0] - 2, center[1])]
        self.direction = (1, 0)
        self.next_direction = self.direction
        self.score = 0
        self.speed = START_SPEED
        self.running = True
        self.food = self.new_food()
        self.draw()
        self.job = self.root.after(self.speed, self.tick)

    def new_food(self) -> tuple[int, int]:
        available = [
            (x, y) for x in range(COLUMNS) for y in range(ROWS)
            if (x, y) not in self.snake
        ]
        return random.choice(available)

    def handle_key(self, event: tk.Event) -> None:
        key = event.keysym.lower()
        directions = {
            "up": (0, -1), "w": (0, -1),
            "down": (0, 1), "s": (0, 1),
            "left": (-1, 0), "a": (-1, 0),
            "right": (1, 0), "d": (1, 0),
        }
        if key == "r":
            self.reset()
            return
        if key not in directions or not self.running:
            return
        candidate = directions[key]
        # A snake cannot immediately turn back into itself.
        if candidate != (-self.direction[0], -self.direction[1]):
            self.next_direction = candidate

    def tick(self) -> None:
        if not self.running:
            return
        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        ate_food = new_head == self.food
        body_to_check = self.snake if ate_food else self.snake[:-1]

        if (
            new_head[0] < 0 or new_head[0] >= COLUMNS
            or new_head[1] < 0 or new_head[1] >= ROWS
            or new_head in body_to_check
        ):
            self.running = False
            self.draw()
            return

        self.snake.insert(0, new_head)
        if ate_food:
            self.score += 1
            if len(self.snake) == COLUMNS * ROWS:
                self.running = False
            else:
                self.food = self.new_food()
        else:
            self.snake.pop()

        self.draw()
        if self.running:
            # Make each move unpredictable: the next move can be quick or slow.
            self.speed = random.randint(MIN_SPEED, MAX_SPEED)
            self.job = self.root.after(self.speed, self.tick)

    def draw(self) -> None:
        self.canvas.delete("all")
        self.score_label.config(text=f"Score: {self.score}")
        for x in range(COLUMNS):
            self.canvas.create_line(x * CELL_SIZE, 0, x * CELL_SIZE, HEIGHT, fill=GRID)
        for y in range(ROWS):
            self.canvas.create_line(0, y * CELL_SIZE, WIDTH, y * CELL_SIZE, fill=GRID)

        self.draw_cell(self.food, FOOD, pad=4)
        for index, segment in enumerate(self.snake):
            self.draw_cell(segment, HEAD if index == 0 else SNAKE, pad=2)

        if not self.running:
            message = "You win!" if len(self.snake) == COLUMNS * ROWS else "Game over"
            self.canvas.create_rectangle(70, HEIGHT // 2 - 55, WIDTH - 70, HEIGHT // 2 + 55,
                                         fill="#13232d", outline="#466170", width=2)
            self.canvas.create_text(WIDTH // 2, HEIGHT // 2 - 12, text=message,
                                    fill=TEXT, font=("Arial", 24, "bold"))
            self.canvas.create_text(WIDTH // 2, HEIGHT // 2 + 22, text="Press R to play again",
                                    fill="#b9c7d0", font=("Arial", 12))

    def draw_cell(self, position: tuple[int, int], color: str, pad: int) -> None:
        x, y = position
        left = x * CELL_SIZE + pad
        top = y * CELL_SIZE + pad
        self.canvas.create_rectangle(left, top, left + CELL_SIZE - 2 * pad,
                                     top + CELL_SIZE - 2 * pad, fill=color, outline="")


if __name__ == "__main__":
    window = tk.Tk()
    SnakeGame(window)
    window.mainloop()
