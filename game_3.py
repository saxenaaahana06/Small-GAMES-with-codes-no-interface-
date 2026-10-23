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
pygame.display.set_caption("Pacman Chase – Dynamic Ghost Speed")

# ---------- COLORS ----------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GRAY = (160, 160, 160)

# ---------- CONSTANTS ----------
PACMAN_RADIUS = 22
GHOST_RADIUS = 22
HOME_RADIUS = 30
TOUCH_RADIUS = 80
SMOOTHING = 0.25

BASE_GHOST_SPEED = 1.0
MAX_GHOST_SPEED = 3.0
ROUND_GAP = 2

# Half wall
WALL_X = WIDTH // 2
WALL_THICKNESS = 12
WALL_HEIGHT = HEIGHT // 2
WALL_TOP = HEIGHT // 4

# ---------- SCORE ----------
score = 0
high_score = 0
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

# ---------- STATE ----------
dragging = False
drag_offset_x = 0
drag_offset_y = 0
ghost_visible = True
round_restart_time = 0

# ---------- POSITION GENERATION ----------
def generate_positions():
    home_x = random.randint(80, WALL_X - 80)
    home_y = random.randint(200, HEIGHT - 200)

    pacman_x = random.randint(80, WALL_X - 80)
    pacman_y = random.randint(200, HEIGHT - 200)

    ghost_x = random.randint(WALL_X + 80, WIDTH - 80)
    ghost_y = random.randint(200, HEIGHT - 200)

    return pacman_x, pacman_y, ghost_x, ghost_y, home_x, home_y


pacman_x, pacman_y, ghost_x, ghost_y, home_x, home_y = generate_positions()

# ---------- DRAW ----------
def draw_pacman(x, y):
    pygame.draw.circle(screen, YELLOW, (int(x), int(y)), PACMAN_RADIUS)
    pygame.draw.polygon(
        screen,
        BLACK,
        [(x, y),
         (x + PACMAN_RADIUS, y - 8),
         (x + PACMAN_RADIUS, y + 8)]
    )

def draw_ghost(x, y):
    pygame.draw.circle(screen, RED, (int(x), int(y)), GHOST_RADIUS)
    pygame.draw.circle(screen, WHITE, (int(x - 6), int(y - 4)), 4)
    pygame.draw.circle(screen, WHITE, (int(x + 6), int(y - 4)), 4)

def draw_home(x, y):
    pygame.draw.rect(
        screen,
        GRAY,
        (int(x - HOME_RADIUS), int(y - HOME_RADIUS),
         HOME_RADIUS * 2, HOME_RADIUS * 2),
        border_radius=6
    )

# ---------- MAIN LOOP ----------
while True:
    screen.fill(WHITE)
    now = time.time()

    # Half wall
    wall_rect = pygame.Rect(
        WALL_X - WALL_THICKNESS // 2,
        WALL_TOP,
        WALL_THICKNESS,
        WALL_HEIGHT
    )
    pygame.draw.rect(screen, BLACK, wall_rect)

    # ---------- EVENTS ----------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if math.hypot(mx - pacman_x, my - pacman_y) <= TOUCH_RADIUS:
                dragging = True
                drag_offset_x = pacman_x - mx
                drag_offset_y = pacman_y - my

        if event.type == pygame.MOUSEMOTION and dragging:
            mx, my = pygame.mouse.get_pos()
            target_x = mx + drag_offset_x
            target_y = my + drag_offset_y

            pacman_x += SMOOTHING * (target_x - pacman_x)
            pacman_y += SMOOTHING * (target_y - pacman_y)

        if event.type == pygame.MOUSEBUTTONUP:
            dragging = False

    # ---------- GHOST MOVEMENT ----------
    if ghost_visible:
        dx = home_x - ghost_x
        dy = home_y - ghost_y
        dist = math.hypot(dx, dy)

        # dynamic speed (faster near home)
        max_dist = math.hypot(WIDTH, HEIGHT)
        progress = 1 - min(dist / max_dist, 1)
        ghost_speed = BASE_GHOST_SPEED + (MAX_GHOST_SPEED - BASE_GHOST_SPEED) * progress

        if dist > 1:
            step_x = ghost_speed * dx / dist
            step_y = ghost_speed * dy / dist

            next_x = ghost_x + step_x
            next_y = ghost_y + step_y

            ghost_rect = pygame.Rect(
                next_x - GHOST_RADIUS,
                next_y - GHOST_RADIUS,
                GHOST_RADIUS * 2,
                GHOST_RADIUS * 2
            )

            if ghost_rect.colliderect(wall_rect):
                step_x = -step_x
                step_y = random.choice([-3, 3])

            ghost_x += step_x
            ghost_y += step_y

    # ---------- COLLISIONS ----------
    if ghost_visible:

        # ✅ WIN
        if math.hypot(pacman_x - ghost_x, pacman_y - ghost_y) <= PACMAN_RADIUS + GHOST_RADIUS:
            ghost_visible = False
            round_restart_time = now + ROUND_GAP
            score += 1
            high_score = max(high_score, score)

        # ❌ LOSE
        elif math.hypot(ghost_x - home_x, ghost_y - home_y) <= HOME_RADIUS:
            ghost_visible = False
            score = 0
            round_restart_time = now + ROUND_GAP

    # ---------- NEW ROUND ----------
    if not ghost_visible and now >= round_restart_time:
        pacman_x, pacman_y, ghost_x, ghost_y, home_x, home_y = generate_positions()
        ghost_visible = True

    # ---------- DRAW ----------
    draw_home(home_x, home_y)
    draw_pacman(pacman_x, pacman_y)

    if ghost_visible:
        draw_ghost(ghost_x, ghost_y)

    txt = font.render(f"Score: {score}   High Score: {high_score}", True, BLACK)
    screen.blit(txt, (20, 40))

    pygame.display.update()
    clock.tick(60)