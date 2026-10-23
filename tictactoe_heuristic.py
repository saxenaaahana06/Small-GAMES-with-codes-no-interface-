import math

SIZE = 3
WIN_LEN = 2
MAX_DEPTH = 1  # ✅ CRITICAL FIX

board = [' ' for _ in range(SIZE * SIZE)]

# ----------------------------
# DISPLAY BOARD
# ----------------------------
def print_board():
    print()
    for r in range(SIZE):
        print(" | ".join(board[r * SIZE:(r + 1) * SIZE]))
    print()

# ----------------------------
# CHECK WINNER
# ----------------------------
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

    # Diagonal \
    for r in range(SIZE - WIN_LEN + 1):
        for c in range(SIZE - WIN_LEN + 1):
            if all(grid[r + k][c + k] == player for k in range(WIN_LEN)):
                return True

    # Diagonal /
    for r in range(SIZE - WIN_LEN + 1):
        for c in range(WIN_LEN - 1, SIZE):
            if all(grid[r + k][c - k] == player for k in range(WIN_LEN)):
                return True

    return False

# ----------------------------
# HEURISTIC EVALUATION
# ----------------------------
def evaluate():
    if check_winner('O'):
        return 100
    if check_winner('X'):
        return -100
    return 0

# ----------------------------
# MINIMAX WITH DEPTH LIMIT
# ----------------------------
def minimax(depth, is_maximizing):
    score = evaluate()

    if abs(score) == 20 or depth == MAX_DEPTH:
        return score

    if is_maximizing:
        best = -math.inf
        for i in range(SIZE * SIZE):
            if board[i] == ' ':
                board[i] = 'O'
                best = max(best, minimax(depth + 1, False))
                board[i] = ' '
        return best
    else:
        best = math.inf
        for i in range(SIZE * SIZE):
            if board[i] == ' ':
                board[i] = 'X'
                best = min(best, minimax(depth + 1, True))
                board[i] = ' '
        return best

# ----------------------------
# AI MOVE
# ----------------------------
def ai_move():
    best_score = -math.inf
    move = None

    for i in range(SIZE * SIZE):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax(0, False)
            board[i] = ' '

            if score > best_score:
                best_score = score
                move = i

    board[move] = 'O'

# ----------------------------
# HUMAN INPUT
# ----------------------------
def get_human_move():
    while True:
        x = input(f"Enter position (0-{SIZE*SIZE-1}): ")
        if x.isdigit():
            pos = int(x)
            if 0 <= pos < SIZE * SIZE and board[pos] == ' ':
                return pos
        print("❌ Invalid move")

# ----------------------------
# MAIN LOOP
# ----------------------------
def play_game():
    print("🎮 5x5 AI Tic-Tac-Toe | 3-in-a-row wins")
    print("You = X | AI = O")
    print_board()

    while True:
        pos = get_human_move()
        board[pos] = 'X'
        print_board()

        if check_winner('X'):
            print("🏆 You win!")
            break

        print("🤖 AI thinking...")
        ai_move()
        print_board()

        if check_winner('O'):
            print("💀 AI wins!")
            break

# ----------------------------
# RUN
# ----------------------------
play_game()