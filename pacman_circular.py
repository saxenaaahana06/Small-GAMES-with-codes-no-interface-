import pygame, math, time

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Pacman Circular Chase - Roll 02")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

ROLL = 2
PAC_SPEED = 3 + ROLL
RADIUS = 80 + ROLL * 10
TIME_LIMIT = 20 + ROLL * 5

angle = 0
center = (300, 300)
pacman = pygame.Rect(100, 100, 25, 25)

start_time = time.time()
score = 0
running = True

while running:
    screen.fill((0, 0, 0))
    elapsed = int(time.time() - start_time)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ghost_x = center[0] + RADIUS * math.cos(angle)
    ghost_y = center[1] + RADIUS * math.sin(angle)
    ghost = pygame.Rect(ghost_x, ghost_y, 25, 25)
    angle += 0.03

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: pacman.x -= PAC_SPEED
    if keys[pygame.K_RIGHT]: pacman.x += PAC_SPEED
    if keys[pygame.K_UP]: pacman.y -= PAC_SPEED
    if keys[pygame.K_DOWN]: pacman.y += PAC_SPEED

    score += 1

    pygame.draw.rect(screen, (255, 255, 0), pacman)
    pygame.draw.rect(screen, (255, 0, 0), ghost)

    if pacman.colliderect(ghost):
        screen.blit(font.render("YOU WIN!", True, (0,255,0)), (230,280))
        pygame.display.update()
        pygame.time.delay(2000)
        break

    if elapsed > TIME_LIMIT:
        screen.blit(font.render("TIME UP!", True, (255,0,0)), (230,280))
        pygame.display.update()
        pygame.time.delay(2000)
        break

    screen.blit(font.render(f"Score: {score}", True, (255,255,255)), (10,10))
    screen.blit(font.render(f"Time: {elapsed}", True, (255,255,255)), (10,40))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
