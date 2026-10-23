# ---------------------------------
# Two-Player Tic-Tac-Toe (X vs O)
# ---------------------------------

# Initialize empty board
board = [' ' for _ in range(9)]

# ---------------------------------
# Display board
# ---------------------------------
def print_board():
    print()
    for i in range(0, 9, 3):
        print(f" {board[i]} | {board[i+1]} | {board[i+2]} ")
        if i < 6:
            print("---+---+---")
    print()

# ---------------------------------
# Check winner
# ---------------------------------
def check_winner(player):
    win_conditions = [
        (0,1,2), (3,4,5), (6,7,8),   # rows
        (0,3,6), (1,4,7), (2,5,8),   # columns
        (0,4,8), (2,4,6)             # diagonals
    ]
    return any(board[a] == board[b] == board[c] == player
               for a, b, c in win_conditions)

# ---------------------------------
# Check draw
# ---------------------------------
def is_draw():
    return ' ' not in board

# ---------------------------------
# Safe input for players
# ---------------------------------
def get_valid_move(player):
    while True:
        move = input(f"Player {player}, enter position (0-8): ")

        if not move.isdigit():
            print("❌ Please enter a number.")
            continue

        pos = int(move)

        if pos < 0 or pos > 8:
            print("❌ Position must be between 0 and 8.")
            continue

        if board[pos] != ' ':
            print("❌ Cell already occupied.")
            continue

        return pos

# ---------------------------------
# Main game loop
# ---------------------------------
def play_game():
    current_player = 'X'

    print("\n🎮 Two-Player Tic-Tac-Toe")
    print("Player X vs Player O")
    print("Board positions:")
    print(" 0 | 1 | 2 ")
    print("---+---+---")
    print(" 3 | 4 | 5 ")
    print("---+---+---")
    print(" 6 | 7 | 8 ")

    print_board()

    while True:
        pos = get_valid_move(current_player)
        board[pos] = current_player
        print_board()

        if check_winner(current_player):
            print(f"🏆 Player {current_player} wins!")
            break

        if is_draw():
            print("🤝 It's a draw!")
            break

        current_player = 'O' if current_player == 'X' else 'X'

# ---------------------------------
# Start the game
# ---------------------------------
play_game()
