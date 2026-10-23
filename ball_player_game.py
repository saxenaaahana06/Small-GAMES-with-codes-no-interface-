import pygame
import time
import random

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 700, 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Catch the ball !!")

SKY_BLUE = (135, 206, 235)
NAVY = (0, 0, 128)
WHITE = (255,255,255)


PADDLE_WIDTH, PADDLE_HEIGHT = 90, 10
paddle = pygame.Rect(
    (SCREEN_WIDTH - PADDLE_WIDTH) // 2,
    int(SCREEN_HEIGHT * 0.75),
    PADDLE_WIDTH,
    PADDLE_HEIGHT
)
paddle_speed = 5

BALL_RADIUS = 8
ball_x = random.randint(BALL_RADIUS, SCREEN_WIDTH - BALL_RADIUS)
ball_y = 0
ball_speed = 12

score = 0
start_time = time.time()

font = pygame.font.SysFont(None, 32)

clock = pygame.time.Clock()

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        running = False

    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle.right < SCREEN_WIDTH:
        paddle.x += paddle_speed

    ball_y += ball_speed

ball_rect = pygame.Rect(ball_x - BALL_RADIUS, ball_y - BALL_RADIUS, BALL_RADIUS*2, BALL_RADIUS*2)

if paddle.colliderect(ball_rect):
    score += 10
    ball_y = 0
    ball_x = random.randint(BALL_RADIUS, SCREEN_WIDTH - BALL_RADIUS)

if ball_y > SCREEN_HEIGHT:
    ball_y = 0
    ball_x = random.randint(BALL_RADIUS, SCREEN_WIDTH - BALL_RADIUS)

    elapsed_time = int(time.time() - start_time)

    screen.fill(NAVY)
    pygame.draw.rect(screen, SKY_BLUE, paddle)
    pygame.draw.circle(screen, SKY_BLUE, (ball_x, ball_y), BALL_RADIUS)

    score_text = font.render(f"Score: {score}", True, WHITE)
    time_text = font.render(f"Time: {elapsed_time} sec", True, WHITE)

    screen.blit(score_text, (20, 20))
    screen.blit(time_text, (20, 50))

    pygame.display.flip()

pygame.quit()