import pygame
import sys
import random
import math

pygame.init()

# ---------- SCREEN ----------
WIDTH = 720
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pacman Touch – Ghost Den Chase")

# ---------- COLORS ----------
RED = (255, 0, 0)
WHITE = (255,255,255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
PINK = (255, 105, 180)
GRAY = (180, 180, 180)

# ---------- CONSTANTS ----------
PACMAN_RADIUS = 25
GHOST_RADIUS = 30        # increased size
HOME_RADIUS = 35

BASE_GHOST_SPEED = 0.8
MAX_GHOST_SPEED = 3.0

# ---------- OBJECTS ----------
pacman_x = random.randint(80, WIDTH - 80)
pacman_y = random.randint(200, HEIGHT - 200)

# Ghost spawns in a larger region
ghost_x = random.randint(50, WIDTH - 50)
ghost_y = random.randint(50, HEIGHT - 50)

home_x = random.randint(150, WIDTH - 150)
home_y = random.randint(300, HEIGHT - 300)

# ---------- SCORE ----------
score = 0
high_score = 0

font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

dragging = False

# ---------- DRAW FUNCTIONS ----------
def draw_pacman(x, y):
    pygame.draw.circle(screen, BLUE, (int(x), int(y)), PACMAN_RADIUS)

def draw_ghost(x, y):
    # head
    pygame.draw.circle(screen, PINK, (int(x), int(y)), GHOST_RADIUS)

    # body
    pygame.draw.rect(
        screen,
        PINK,
        (int(x - GHOST_RADIUS), int(y),
         GHOST_RADIUS * 2, GHOST_RADIUS)
    )

    # eyes
    pygame.draw.circle(screen, WHITE, (int(x - 8), int(y - 5)), 5)
    pygame.draw.circle(screen, WHITE, (int(x + 8), int(y - 5)), 5)
    pygame.draw.circle(screen, BLACK, (int(x - 8), int(y - 3)), 2)
    pygame.draw.circle(screen, BLACK, (int(x + 8), int(y - 3)), 2)

def draw_home(x, y):
    pygame.draw.circle(screen, GRAY, (int(x), int(y)), HOME_RADIUS)

# ---------- MAIN LOOP ----------
while True:
    screen.fill(RED)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # TOUCH START
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if math.hypot(mx - pacman_x, my - pacman_y) <= PACMAN_RADIUS + 10:
                dragging = True

        # TOUCH MOVE
        if event.type == pygame.MOUSEMOTION and dragging:
            pacman_x, pacman_y = pygame.mouse.get_pos()
            score += 1
            high_score = max(high_score, score)

        # TOUCH END
        if event.type == pygame.MOUSEBUTTONUP:
            dragging = False

    # ---------- GHOST MOVES TO DEN ----------
    dx = home_x - ghost_x
    dy = home_y - ghost_y
    dist = math.hypot(dx, dy)

    # speed increases as ghost gets closer to den
    progress = 1 - min(dist / math.hypot(WIDTH, HEIGHT), 1)
    ghost_speed = BASE_GHOST_SPEED + progress * (MAX_GHOST_SPEED - BASE_GHOST_SPEED)

    if dist > 1:
        ghost_x += ghost_speed * dx / dist
        ghost_y += ghost_speed * dy / dist

    # ---------- COLLISIONS ----------
    # Pacman catches ghost
    if math.hypot(pacman_x - ghost_x, pacman_y - ghost_y) <= PACMAN_RADIUS + GHOST_RADIUS:
        score = 0
        pacman_x = random.randint(80, WIDTH - 80)
        pacman_y = random.randint(200, HEIGHT - 200)
        ghost_x = random.randint(50, WIDTH - 50)
        ghost_y = random.randint(50, HEIGHT - 50)
        home_x = random.randint(150, WIDTH - 150)
        home_y = random.randint(300, HEIGHT - 300)

    # Ghost reaches den
    if math.hypot(ghost_x - home_x, ghost_y - home_y) <= HOME_RADIUS:
        score = 0
        ghost_x = random.randint(50, WIDTH - 50)
        ghost_y = random.randint(50, HEIGHT - 50)
        home_x = random.randint(150, WIDTH - 150)
        home_y = random.randint(300, HEIGHT - 300)

    # ---------- DRAW ----------
    draw_home(home_x, home_y)
    draw_pacman(pacman_x, pacman_y)
    draw_ghost(ghost_x, ghost_y)

    text = f"Score: {score}   High Score: {high_score}"
    txt = font.render(text, True, BLACK)
    screen.blit(txt, (20, 40))

    pygame.display.update()
    clock.tick(60)
