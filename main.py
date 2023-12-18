import pygame

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
w, h = screen.get_size()
all_units = pygame.sprite.Group()
floor = pygame.sprite.Group()
objects = pygame.sprite.Group()

from classPlayer import Player
from classMainFloor import MainFloor
from classBranch import Branch

MainFloor((w, h), floor)
Branch(0.2 * w, 0.5 * h, 100, 50, objects)
running = True
player = Player(0.5 * w - 20, 0.5 * h - 20, 75, 5, all_units, (w, h))
clock = pygame.time.Clock()
# FALL = pygame.USEREVENT + 1
# pygame.time.set_timer(FALL, 1)
while running:
    screen.fill((50, 50, 50))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                player.x1motoin = "y"
            if event.key == pygame.K_a:
                player.x2motoin = "y"
            if (event.key == pygame.K_w or event.key == pygame.K_SPACE):
                player.jump = True
            if event.mod & pygame.KMOD_SHIFT:
                player.v += 5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                player.x1motoin = "n"
            if event.key == pygame.K_a:
                player.x2motoin = "n"
            if event.mod & pygame.KMOD_SHIFT:
                player.v -= 5
                print("player")
            # if (event.key == pygame.K_w or event.key == pygame.K_SPACE):
            #     player.vy = player.vd
    #     if event.type == FALL:
    #         if player.y < 0.8 * h - player.radius:
    #             player.y += 1
    if player.rect.x < 0.3 * w:
        player.rect = player.rect.move(-player.vx, 0)
        objects.update("r", player.v)
    if player.rect.x + player.radius > 0.7 * w:
        player.rect = player.rect.move(-player.vx, 0)
        objects.update("l", player.v)
    # if player.rect.y < 0.9 * h:
    #     player.vy = 0
    # board.render(screen)
    # pygame.draw.rect(screen, "white", (0, 0.8 * h, w, 0.2 * h))
    # pygame.draw.circle(screen, "red", (circle.x, circle.y), circle.radius)
    # pygame.draw.rect(screen, "green", (0.3 * w, 0.3 * h, 0.4 * w, 0.6 * h), 2)
    all_units.update(objects, floor)
    objects.draw(screen)
    floor.draw(screen)
    all_units.draw(screen)
    clock.tick(120)
    pygame.display.flip()
pygame.quit()
