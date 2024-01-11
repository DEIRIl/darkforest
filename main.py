import pygame

from libraryImages import load_image

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
w, h = screen.get_size()
screen = pygame.display.set_mode((0.5 * w, 0.5 * h))
all_units = pygame.sprite.Group()
floor = pygame.sprite.Group()
objects = pygame.sprite.Group()
thorns = pygame.sprite.Group()

from classPlayer import Player
from classEnemy import Enemy
from classMainFloor import MainFloor
from classBlock import Block
from classThorns import Thorns

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


def training_level():
    global the_first_download
    font = pygame.font.Font(None, 50)
    text = font.render("Для движения нажмите и удерживайте клавиши 'A' или 'D'", True, "white")
    text2 = font.render("Для прыжка нажмите 'W' или 'SPACE'", True, "white")
    text3 = font.render("Вы можете запрыгнуть на платформу", True, "white")
    text4 = font.render("Находясь на платформе вы можете нажать одновременно 'S' и 'SPACE' чтобы спрыгнуть с платформы", True, "white")
    text5 = font.render("Чтобы ускориться зажмите 'SHIFT'", True, "white")
    text6 = font.render("Совет вам, игрок, не натыкайтесь на шипы, а то будет бобо...", True, "white")
    screen.blit(text, (0.3 * w + x, 0.4 * h))
    screen.blit(text2, (1.3 * w + x, 0.4 * h))
    screen.blit(text3, (2.3 * w + x, 0.4 * h))
    screen.blit(text4, (3.3 * w + x, 0.4 * h))
    screen.blit(text5, (4.5 * w + x, 0.4 * h))
    screen.blit(text6, (6 * w + x, 0.4 * h))
    if not the_first_download:
        the_first_download = True
        Block(2.5 * w + x, 1, w, h, objects)
        Block(3.7 * w + x, 1, w, h, objects)
        Block(3.7 * w + x, 2, w, h, objects)
        Thorns(6.3 * w + x, 1, w, h, thorns)


running = True
while running:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen.fill((50, 50, 50))
    player.running = True
    while player.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                player.running = False
                player.rect.x = 0.5 * w
                player.rect.y = 0.8 * h
                player.hp = player.max_hp
                x = 0
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
        if player.rect.x < 0.35 * w:
            player.rect = player.rect.move(-player.vx, 0)
            objects.update("r", player.v)
            thorns.update("r", player.v)
            motion = "r"
            x += player.v
        elif player.rect.x + player.radius > 0.65 * w:
            player.rect = player.rect.move(-player.vx, 0)
            objects.update("l", player.v)
            thorns.update("l", player.v)
            motion = "l"
            x -= player.v
        else:
            motion = ""
        jump, fall = player.upd(jump, fall, objects, thorns, floor)
        screen.blit(screen_image, (0, 0))
        if level == 0:
            screen.fill((50, 50, 50))
            training_level()
        # screen.blit(screen2, (0, 0))
        objects.draw(screen)
        thorns.draw(screen)
        floor.draw(screen)
        all_units.update(floor, objects, motion)
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
