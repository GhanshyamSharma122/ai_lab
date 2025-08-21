from tkinter import *
from tkinter import messagebox
import random

Player1 = 'X'
stop_game = False
ai_mode = "Dumb"  

def clicked(r, c):
    global Player1, stop_game

    if Player1 == "X" and states[r][c] == 0 and not stop_game:
        b[r][c].configure(text="X")
        states[r][c] = 'X'
        Player1 = 'O'
        check_if_win()

        if not stop_game:
            ai_move()

def ai_move():
    global Player1, stop_game

    if stop_game:
        return

    if ai_mode == "Dumb":
        dumb_ai_move()
    else:
        smart_ai_move()

    Player1 = 'X'
    check_if_win()

def dumb_ai_move():
    empty_cells = [(r, c) for r in range(3) for c in range(3) if states[r][c] == 0]
    if empty_cells:
        r, c = random.choice(empty_cells)
        b[r][c].configure(text='O')
        states[r][c] = 'O'

def smart_ai_move():
    best_score = -float('inf')
    best_move = None

    for r in range(3):
        for c in range(3):
            if states[r][c] == 0:
                states[r][c] = 'O'
                score = minimax(states, False)
                states[r][c] = 0
                if score > best_score:
                    best_score = score
                    best_move = (r, c)

    if best_move:
        r, c = best_move
        b[r][c].configure(text='O')
        states[r][c] = 'O'

def minimax(board, is_maximizing):
    # Check for terminal states
    winner = check_winner_for_minimax(board)
    if winner == 'O':
        return 1
    elif winner == 'X':
        return -1
    elif winner == 'Tie':
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for r in range(3):
            for c in range(3):
                if board[r][c] == 0:
                    board[r][c] = 'O'
                    score = minimax(board, False)
                    board[r][c] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for r in range(3):
            for c in range(3):
                if board[r][c] == 0:
                    board[r][c] = 'X'
                    score = minimax(board, True)
                    board[r][c] = 0
                    best_score = min(score, best_score)
        return best_score

def check_winner_for_minimax(board):
    # Rows and Columns
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != 0:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != 0:
            return board[0][i]

    # Diagonals
    if board[0][0] == board[1][1] == board[2][2] != 0:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != 0:
        return board[0][2]

    # Check tie
    if all(board[r][c] != 0 for r in range(3) for c in range(3)):
        return 'Tie'

    return None

def check_if_win():
    global stop_game

    for i in range(3):
        if states[i][0] == states[i][1] == states[i][2] != 0:
            stop_game = True
            messagebox.showinfo("Winner", states[i][0] + " Won!")
            return

        if states[0][i] == states[1][i] == states[2][i] != 0:
            stop_game = True
            messagebox.showinfo("Winner", states[0][i] + " Won!")
            return

    if states[0][0] == states[1][1] == states[2][2] != 0:
        stop_game = True
        messagebox.showinfo("Winner", states[0][0] + " Won!")
        return

    if states[0][2] == states[1][1] == states[2][0] != 0:
        stop_game = True
        messagebox.showinfo("Winner", states[0][2] + " Won!")
        return

    if all(states[r][c] != 0 for r in range(3) for c in range(3)):
        stop_game = True
        messagebox.showinfo("Tie", "It's a tie!")
        return

def switch_ai_mode():
    global ai_mode, switch_button, stop_game

    if stop_game:
        messagebox.showinfo("Game Over", "Please restart the game to change AI mode.")
        return

    if ai_mode == "Dumb":
        ai_mode = "Smart"
    else:
        ai_mode = "Dumb"

    switch_button.config(text=f"AI Mode: {ai_mode}")

def restart_game():
    global stop_game, Player1, states
    stop_game = False
    Player1 = 'X'
    for i in range(3):
        for j in range(3):
            states[i][j] = 0
            b[i][j].config(text="")
    switch_button.config(state=NORMAL)

# Design window
root = Tk()
root.title("Tic Tac Toe - Player vs AI")
root.resizable(0, 0)

b = [[0 for _ in range(3)] for _ in range(3)]
states = [[0 for _ in range(3)] for _ in range(3)]

for i in range(3):
    for j in range(3):
        b[i][j] = Button(root,
                         height=4, width=8,
                         font=("Helvetica", "20"),
                         command=lambda r=i, c=j: clicked(r, c))
        b[i][j].grid(row=i, column=j)

switch_button = Button(root, text=f"AI Mode: {ai_mode}", command=switch_ai_mode)
switch_button.grid(row=3, column=0, columnspan=2, sticky="we")

restart_button = Button(root, text="Restart Game", command=restart_game)
restart_button.grid(row=3, column=2, sticky="we")

root.mainloop()
