# ---------------------------------
# AUTO-INSTALL pygame IF NOT PRESENT
# ---------------------------------
import sys
import subprocess

try:
    import pygame
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
    import pygame

# ---------------------------------
# INITIAL SETUP
# ---------------------------------
pygame.init()

WIDTH, HEIGHT = 900, 900
LINE_WIDTH = 10
CELL_SIZE = WIDTH // 5

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Touch Tic-Tac-Toe")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)

font = pygame.font.SysFont(None, 40)
big_font = pygame.font.SysFont(None, 50)

# ---------------------------------
# GAME STATE
# ---------------------------------
def reset_game():
    global board, current_player, game_over
    board = [['' for _ in range(3)] for _ in range(3)]
    current_player = 'X'   # Auto start
    game_over = False

reset_game()

# ---------------------------------
# DRAW GRID
# ---------------------------------
def draw_grid():
    for i in range(1, 3):
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE),
                         (WIDTH, i * CELL_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0),
                         (i * CELL_SIZE, HEIGHT), LINE_WIDTH)

# ---------------------------------
# DRAW X AND O
# ---------------------------------
def draw_marks():
    for row in range(3):
        for col in range(3):
            x = col * CELL_SIZE + CELL_SIZE // 2
            y = row * CELL_SIZE + CELL_SIZE // 2

            if board[row][col] == 'X':
                pygame.draw.line(screen, BLUE,
                                 (x - 50, y - 50), (x + 50, y + 50), 8)
                pygame.draw.line(screen, RED,
                                 (x - 50, y + 50), (x + 50, y - 50), 8)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, BLUE, (x, y), 50, 8)

# ---------------------------------
# CHECK WINNER
# ---------------------------------
def check_winner(player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)):
            return True
        if all(board[j][i] == player for j in range(3)):
            return True

    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2 - i] == player for i in range(3)):
        return True

    return False

# ---------------------------------
# CHECK DRAW
# ---------------------------------
def is_draw():
    return all(board[r][c] != '' for r in range(3) for c in range(3))

# ---------------------------------
# SHOW MESSAGE
# ---------------------------------
def show_message(text):
    msg = big_font.render(text, True, BLACK)
    rect = msg.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(msg, rect)

    sub = font.render("Tap anywhere to restart", True, BLACK)
    sub_rect = sub.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(sub, sub_rect)

# ---------------------------------
# MAIN GAME LOOP (TOUCH ONLY)
# ---------------------------------
clock = pygame.time.Clock()

while True:
    screen.fill(WHITE)
    draw_grid()
    draw_marks()

    if game_over:
        if check_winner('X'):
            show_message("Player X Wins!")
        elif check_winner('O'):
            show_message("Player O Wins!")
        else:
            show_message("It's a Draw!")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                reset_game()
            else:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                row = mouse_y // CELL_SIZE
                col = mouse_x // CELL_SIZE

                if board[row][col] == '':
                    board[row][col] = current_player

                    if check_winner(current_player) or is_draw():
                        game_over = True
                    else:
                        current_player = 'O' if current_player == 'X' else 'X'

    pygame.display.update()
    clock.tick(60)