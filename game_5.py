import pygame
import sys
import random
import time
import math

# ---------------- INIT ----------------
pygame.init()
pygame.font.init()

# ---------------- SCREEN ----------------
WIDTH, HEIGHT = 750,750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blue Chase")

# ---------------- COLORS ----------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (40, 90, 255)
RED = (220, 60, 60)
GRAY = (170, 170, 170)

# ---------------- CONSTANTS ----------------
PACMAN_RADIUS = 25
GHOST_RADIUS = 25
HOME_RADIUS = 30
ROUND_GAP = 2

# ---------------- GAME STATES ----------------
MENU = 0
PLAYING = 1
GAME_OVER = 2
game_state = MENU

# ---------------- FONTS ----------------
title_font = pygame.font.SysFont(None, 72)
font = pygame.font.SysFont(None, 36)

clock = pygame.time.Clock()

# ---------------- FUNCTIONS ----------------
def random_pos():
    return (
        random.randint(100, WIDTH - 100),
        random.randint(200, HEIGHT - 200)
    )

def reset_round():
    global pacman_x, pacman_y, ghost_x, ghost_y, home_x, home_y
    pacman_x, pacman_y = random_pos()
    ghost_x, ghost_y = random_pos()
    home_x, home_y = random_pos()

def draw_text(text, fnt, color, x, y, center=True):
    img = fnt.render(text, True, color)
    rect = img.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(img, rect)

# ---------------- GAME VARIABLES ----------------
score = 0
high_score = 0
round_number = 1
ghost_visible = True
round_restart_time = 0
dragging = False

reset_round()

# ---------------- MAIN LOOP ----------------
while True:
    screen.fill(WHITE)
    now = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # ---------- MENU ----------
        if game_state == MENU:
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_state = PLAYING
                score = 0
                round_number = 1
                reset_round()

        # ---------- PLAYING ----------
        if game_state == PLAYING:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if math.hypot(mx - pacman_x, my - pacman_y) <= PACMAN_RADIUS + 10:
                    dragging = True

            if event.type == pygame.MOUSEMOTION and dragging:
                pacman_x, pacman_y = pygame.mouse.get_pos()
                score += 1
                high_score = max(high_score, score)

            if event.type == pygame.MOUSEBUTTONUP:
                dragging = False

        # ---------- GAME OVER ----------
        if game_state == GAME_OVER:
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_state = MENU

    # ================= PLAY LOGIC =================
    if game_state == PLAYING and ghost_visible:
        ghost_speed = 1.2 + round_number * 0.2

        dx = home_x - ghost_x
        dy = home_y - ghost_y
        dist = math.hypot(dx, dy)

        if dist > 1:
            ghost_x += ghost_speed * dx / dist
            ghost_y += ghost_speed * dy / dist

        # Collision: Player catches ghost
        if math.hypot(pacman_x - ghost_x, pacman_y - ghost_y) <= PACMAN_RADIUS + GHOST_RADIUS:
            ghost_visible = False
            round_restart_time = now + ROUND_GAP
            round_number += 1

        # Ghost reaches home (Game Over)
        if math.hypot(ghost_x - home_x, ghost_y - home_y) <= HOME_RADIUS:
            game_state = GAME_OVER

    # ---------- NEW ROUND ----------
    if game_state == PLAYING and not ghost_visible and now >= round_restart_time:
        reset_round()
        ghost_visible = True

    # ================= DRAW =================
    if game_state == MENU:
        draw_text("BLUE CHASE", title_font, BLUE, WIDTH//2, HEIGHT//2 - 100)
        draw_text("Click to Start", font, BLACK, WIDTH//2, HEIGHT//2)

    elif game_state == PLAYING:
        pygame.draw.circle(screen, GRAY, (int(home_x), int(home_y)), HOME_RADIUS)
        pygame.draw.circle(screen, BLUE, (int(pacman_x), int(pacman_y)), PACMAN_RADIUS)

        if ghost_visible:
            pygame.draw.circle(screen, RED, (int(ghost_x), int(ghost_y)), GHOST_RADIUS)

        draw_text(f"Score: {score}", font, BLACK, 20, 20, center=False)
        draw_text(f"High Score: {high_score}", font, BLACK, 20, 60, center=False)
        draw_text(f"Round: {round_number}", font, BLACK, 20, 100, center=False)

    elif game_state == GAME_OVER:
        draw_text("GAME OVER", title_font, RED, WIDTH//2, HEIGHT//2 - 80)
        draw_text(f"Final Score: {score}", font, BLACK, WIDTH//2, HEIGHT//2)
        draw_text("Click to return to Menu", font, BLACK, WIDTH//2, HEIGHT//2 + 60)

    pygame.display.update()
    clock.tick(60)