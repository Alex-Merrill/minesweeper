# minesweeper game using python
import random
import tkinter as tk
import tkinter.font as tkFont
import time

# Defines Game class
class Game:
    def __init__(self, rows, cols, mines, grid_frame, top_frame):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.grid_frame = grid_frame
        self.top_frame = top_frame
        self.board = [[0 for i in range(cols)] for j in range(rows)]
        self.checked_spots = [
            [False for i in range(cols)] for j in range(rows)]
        self.flagged_spots = [
            [False for i in range(cols)] for j in range(rows)]
        self.btn_board = [[None for i in range(cols)] for j in range(rows)]
        self.game_over = False
        self.game_won = False
        self.start_time = time.time()
        self.generate_mines()
        self.generate_numbers()

        # creates button grid
        for i in range(0, self.rows):
            for j in range(0, self.cols):
                btn = tk.Button(self.grid_frame,
                                text='',
                                width=5,
                                height=2,
                                bg='grey')
                btn.grid(row=i, column=j)
                btn.bind("<Button-1>", lambda q, i=i, j=j: self.check_spot_render(i, j))
                btn.bind("<Button-3>", lambda q, i=i, j=j: self.flag_spot(i, j))
                self.btn_board[i][j] = btn

    # generates mines
    def generate_mines(self):
        for i in range(self.mines):
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            while self.board[row][col] == "*":
                row = random.randint(0, self.rows - 1)
                col = random.randint(0, self.cols - 1)
            self.board[row][col] = "*"

    # generates numbers for each tile
    def generate_numbers(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != "*":
                    self.board[i][j] = self.get_number_for_tile(i, j)

    # returns number of mines around tile
    def get_number_for_tile(self, row, col):
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            return 0
        if self.board[row][col] == "*":
            return "*"
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i == 0 and j == 0) or (row + i < 0 or row + i >= self.rows) or (col + j < 0 or col + j >= self.cols):
                    continue
                if self.board[row + i][col + j] == "*":
                    count += 1
        return count

    # select tile and render after completetion
    def check_spot_render(self, row, col):
        if self.game_over:
            return
        # spot is mine, game over
        if self.board[row][col] == "*":
            self.game_over = True
            self.render()
            return

        if self.checked_spots[row][col]:
            return

        # marks tile as checked
        self.checked_spots[row][col] = True
        if self.board[row][col] == 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if (i == 0 and j == 0) or (row + i < 0 or row + i >= self.rows) or (col + j < 0 or col + j >= self.cols):
                        continue
                    self.check_spot_recursive(row + i, col + j)

       # render new board
        self.render()

    # recursive check_spot for cascading tile deletion, no need to render
    def check_spot_recursive(self, row, col):
        if self.checked_spots[row][col]:
            return

        # marks tile as checked
        self.checked_spots[row][col] = True
        if self.board[row][col] == 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if (i == 0 and j == 0) or (row + i < 0 or row + i >= self.rows) or (col + j < 0 or col + j >= self.cols):
                        continue
                    self.check_spot_recursive(row + i, col + j)

    # flags a tile, or unflags a tile
    # renders after flagging/unflagging
    def flag_spot(self, row, col):
        if self.flagged_spots[row][col]:
            self.flagged_spots[row][col] = False
        else:
            self.flagged_spots[row][col] = True

        # renders board
        self.render()

    # returns true if win, false if not
    # sets proper game state in object
    def check_win(self):
        win = True
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] == "*" and self.checked_spots[i][j]:
                    self.game_over = True
                elif self.board[i][j] != "*" and not self.checked_spots[i][j]:
                    win = False

        if win:
            self.game_over = True
            self.game_won = True

    # render method called after player selects a tile
    def render(self):
        # checks win
        self.check_win()

        if self.game_over:
            if self.game_won:
                tk.Label(self.top_frame, text="You won!").pack()
                tk.Label(self.top_frame, text=f"Time: {int(time.time() - self.start_time)}").pack()
            else:
                label = tk.Label(self.top_frame, text="Game Over").pack()
                tk.Label(self.top_frame, text=f"Time: {int(time.time() - self.start_time)}s").pack()

        # draw grid
        for i in range(0, self.rows):
            for j in range(0, self.cols):
                textToDisplay = ""
                colorToDisplay = ""

                if self.game_over:
                    textToDisplay = "" if self.board[i][j] == 0 else "💣" if self.board[i][j] == "*" else self.board[i][j]
                    colorToDisplay = "red" if self.board[i][j] == "*" else "grey"
                    fgColorToDisplay = "black"
                else:
                    if self.checked_spots[i][j]:
                        textToDisplay = "" if self.board[i][j] == 0 else self.board[i][j]
                        colorToDisplay = "grey"
                        fgColorToDisplay = "black"
                    elif not self.flagged_spots[i][j]:
                        textToDisplay = ""
                        colorToDisplay = "white"
                        fgColorToDisplay = "black"
                    elif self.flagged_spots[i][j]:
                        textToDisplay = "🚩"
                        colorToDisplay = "white"
                        fgColorToDisplay = "red"
                self.btn_board[i][j].config(text=textToDisplay, bg=colorToDisplay, fg=fgColorToDisplay, font = tkFont.Font(size = 15))

    ########### TESTING METHODS ##############

    # prints board to console
    def print_board(self):
        for i in range(self.rows):
            for j in range(self.cols):
                print(self.board[i][j], end=" ")
            print()
        print()
    
    # prints checked spots to console
    def print_checked_spots(self):
        for i in range(self.rows):
            for j in range(self.cols):
                print(self.checked_spots[i][j], end=" ")
            print()
        print()

    # prints flagged spots to console
    def print_flagged_spots(self):
        for i in range(self.rows):
            for j in range(self.cols):
                print(self.flagged_spots[i][j], end=" ")
            print()
        print()


## UI and Main method

# sets up some ui stuff
window = tk.Tk()
window.title("Minesweeper")

top_frame = tk.Frame(window)
grid_frame = tk.Frame(window)
bottom_frame = tk.Frame(window)

def main(difficulty):
    # clear top frame
    for widget in top_frame.winfo_children():
        widget.destroy()

    # clear grid frame
    for widget in grid_frame.winfo_children():
        widget.destroy()

    # set difficulties
    if difficulty == "easy":
        rows = 9
        columns = 9
        mines = 10
    elif difficulty == "medium":
        rows = 16
        columns = 16
        mines = 40
    elif difficulty == "hard":
        rows = 16
        columns = 30
        mines = 99

    # create game
    game = Game(rows, columns, mines, grid_frame, top_frame)

    # render game
    game.render()


# finishes ui setup
diff1 = tk.Button(bottom_frame, text="Easy", bg="red",
                  command=lambda: main('easy')).pack()
diff2 = tk.Button(bottom_frame, text="Medium", bg="red",
                  command=lambda: main('medium')).pack()
diff3 = tk.Button(bottom_frame, text="Hard", bg="red",
                  command=lambda: main('hard')).pack()
instructions = tk.Label(bottom_frame, text="Instructions: \nLeft click to reveal a tile. \nRight click to flag a tile. \nYou win when all non-mine tiles are cleared. \nYou lose when you click on a mine. \nGood luck!").pack()
top_frame.pack(side="top")
grid_frame.pack()
bottom_frame.pack(side="bottom")


window.mainloop()


