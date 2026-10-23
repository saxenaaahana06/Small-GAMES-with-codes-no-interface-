import math

# ---------------------------------
# Initialize board
# ---------------------------------
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
        (0,1,2), (3,4,5), (6,7,8),    # rows
        (0,3,6), (1,4,7), (2,5,8),    # columns
        (0,4,8), (2,4,6)              # diagonals
    ]
    return any(board[a] == board[b] == board[c] == player
               for a, b, c in win_conditions)

# ---------------------------------
# Check draw
# ---------------------------------
def is_draw():
    return ' ' not in board

# ---------------------------------
# Minimax Algorithm
# ---------------------------------
def minimax(is_maximizing):
    if check_winner('O'):
        return 1
    if check_winner('X'):
        return -1
    if is_draw():
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                score = minimax(False)
                board[i] = ' '
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax(True)
                board[i] = ' '
                best_score = min(score, best_score)
        return best_score

# ---------------------------------
# AI Move
# ---------------------------------
def ai_move():
    best_score = -math.inf
    move = None

    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax(False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                move = i

    board[move] = 'O'

# ---------------------------------
# Main Game Loop
# ---------------------------------
def play_game():
    print("\n🎮 Tic-Tac-Toe")
    print("You are X | AI is O")
    print("Positions:")
    print(" 0 | 1 | 2 ")
    print("---+---+---")
    print(" 3 | 4 | 5 ")
    print("---+---+---")
    print(" 6 | 7 | 8 ")
    print_board()

    while True:
        # Human move
        try:
            pos = int(input("Enter position (0-8): "))
            if pos < 0 or pos > 8 or board[pos] != ' ':
                print("❌ Invalid move. Try again.")
                continue
        except ValueError:
            print("❌ Enter a valid number.")
            continue

        board[pos] = 'X'
        print_board()

        if check_winner('X'):
            print("🏆 You win!")
            break
        if is_draw():
            print("🤝 It's a draw!")
            break

        # AI move
        print("🤖 AI is thinking...")
        ai_move()
        print_board()

        if check_winner('O'):
            print("💀 AI wins!")
            break
        if is_draw():
            print("🤝 It's a draw!")
            break

# ---------------------------------
# Start game
# ---------------------------------
play_game()
