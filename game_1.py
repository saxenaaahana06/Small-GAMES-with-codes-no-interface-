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
pygame.display.set_caption("Pacman Chase – Smooth Touch Version")

# ---------- COLORS ----------
MUSTARD = (245, 204, 77)
BLACK = (0, 0, 0)
GREEN = (0, 180, 0)
PINK = (255, 105, 180)
GRAY = (160, 160, 160)

# ---------- TUNABLE PARAMETERS ----------
DISTANCE_UNITS = [1, 2]
BASE_RADIUS = 120
BASE_GHOST_SPEED = 0.9
ROUND_GAP = 2

PACMAN_RADIUS = 22
GHOST_RADIUS = 22
HOME_RADIUS = 30

TOUCH_RADIUS = 80
SMOOTHING = 0.18   # 🔻 Pacman slower

# ---------- STOPPAGE ----------
STOP_CHANCE = 0.005     # probability per frame
STOP_DURATION = 0.6     # seconds
pacman_stopped_until = 0

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
    home_x = random.randint(200, WIDTH - 200)
    home_y = random.randint(200, HEIGHT - 200)

    x = random.choice(DISTANCE_UNITS)
    y = random.choice(DISTANCE_UNITS)

    theta_g = random.uniform(0, 2 * math.pi)
    theta_p = random.uniform(0, 2 * math.pi)

    ghost_x = home_x + x * BASE_RADIUS * math.cos(theta_g)
    ghost_y = home_y + x * BASE_RADIUS * math.sin(theta_g)

    pacman_x = home_x + y * BASE_RADIUS * math.cos(theta_p)
    pacman_y = home_y + y * BASE_RADIUS * math.sin(theta_p)

    return pacman_x, pacman_y, ghost_x, ghost_y, home_x, home_y


pacman_x, pacman_y, ghost_x, ghost_y, home_x, home_y = generate_positions()

# ---------- DRAW ----------
def draw_pacman(x, y):
    pygame.draw.circle(screen, GREEN, (int(x), int(y)), PACMAN_RADIUS)

def draw_ghost(x, y):
    pygame.draw.circle(screen, PINK, (int(x), int(y)), GHOST_RADIUS)

def draw_home(x, y):
    pygame.draw.rect(
        screen, GRAY,
        (int(x - HOME_RADIUS), int(y - HOME_RADIUS),
         HOME_RADIUS * 2, HOME_RADIUS * 2),
        border_radius=6
    )

# ---------- MAIN LOOP ----------
while True:
    screen.fill(MUSTARD)
    now = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # ----- TOUCH START -----
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if math.hypot(mx - pacman_x, my - pacman_y) <= TOUCH_RADIUS:
                dragging = True
                drag_offset_x = pacman_x - mx
                drag_offset_y = pacman_y - my

        # ----- TOUCH MOVE -----
        if event.type == pygame.MOUSEMOTION and dragging:
            if now > pacman_stopped_until:
                mx, my = pygame.mouse.get_pos()
                target_x = mx + drag_offset_x
                target_y = my + drag_offset_y

                pacman_x += SMOOTHING * (target_x - pacman_x)
                pacman_y += SMOOTHING * (target_y - pacman_y)

                score += 1
                high_score = max(high_score, score)

        # ----- TOUCH END -----
        if event.type == pygame.MOUSEBUTTONUP:
            dragging = False

    # ---------- RANDOM STOPPAGE ----------
    if random.random() < STOP_CHANCE:
        pacman_stopped_until = now + STOP_DURATION

    # ---------- GHOST MOVEMENT ----------
    if ghost_visible:
        dx = home_x - ghost_x
        dy = home_y - ghost_y
        dist = math.hypot(dx, dy)

        if dist > 1:
            # 🔥 Speed increases with score + randomness
            ghost_speed = BASE_GHOST_SPEED + score * 0.004 + random.uniform(-0.2, 0.2)

            ghost_x += ghost_speed * dx / dist
            ghost_y += ghost_speed * dy / dist

    # ---------- PACMAN CATCHES GHOST ----------
    if ghost_visible:
        if math.hypot(pacman_x - ghost_x, pacman_y - ghost_y) <= PACMAN_RADIUS + GHOST_RADIUS:
            ghost_visible = False
            round_restart_time = now + ROUND_GAP
            score = 0

    # ---------- GHOST REACHES HOME ----------
    if ghost_visible:
        if math.hypot(ghost_x - home_x, ghost_y - home_y) <= HOME_RADIUS:
            ghost_visible = False
            high_score = 0
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

    # ---------- SCORE ----------
    txt = font.render(f"Score: {score}   High Score: {high_score}", True, BLACK)
    screen.blit(txt, (20, 40))

    pygame.display.update()
    clock.tick(60)
