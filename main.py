import pygame

from libraryImages import load_image

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
w, h = screen.get_size()
all_units = pygame.sprite.Group()
floor = pygame.sprite.Group()
objects = pygame.sprite.Group()
thorns = pygame.sprite.Group()

from classPlayer import Player
from classMainFloor import MainFloor
from classBlock import Block
from classThorns import Thorns

MainFloor((w, h), floor)
Block(0.2 * w, 1, w, h, objects)
Block(0.2 * w, 2, w, h, objects)
Thorns(0.2 * w, 1, w, h, thorns)
running = True
player = Player(0.5 * w - 20, 0.5 * h - 20, 75, 5, all_units, (w, h), screen)
clock = pygame.time.Clock()
jump = False
f = False
fall = False
screen_image = pygame.transform.scale(load_image("screen2.png"), (w, h))
# FALL = pygame.USEREVENT + 1
# pygame.time.set_timer(FALL, 1)
while player.running:
    screen.fill((50, 50, 50))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            player.running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                player.x1motoin = "y"
            if event.key == pygame.K_a:
                player.x2motoin = "y"
            if (event.key == pygame.K_w or event.key == pygame.K_SPACE) and not jump and not f and not fall and player.jump_count == 0:
                jump = True
                player.jump_count = player.jump_max
            if event.key == pygame.K_LSHIFT:
                player.v *= 2
            if event.key == pygame.K_s:
                f = True
            if event.key == pygame.K_SPACE and f:
                fall = True
                player.jump_count = -player.jump_max
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                player.x1motoin = "n"
            if event.key == pygame.K_a:
                player.x2motoin = "n"
            if event.key == pygame.K_LSHIFT:
                player.v /= 2
            if event.key == pygame.K_s:
                f = False
    if player.rect.x < 0.3 * w:
        player.rect = player.rect.move(-player.vx, 0)
        objects.update("r", player.v)
        thorns.update("r", player.v)
    if player.rect.x + player.radius > 0.7 * w:
        player.rect = player.rect.move(-player.vx, 0)
        objects.update("l", player.v)
        thorns.update("l", player.v)
    jump, fall = player.update(jump, fall, objects, thorns, floor)
    screen.blit(screen_image, (0, 0))
    objects.draw(screen)
    thorns.draw(screen)
    floor.draw(screen)
    all_units.draw(screen)
    player.show_hp()
    clock.tick(120)
    pygame.display.flip()
pygame.quit()
