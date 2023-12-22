import sys

class State:
    def __init__(self, board, turn):
        self.board = board
        self.turn = turn

count = 1

# Function to get the player whose turn is next
def moves_next(state):
    return state.turn

def actions(state):
    return [i+1 for i in range(9) if state.board[i] is None]

def result(state, action):
    action -= 1  # Adjust action to zero-based index
    new_board = state.board[:]
    new_board[action] = state.turn
    new_turn = 'o' if state.turn == 'x' else 'x'
    return State(new_board, new_turn)

# Function to check if the current state is terminal (game over)
def is_terminal(state):
    return any(check_winner(state.board, 'x' if state.turn == 'o' else 'o')) or not actions(state)

# Function to check for a winning combination on the board
def check_winner(board, player):
    win_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]  # Diagonals
    ]
    return [pos for pos in win_combinations if all(board[i] == player for i in pos)]

# Function to calculate the utility value for the current state
def utility(state, initial_player):
    winner = check_winner(state.board, 'x')
    if winner:
        return 1 if initial_player == 'x' else -1
    winner = check_winner(state.board, 'o')
    if winner:
        return 1 if initial_player == 'o' else -1
    return 0

# MiniMax Search Algorithm
def minimax_search(state):
    val_move_tuple = min_value(state)
    value = val_move_tuple[0]
    move = val_move_tuple[1]
    return move

# MiniMax Search Algorithm for the opponent's turn
def minimax_search2(state):
    val_move_tuple = max_value(state)
    value = val_move_tuple[0]
    move = val_move_tuple[1]
    return move

# MiniMax: Max Value function
def max_value(state):
    if is_terminal(state):
        util = utility(state, initial_player)
        return util, None
    
    v = float('-inf')
    for a in actions(state):
        global count
        count = count + 1
        result_state = result(state, a)
        the_tuple = min_value(result_state)
        v2 = the_tuple[0]
        if v2 > v:
            v = v2
            move = a
    return v, move

# MiniMax: Min Value function
def min_value(state):
    if is_terminal(state):
        util = utility(state, initial_player)
        return util, None
    
    v = float('inf')
    for a in actions(state):
        global count
        count = count + 1
        the_tuple = max_value(result(state, a))
        v2 = the_tuple[0]
        if v2 < v:
            v = v2
            move = a
    return v, move

def alpha_beta_search(state):
    val_move_tuple = alpha_beta_min_val(state, float('-inf'), float('inf'))
    value = val_move_tuple[0]
    move = val_move_tuple[1]
    return move

def alpha_beta_search2(state):
    val_move_tuple = alpha_beta_max_val(state, float('-inf'), float('inf'))
    value = val_move_tuple[0]
    move = val_move_tuple[1]
    return move

def alpha_beta_min_val(state, alpha, beta):
    if is_terminal(state):
        util = utility(state, initial_player)
        return util, None
    
    v = float('inf')
    move = None  # Initialize move as None

    for a in actions(state):
        global count
        count = count + 1
        the_tuple = alpha_beta_max_val(result(state, a), alpha, beta)
        v2 = the_tuple[0]
        if v2 < v:
            v = v2
            move = a
            beta = min(beta, v)
        if v <= alpha:
            return v, move

    return v, move

def alpha_beta_max_val(state, alpha, beta):
    if is_terminal(state):
        util = utility(state, initial_player)
        return util, None
    
    v = float('-inf')
    move = None  # Initialize move as None

    for a in actions(state):
        global count
        count = count + 1
        the_tuple = alpha_beta_min_val(result(state, a), alpha, beta)
        v2 = the_tuple[0]
        if v2 > v:
            v = v2
            move = a
            alpha = max(alpha, v)
        if v >= beta:
            return v, move

    return v, move

# Function to print the game board
def print_board(board):
    print("     |     |     ")
    print(f"  {board[0] or ' '}  |  {board[1] or ' '}  |  {board[2] or ' '}  ")
    print("     |     |     ")
    print("-----+-----+-----")
    print("     |     |     ")
    print(f"  {board[3] or ' '}  |  {board[4] or ' '}  |  {board[5] or ' '}  ")
    print("     |     |     ")
    print("-----+-----+-----")
    print("     |     |     ")
    print(f"  {board[6] or ' '}  |  {board[7] or ' '}  |  {board[8] or ' '}  ")
    print("     |     |     ")

# Function to get player input for a human player
def get_player_input(current_state):
    while True:
        print(f"{current_state.turn}'s move. Enter your move (possible moves at the moment are: {actions(current_state)}, enter 0 to exit):")
        player_input = input()
        if player_input == '0':
            exit()
        if player_input in map(str, actions(current_state)):
            return int(player_input)

# Function to print the current game board
def print_current_board(current_state):
    print_board(current_state.board)

# Function to play the game: Human vs. Computer
def play_human_vs_computer(initial_player, current_state):
    while not is_terminal(current_state):
        print_current_board(current_state)  # Print the current board
        if current_state.turn == initial_player:
            print(f"{initial_player}'s move. What is your move (possible moves at the moment are: {actions(current_state)} | enter 0 to exit the game)?")
            player_input = input()
            possible_actions = list(map(str, actions(current_state)))

            while player_input not in possible_actions and not player_input == '0':
                print(f"{initial_player}'s move. What is your move (possible moves at the moment are: {actions(current_state)} | enter 0 to exit the game)?")
                player_input = input()

            if player_input == '0':
                exit()

            if player_input in possible_actions:
                current_state = result(current_state, int(player_input))
        else:
            move = minimax_search(current_state)
            print(f"{current_state.turn}'s selected move: {move}. Number of search tree nodes generated:", count)
            current_state = result(current_state, move)

    print_current_board(current_state)  # Print the final board
    print_result(current_state, initial_player)

# Function to play the game: Computer vs. Computer with Minimax
def play_computer_vs_computer(initial_player, current_state):
    while not is_terminal(current_state):
        print_current_board(current_state)  # Print the current board for each move

        if current_state.turn == initial_player:
            move = minimax_search(current_state)
        else:
            move = minimax_search2(current_state)

        print(f"{current_state.turn}'s selected move: {move}. Number of search tree nodes generated:", count)
        current_state = result(current_state, move)

    print_current_board(current_state)  # Print the final board
    print_result(current_state, initial_player)

# Function to play the game: Human vs. Computer with Alpha-Beta Pruning
def play_human_vs_computer_alpha_beta(initial_player, current_state):
    while not is_terminal(current_state):
        print_current_board(current_state)  # Print the current board
        if current_state.turn == initial_player:
            print(f"{initial_player}'s move. What is your move (possible moves at the moment are: {actions(current_state)} | enter 0 to exit the game)?")
            player_input = input()
            possible_actions = list(map(str, actions(current_state)))

            while player_input not in possible_actions and not player_input == '0':
                print(f"{initial_player}'s move. What is your move (possible moves at the moment are: {actions(current_state)} | enter 0 to exit the game)?")
                player_input = input()

            if player_input == '0':
                exit()

            if player_input in possible_actions:
                current_state = result(current_state, int(player_input))
        else:
            move = alpha_beta_search(current_state)
            print(f"{current_state.turn}'s selected move: {move}. Number of search tree nodes generated:", count)
            current_state = result(current_state, move)
    print_current_board(current_state)  # Print the final board
    print_result(current_state, initial_player)

# Function to play the game: Computer vs. Computer with Alpha-Beta Pruning
def play_computer_vs_computer_alpha_beta(initial_player, current_state):
    while not is_terminal(current_state):
        print_current_board(current_state)  # Print the current board for each move

        if current_state.turn == initial_player:
            move = alpha_beta_search(current_state)
        else:
            move = alpha_beta_search2(current_state)

        print(f"{current_state.turn}'s selected move: {move}. Number of search tree nodes generated:", count)
        current_state = result(current_state, move)

    print_current_board(current_state)  # Print the final board
    print_result(current_state, initial_player)

# Function to print the game result
def print_result(current_state, initial_player):
    final_result = utility(current_state, initial_player)
    if final_result == 1 and initial_player == 'x':
        print("X WON")
    elif final_result == 1 and initial_player == 'o':
        print("O WON")
    elif final_result == -1 and initial_player == 'x':
        print("X LOST")
    elif final_result == -1 and initial_player == 'o':
        print("O LOST")
    elif final_result == 0:
        print("TIE")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("ERROR: Not enough/too many input arguments.")
        sys.exit()

    algorithm = int(sys.argv[1])
    initial_player = sys.argv[2].lower()
    mode = int(sys.argv[3])

    print("Sharma, Shambhawi, A20459117 solution:")

    if algorithm == 1:
        print("Algorithm: MiniMax")
        init_board = State([None] * 9, initial_player)
        current_state = init_board
        if mode == 1:
            print("Mode: human versus computer")
            print("First: ", initial_player)
            play_human_vs_computer(initial_player, current_state)
        elif mode == 2:
            print("Mode: computer versus computer")
            print("First: ", initial_player)
            play_computer_vs_computer(initial_player, current_state)
    elif algorithm == 2:
        print("Algorithm: MiniMax with alpha-beta pruning")
        init_board = State([None] * 9, initial_player)
        current_state = init_board
        if mode == 1:
            print("Mode: human versus computer")
            print("First: ", initial_player)
            play_human_vs_computer_alpha_beta(initial_player, current_state)
        elif mode == 2:
            print("Mode: computer versus computer")
            print("First: ", initial_player)
            play_computer_vs_computer_alpha_beta(initial_player, current_state)
    else:
        print("ERROR: Invalid player number")