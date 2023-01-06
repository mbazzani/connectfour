import numpy as np
from scipy.signal import convolve2d
import math
import random
import os

ROWS=6
COLUMNS=7

# Play one game of connect four
def play_game():
    clear_screen()
    board = np.zeros((ROWS, COLUMNS), dtype=np.intc)

    # Randomly assign player order
    players = [1, 2]
    random.shuffle(players)
    human_player, computer_player = players

    # Print player order
    print(f"You are Player {human_player}.")
    print(f"The computer is Player {computer_player}.")

    current_player = 1

    while True:
        # Play computer or player depending on the round
        if current_player == human_player:
            player_move(board, human_player)
            if check_winning(board, human_player):
                print("You win!")
                break
        else:
            computer_move(board, 5, computer_player)
            if check_winning(board, computer_player):
                print("You lose")
                break

        current_player = other_player(current_player)

    if not prompt_end():
        play_game()

# Get the player's move and add it to the board
def player_move(board, player):
    while True:
        move = int(input('What move will you make? ')) - 1
        if valid_move(board, move):
            make_move(board, move, player)
            print('Here is the result of your move:')
            print_board(board)
            break
        else:
            print('Invalid move. Try again.')


def computer_move(board, difficulty, player):
    move_vals = []
    for move in range(COLUMNS):
        if valid_move(board, move):
            make_move(board, move, player)
            move_val = minimax(board, difficulty, -math.inf, math.inf, other_player(player))
            unmake_move(board, move)
            move_vals.append(move_val)
        else:
            move_vals.append(math.inf if player == 2 else -math.inf)

    if player == 1:
        move = max(range(len(move_vals)), key=move_vals.__getitem__)
    else:
        move = min(range(len(move_vals)), key=move_vals.__getitem__)

    make_move(board, move, player)
    print('Here is the computer\'s move:')
    print_board(board)

# Returns the relative values of each possible move when
# both players play optimally
def minimax(board, depth, alpha, beta, player):
    # Base cases
    if check_winning(board, 1):
        return 100 + depth
    elif check_winning(board, 2):
        return -(100 + depth)
    elif depth == 0:
        return random.random()

    if player == 1:
        # Player 1 finds highest value move
        max_move_eval = -math.inf
        for move in range(COLUMNS):
            if valid_move(board, move):
                make_move(board, move, player)
                move_eval = minimax(board, depth-1, alpha, beta, 2)
                unmake_move(board, move)
                max_move_eval = max(max_move_eval, move_eval)
                alpha = max(alpha, move_eval)
                if beta <= alpha:
                    break
        return max_move_eval
    else:
        # Player 2 finds lowest (for player one) value move
        min_move_eval = math.inf
        for move in range(COLUMNS):
            if valid_move(board, move):
                make_move(board, move, player)
                move_eval = minimax(board, depth-1, alpha, beta, 1)
                unmake_move(board, move)
                min_move_eval = min(min_move_eval, move_eval)
                beta = min(beta, move_eval)
                if beta <= alpha:
                    break
        return min_move_eval

# Given a player and a board, check if the player
# is winning in that board configuration
def check_winning(board, player):
    new_board = one_hot(board, player)
    horizontal_kernel = np.array([[1, 1, 1, 1]])
    vertical_kernel = np.transpose(horizontal_kernel)
    diag1_kernel = np.eye(4, dtype=np.uint8)
    diag2_kernel = np.fliplr(diag1_kernel)
    detection_kernels = [horizontal_kernel,
                         vertical_kernel,
                         diag1_kernel,
                         diag2_kernel]

    for kernel in detection_kernels:
        if (convolve2d(new_board, kernel, mode='valid') == 4).any():
            return True
    return False

# Checks if any given integer move is valid
def valid_move(board, move):
    if move<0 or move>=COLUMNS:
        return False
    if board[0, move]!=0:
        return False
    return True

# Adds a token to the move column of the board
def make_move(board, move, player):
    for i in range(ROWS-1,-1,-1):
        if board[i, move]==0:
            board[i, move]=player
            return

# Undoes the last move in the given column
def unmake_move(board, move):
    for i in range(ROWS):
        if board[i, move]!=0:
            board[i, move]=0
            return
 
# Prompt user to end program or play another game
def prompt_end():
    response = prompt('\nWould you like to play another game? [y/n]').lower()
    return response not in ['y', 'yes']

# Helper function that prompts the user with the passed message,
# reprompts user if validity_test function returns false,
# or if the response does not match response_type
def prompt(message,
           validity_test=lambda x: True,
           response_type=None):
    response=''
    while True:
        try:
            print(message)
            if response_type is None:
                response = input()
            else:
                response = response_type(input())
        except ValueError:
            print('Please enter a valid value')
            continue
        if validity_test(response):
            return response
        else:
            print('Please enter a valid value')
            continue
    return response

# Returns 1 if passed 2, and 2 if passed 1
def other_player(player):
    return int((not bool(player-1)))+1


def clear_screen():
    os.system("clear")

# Print a numpy array as a connect four board
# Symbols to use given by icons dict
def print_board(board):
    icons = {0:'_',1:'O',2:'X'}
    for row in board:
        for val in row:
            print(icons[val], end=' ')
        print()

    for i in range(1,COLUMNS+1):
        print(i, end=' ')
    print(end='\n\n')


# Fill the board with zeros, except where
# the values/entries equal player
def one_hot(board, player):
    return np.asarray(np.isin(board, player), dtype=np.uint8)

if __name__=="__main__":
    play_game()
