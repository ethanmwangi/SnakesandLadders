import tkinter as tk
import random

# Define ladders and snakes
ladders = {3: 22, 5: 8, 11: 26, 20: 29, 27: 84, 21: 82, 43: 77, 50: 91, 57: 76}
snakes = {17: 4, 19: 7, 21: 9, 62: 18, 54: 34, 64: 60, 87: 24, 93: 73, 95: 75, 98: 79}

class SnakesAndLadders:
    def __init__(self, root):
        self.root = root
        self.root.title("Snakes and Ladders")

        self.canvas = tk.Canvas(root, width=600, height=600)
        self.canvas.grid(row=0, column=0, columnspan=4)

        self.board_size = 10
        self.tile_size = 60
        self.draw_board()

        self.positions = [0, 0]
        self.turn = 0  # 0 for Player 1, 1 for Player 2

        self.dice_label = tk.Label(root, text="Roll the dice!", font=("Arial", 16))
        self.dice_label.grid(row=1, column=0, columnspan=2)

        self.roll_button = tk.Button(root, text="Roll Dice", command=self.roll_dice)
        self.roll_button.grid(row=1, column=2)

        self.reset_button = tk.Button(root, text="Reset", command=self.reset_game)
        self.reset_button.grid(row=1, column=3)

        self.tokens = [None, None]
        self.create_tokens()

    def draw_board(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                x1 = j * self.tile_size
                y1 = (9 - i) * self.tile_size
                x2 = x1 + self.tile_size
                y2 = y1 + self.tile_size

                number = i * 10 + j + 1 if i % 2 == 0 else i * 10 + (9 - j) + 1
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="white")
                self.canvas.create_text(x1 + 30, y1 + 30, text=str(number), font=("Arial", 10))

    def create_tokens(self):
        # Player 1: Red, Player 2: Blue
        self.tokens[0] = self.canvas.create_oval(5, 565, 25, 585, fill="red")
        self.tokens[1] = self.canvas.create_oval(35, 565, 55, 585, fill="blue")

    def get_coordinates(self, position):
        if position == 0:
            return (5, 565)
        row = (position - 1) // 10
        col = (position - 1) % 10
        if row % 2 == 1:
            col = 9 - col
        x = col * self.tile_size + 5 + (30 * self.turn)
        y = (9 - row) * self.tile_size + 5
        return x, y

    def roll_dice(self):
        roll = random.randint(1, 6)
        current_player = self.turn + 1
        self.dice_label.config(text=f"Player {current_player} rolled a {roll}!")

        new_pos = self.positions[self.turn] + roll
        if new_pos > 100:
            self.dice_label.config(text=f"Player {current_player} rolled too high!")
        else:
            if new_pos in ladders:
                new_pos = ladders[new_pos]
                self.dice_label.config(text=f"Player {current_player} climbed a ladder to {new_pos}!")
            elif new_pos in snakes:
                new_pos = snakes[new_pos]
                self.dice_label.config(text=f"Player {current_player} got bitten by a snake to {new_pos}!")

            self.positions[self.turn] = new_pos
            x, y = self.get_coordinates(new_pos)
            self.canvas.coords(self.tokens[self.turn], x, y, x + 20, y + 20)

            if new_pos == 100:
                self.dice_label.config(text=f"🎉 Player {current_player} Wins!")
                self.roll_button.config(state="disabled")
                return

        # Switch turns
        self.turn = 1 - self.turn

    def reset_game(self):
        self.positions = [0, 0]
        self.turn = 0
        self.dice_label.config(text="Game reset! Roll the dice.")
        self.roll_button.config(state="normal")
        self.canvas.coords(self.tokens[0], 5, 565, 25, 585)
        self.canvas.coords(self.tokens[1], 35, 565, 55, 585)

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = SnakesAndLadders(root)
    root.mainloop()
