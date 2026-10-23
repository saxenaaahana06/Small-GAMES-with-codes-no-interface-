import pygame, random

pygame.init()
screen = pygame.display.set_mode((700, 400))
pygame.display.set_caption("Mario Endless Runner - Roll 02")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

ROLL = 2
JUMP_POWER = 15 + ROLL * 2
GRAVITY = 1 + ROLL
OBSTACLE_SPEED = 6 + ROLL

mario = pygame.Rect(100, 300, 40, 50)
ground = 350
vel_y = 0
jumping = False

obstacles = []
score = 0
game_over = False

def spawn_obstacle():
    return pygame.Rect(700, 310, 30, 40)

running = True
while running:
    screen.fill((135, 206, 235))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and not jumping:
            if event.key == pygame.K_SPACE:
                vel_y = -JUMP_POWER
                jumping = True

    if not game_over:
        vel_y += GRAVITY
        mario.y += vel_y

        if mario.y >= ground - mario.height:
            mario.y = ground - mario.height
            jumping = False

        if random.randint(1, 60) == 1:
            obstacles.append(spawn_obstacle())

        for obs in obstacles[:]:
            obs.x -= OBSTACLE_SPEED
            if obs.x < -50:
                obstacles.remove(obs)
                score += 5 + ROLL

            if mario.colliderect(obs):
                game_over = True

    pygame.draw.rect(screen, (255, 0, 0), mario)
    for obs in obstacles:
        pygame.draw.rect(screen, (0, 0, 0), obs)

    pygame.draw.line(screen, (0, 255, 0), (0, ground), (700, ground), 3)
    screen.blit(font.render(f"Score: {score}", True, (0,0,0)), (10,10))

    if game_over:
        screen.blit(font.render("GAME OVER", True, (255,0,0)), (280,180))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
