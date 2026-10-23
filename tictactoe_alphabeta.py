# --------------------------------------------------
# TIC-TAC-TOE WITH ALPHA–BETA PRUNING
# --------------------------------------------------
SIZE = 5
WIN_LEN = 3
board = [' ' for _ in range(SIZE * SIZE)]

def print_board():
    print()
    for r in range(SIZE):
        print(" | ".join(board[r*SIZE:(r+1)*SIZE]))
    print()

def check_winner(player):
    grid = [board[i*SIZE:(i+1)*SIZE] for i in range(SIZE)]

    for r in range(SIZE):
        for c in range(SIZE - WIN_LEN + 1):
            if all(grid[r][c+k] == player for k in range(WIN_LEN)):
                return True

    for c in range(SIZE):
        for r in range(SIZE - WIN_LEN + 1):
            if all(grid[r+k][c] == player for k in range(WIN_LEN)):
                return True

    for r in range(SIZE - WIN_LEN + 1):
        for c in range(SIZE - WIN_LEN + 1):
            if all(grid[r+k][c+k] == player for k in range(WIN_LEN)):
                return True

    for r in range(SIZE - WIN_LEN + 1):
        for c in range(WIN_LEN - 1, SIZE):
            if all(grid[r+k][c-k] == player for k in range(WIN_LEN)):
                return True

    return False

def is_draw():
    return ' ' not in board

# ---------------- ALPHA–BETA MINIMAX ----------------
def minimax_ab(depth, alpha, beta, maximizing):
    if check_winner('O'):
        return 10 - depth
    if check_winner('X'):
        return depth - 10
    if is_draw() or depth == 0:
        return 0

    if maximizing:
        max_eval = -math.inf
        for i in range(SIZE * SIZE):
            if board[i] == ' ':
                board[i] = 'O'
                eval = minimax_ab(depth-1, alpha, beta, False)
                board[i] = ' '
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = math.inf
        for i in range(SIZE * SIZE):
            if board[i] == ' ':
                board[i] = 'X'
                eval = minimax_ab(depth-1, alpha, beta, True)
                board[i] = ' '
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return min_eval

def ai_move():
    best_score = -math.inf
    move = None

    for i in range(SIZE * SIZE):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax_ab(3, -math.inf, math.inf, False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                move = i

    board[move] = 'O'

def get_human_move():
    while True:
        x = input(f"Enter position (0-{SIZE*SIZE-1}): ")
        if x.isdigit():
            pos = int(x)
            if 0 <= pos < SIZE*SIZE and board[pos] == ' ':
                return pos
        print("❌ Invalid move")

def play_game():
    print("\n🎮 5x5 Tic-Tac-Toe (3-in-a-row)")
    print("You = X | AI = O")
    print_board()

    while True:
        board[get_human_move()] = 'X'
        print_board()

        if check_winner('X'):
            print("🏆 You win!")
            break
        if is_draw():
            print("🤝 Draw!")
            break

        print("🤖 AI thinking...")
        ai_move()
        print_board()

        if check_winner('O'):
            print("💀 AI wins!")
            break
        if is_draw():
            print("🤝 Draw!")
            break

play_game()
