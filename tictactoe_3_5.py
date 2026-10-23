import math

# ---------------------------------
# BOARD SETUP
# ---------------------------------
SIZE = 5
WIN_LEN = 3
board = [' ' for _ in range(SIZE * SIZE)]

# ---------------------------------
# DISPLAY BOARD
# ---------------------------------
def print_board():
    print()
    for r in range(SIZE):
        row = board[r * SIZE:(r + 1) * SIZE]
        print(" | ".join(row))
    print()

# ---------------------------------
# CHECK WINNER (GENERALIZED)
# ---------------------------------
def check_winner(player):
    grid = [board[i * SIZE:(i + 1) * SIZE] for i in range(SIZE)]

    # Horizontal
    for r in range(SIZE):
        for c in range(SIZE - WIN_LEN + 1):
            if all(grid[r][c + k] == player for k in range(WIN_LEN)):
                return True

    # Vertical
    for c in range(SIZE):
        for r in range(SIZE - WIN_LEN + 1):
            if all(grid[r + k][c] == player for k in range(WIN_LEN)):
                return True

    # Diagonal (\)
    for r in range(SIZE - WIN_LEN + 1):
        for c in range(SIZE - WIN_LEN + 1):
            if all(grid[r + k][c + k] == player for k in range(WIN_LEN)):
                return True

    # Diagonal (/)
    for r in range(SIZE - WIN_LEN + 1):
        for c in range(WIN_LEN - 1, SIZE):
            if all(grid[r + k][c - k] == player for k in range(WIN_LEN)):
                return True

    return False

# ---------------------------------
# CHECK DRAW
# ---------------------------------
def is_draw():
    return ' ' not in board

# ---------------------------------
# MINIMAX
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
        for i in range(SIZE * SIZE):
            if board[i] == ' ':
                board[i] = 'O'
                score = minimax(False)
                board[i] = ' '
                best_score = max(best_score, score)
        return best_score
    else:
        best_score = math.inf
        for i in range(SIZE * SIZE):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax(True)
                board[i] = ' '
                best_score = min(best_score, score)
        return best_score

# ---------------------------------
# AI MOVE
# ---------------------------------
def ai_move():
    best_score = -math.inf
    move = None

    for i in range(SIZE * SIZE):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax(False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                move = i

    board[move] = 'O'

# ---------------------------------
# SAFE HUMAN INPUT
# ---------------------------------
def get_human_move():
    while True:
        val = input(f"Enter position (0-{SIZE*SIZE-1}): ")

        if not val.isdigit():
            print("❌ Enter a number.")
            continue

        pos = int(val)

        if pos < 0 or pos >= SIZE * SIZE:
            print("❌ Out of range.")
            continue

        if board[pos] != ' ':
            print("❌ Cell occupied.")
            continue

        return pos

# ---------------------------------
# MAIN GAME LOOP
# ---------------------------------
def play_game():
    print("🎮 AI Tic-Tac-Toe (5x5 board, 3-in-a-row)")
    print("You are X | AI is O")
    print_board()

    while True:
        # Human move
        pos = get_human_move()
        board[pos] = 'X'
        print_board()

        if check_winner('X'):
            print("🏆 You win!")
            break
        if is_draw():
            print("🤝 Draw!")
            break

        # AI move
        print("🤖 AI thinking...")
        ai_move()
        print_board()

        if check_winner('O'):
            print("💀 AI wins!")
            break
        if is_draw():
            print("🤝 Draw!")
            break

# ---------------------------------
# RUN GAME
# ---------------------------------
play_game()
