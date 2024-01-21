import pygame

from libraryImages import load_image

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
w, h = screen.get_size()
screen = pygame.display.set_mode((0.5 * w, 0.5 * h))

all_units = pygame.sprite.Group()
all_enemy = pygame.sprite.Group()
floor = pygame.sprite.Group()
objects = pygame.sprite.Group()
thorns = pygame.sprite.Group()
bullets = pygame.sprite.Group()
heals = pygame.sprite.Group()

from classPlayer import Player
from classEnemy import StandartEnemy, NoBulletEnemy, NoMovementEnemy
from classMainFloor import MainFloor
from classBlock import Block
from classThorns import Thorns
from classHeal import LittleHeal, BigHeal
from Levels import training_level
from classButton import Button

run = True
while run:
    screen.fill("white")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            run = False
    pygame.display.flip()

MainFloor((w, h), floor)
player = Player(0.5 * w, 0.8 * h, all_units, (w, h), screen)
clock = pygame.time.Clock()
jump = False
f = False
fall = False
motion = ""
screen_image = pygame.transform.scale(load_image("screen.jpg"), (w, h))
screen_finish_image = pygame.transform.scale(load_image("screen_finish.jpg"), (0.5 * w, 0.5 * h))
level = 0
x = 0
the_first_download = False


running = True
while running:
    next_level = False
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen.fill((50, 50, 50))
    player.running = True
    while player.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                player.running = False
                player.vx = 0
                player.v = 10
                player.rect.x = 0.5 * w
                player.rect.y = 0.8 * h
                x = 0
                for it in bullets:
                    it.kill()
                bullets.clear(screen, pygame.Surface((w, h)))
                for it in heals:
                    it.kill()
                heals.clear(screen, pygame.Surface((w, h)))
                for it in all_enemy:
                    it.kill()
                all_enemy.clear(screen, pygame.Surface((w, h)))
                for it in objects:
                    it.kill()
                objects.clear(screen, pygame.Surface((w, h)))
                for it in thorns:
                    it.kill()
                thorns.clear(screen, pygame.Surface((w, h)))
                the_first_download = False
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
        if player.rect.x < 0.45 * w:
            motion = "r"
            player.rect = player.rect.move(player.v, 0)
            x += player.v
        elif player.rect.x + player.radius > 0.55 * w:
            motion = "l"
            player.rect = player.rect.move(-player.v, 0)
            x -= player.v
        else:
            motion = ""
        jump, fall = player.upd(jump, fall, objects, thorns, floor, bullets, heals)
        screen.blit(screen_image, (0, 0))
        if level == 0:
            screen.fill((50, 50, 50))
            level_passed = training_level(screen, w, h, x, objects, thorns, all_enemy, heals, player)
            if level_passed:
                next_level = True
        # screen.blit(screen2, (0, 0))
        objects.draw(screen)
        thorns.draw(screen)
        bullets.update(motion, player.v)
        objects.update(motion, player.v)
        thorns.update(motion, player.v)
        heals.update(motion, player.v)
        bullets.draw(screen)
        heals.draw(screen)
        floor.draw(screen)
        all_enemy.update(floor, objects, motion, player, bullets)
        all_enemy.draw(screen)
        all_units.draw(screen)
        player.show_hp()
        clock.tick(120)
        pygame.display.flip()
    screen = pygame.display.set_mode((0.5 * w, 0.5 * h))
    run = True
    while run:
        screen.blit(screen_finish_image, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                run = False
        pygame.display.flip()
pygame.quit()
