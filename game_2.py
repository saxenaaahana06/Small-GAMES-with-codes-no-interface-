import pygame
import sys
import random
import time
import math

pygame.init()

# ---------- SCREEN ----------
WIDTH = 720
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Pacman Touch Game")

# ---------- COLORS ----------
SOFT_PINK = (255, 200, 210)   # background
GREEN = (0, 180, 0)          # pacman
ORANGE = (255, 140, 0)       # ghost
BLACK = (0, 0, 0)

# ---------- OBJECT RADII (changed) ----------
PACMAN_RADIUS = 30
GHOST_RADIUS = 20

# ---------- RANDOM POSITION ----------
def random_pos():
    return (
        random.randint(100, WIDTH - 100),
        random.randint(200, HEIGHT - 200)
    )

pacman_x, pacman_y = random_pos()
ghost_x, ghost_y = random_pos()

# ---------- SCORE ----------
score = 0
high_score = 0

font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

dragging = False

# ---------- GAME STATE ----------
ghost_visible = True
ghost_respawn_time = 0

# ---------- MAIN LOOP ----------
while True:
    screen.fill(SOFT_PINK)
    current_time = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # ----- TOUCH START -----
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if math.hypot(mx - pacman_x, my - pacman_y) <= PACMAN_RADIUS + 20:
                dragging = True

        # ----- TOUCH MOVE -----
        if event.type == pygame.MOUSEMOTION and dragging:
            pacman_x, pacman_y = pygame.mouse.get_pos()
            score += random.randint(1, 3)  # more randomness
            high_score = max(high_score, score)

        # ----- TOUCH END -----
        if event.type == pygame.MOUSEBUTTONUP:
            dragging = False

    # ---------- COLLISION ----------
    if ghost_visible:
        if math.hypot(pacman_x - ghost_x, pacman_y - ghost_y) <= PACMAN_RADIUS + GHOST_RADIUS:
            ghost_visible = False
            ghost_respawn_time = current_time + random.uniform(1.5, 3.5)
            score = 0

    # ---------- RESPAWN GHOST ----------
    if not ghost_visible and current_time >= ghost_respawn_time:
        ghost_x, ghost_y = random_pos()
        ghost_visible = True

    # ---------- DRAW ----------
    pygame.draw.circle(screen, GREEN, (int(pacman_x), int(pacman_y)), PACMAN_RADIUS)

    if ghost_visible:
        pygame.draw.circle(screen, ORANGE, (int(ghost_x), int(ghost_y)), GHOST_RADIUS)

    # ---------- SCORE ----------
    text = f"Score: {score}   High Score: {high_score}"
    txt = font.render(text, True, BLACK)
    screen.blit(txt, (20, 40))

    pygame.display.update()
    clock.tick(60)
