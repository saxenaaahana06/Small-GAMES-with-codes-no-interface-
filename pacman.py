import pygame
import random

pygame.init()
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pacman Game - Roll No 02")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

# Roll number logic
ROLL = 2
PACMAN_SPEED = 4 + ROLL
GHOST_SPEED = 2 + ROLL
PELLET_SCORE = 10 + ROLL

# FSM states
GAME_START = "START"
GAME_PLAY = "PLAY"
GAME_OVER = "OVER"
GAME_WIN = "WIN"

state = GAME_START

pacman = pygame.Rect(300, 300, 25, 25)
ghost = pygame.Rect(100, 100, 25, 25)

pellets = [pygame.Rect(random.randint(50, 550), random.randint(50, 550), 10, 10) for _ in range(10)]
score = 0

def draw_text(text, x, y):
    img = font.render(text, True, (255, 255, 255))
    screen.blit(img, (x, y))

running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and state == GAME_START:
            state = GAME_PLAY

    if state == GAME_START:
        draw_text("Press any key to start", 150, 280)

    elif state == GAME_PLAY:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: pacman.x -= PACMAN_SPEED
        if keys[pygame.K_RIGHT]: pacman.x += PACMAN_SPEED
        if keys[pygame.K_UP]: pacman.y -= PACMAN_SPEED
        if keys[pygame.K_DOWN]: pacman.y += PACMAN_SPEED

        # Ghost FSM – simple chase
        if pacman.x > ghost.x: ghost.x += GHOST_SPEED
        if pacman.x < ghost.x: ghost.x -= GHOST_SPEED
        if pacman.y > ghost.y: ghost.y += GHOST_SPEED
        if pacman.y < ghost.y: ghost.y -= GHOST_SPEED

        for pellet in pellets[:]:
            if pacman.colliderect(pellet):
                pellets.remove(pellet)
                score += PELLET_SCORE

        if pacman.colliderect(ghost):
            state = GAME_OVER
        if len(pellets) == 0:
            state = GAME_WIN

        pygame.draw.rect(screen, (255, 255, 0), pacman)
        pygame.draw.rect(screen, (255, 0, 0), ghost)
        for pellet in pellets:
            pygame.draw.rect(screen, (255, 255, 255), pellet)

        draw_text(f"Score: {score}", 10, 10)

    elif state == GAME_OVER:
        draw_text("GAME OVER", 230, 260)

    elif state == GAME_WIN:
        draw_text("YOU WIN!", 240, 260)

    pygame.display.update()
    clock.tick(60)

pygame.quit()