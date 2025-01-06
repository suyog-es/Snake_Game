import tkinter as tk
import random
import time

# Constants for game settings
GRID_SIZE = 20
CELL_SIZE = 20
WINDOW_SIZE = GRID_SIZE * CELL_SIZE
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF4500"
BG_COLOR = "#1E1E1E"

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=WINDOW_SIZE, height=WINDOW_SIZE, bg=BG_COLOR)
        self.canvas.pack()

        self.reset_button = tk.Button(root, text="Restart", command=self.reset_game, bg="white")
        self.reset_button.pack()

        self.score_label = tk.Label(root, text="Score: 0", bg=BG_COLOR, fg="white", font=("Arial", 14))
        self.score_label.pack()

        self.snake = [(5, 5), (4, 5), (3, 5)]  # Initial snake coordinates
        self.food = None
        self.direction = "Right"
        self.score = 0
        self.speed = 100
        self.running = True

        self.place_food()
        self.root.bind("<KeyPress>", self.change_direction)
        self.update_game()

    def place_food(self):
        while True:
            food_x = random.randint(0, GRID_SIZE - 1)
            food_y = random.randint(0, GRID_SIZE - 1)
            if (food_x, food_y) not in self.snake:
                self.food = (food_x, food_y)
                break

    def draw_grid(self):
        self.canvas.delete("all")

        # Draw food
        food_x, food_y = self.food
        self.canvas.create_rectangle(
            food_x * CELL_SIZE,
            food_y * CELL_SIZE,
            (food_x + 1) * CELL_SIZE,
            (food_y + 1) * CELL_SIZE,
            fill=FOOD_COLOR,
            outline=""
        )

        # Draw snake
        for x, y in self.snake:
            self.canvas.create_rectangle(
                x * CELL_SIZE,
                y * CELL_SIZE,
                (x + 1) * CELL_SIZE,
                (y + 1) * CELL_SIZE,
                fill=SNAKE_COLOR,
                outline=""
            )

    def change_direction(self, event):
        new_direction = event.keysym
        all_directions = {"Left", "Right", "Up", "Down"}
        opposites = {"Left": "Right", "Right": "Left", "Up": "Down", "Down": "Up"}

        if new_direction in all_directions and new_direction != opposites.get(self.direction):
            self.direction = new_direction

    def move_snake(self):
        head_x, head_y = self.snake[0]
        if self.direction == "Left":
            head_x -= 1
        elif self.direction == "Right":
            head_x += 1
        elif self.direction == "Up":
            head_y -= 1
        elif self.direction == "Down":
            head_y += 1

        # Check for collisions
        if (
            head_x < 0 or head_x >= GRID_SIZE or
            head_y < 0 or head_y >= GRID_SIZE or
            (head_x, head_y) in self.snake
        ):
            self.game_over()
            return

        # Move snake
        self.snake.insert(0, (head_x, head_y))

        # Check for food
        if (head_x, head_y) == self.food:
            self.score += 1
            self.speed = max(50, self.speed - 2)  # Increase difficulty
            self.score_label.config(text=f"Score: {self.score}")
            self.place_food()
        else:
            self.snake.pop()

    def game_over(self):
        self.running = False
        self.canvas.create_text(
            WINDOW_SIZE // 2,
            WINDOW_SIZE // 2,
            text="Game Over",
            fill="red",
            font=("Arial", 24)
        )

    def reset_game(self):
        self.snake = [(5, 5), (4, 5), (3, 5)]
        self.food = None
        self.direction = "Right"
        self.score = 0
        self.speed = 100
        self.running = True
        self.score_label.config(text="Score: 0")
        self.place_food()
        self.update_game()

    def update_game(self):
        if self.running:
            self.move_snake()
            self.draw_grid()
            self.root.after(self.speed, self.update_game)

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()