import pygame

from libraryImages import load_image

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
w, h = screen.get_size()
screen = pygame.display.set_mode((0.5 * w - 60, 0.5 * h))
pygame.mixer.music.load("data/music_for_start_game.mp3")

all_units = pygame.sprite.Group()
all_enemy = pygame.sprite.Group()
floor = pygame.sprite.Group()
objects = pygame.sprite.Group()
thorns = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
heals = pygame.sprite.Group()
books = pygame.sprite.Group()

from classPlayer import Player
from classBullet import Flame
from classEnemy import StandartEnemy, NoBulletEnemy, NoMovementEnemy
from classMainFloor import MainFloor
from classBlock import Block
from classThorns import Thorns
from classHeal import LittleHeal, BigHeal
from Levels import training_level
from classButton import Button, obj

start_frames = []
for i in range(1, 7):
    im = f"start_screen/{i}.png"
    start_frames.append(pygame.transform.scale(load_image(im), (0.5 * w, 0.5 * h)))


run = True
level = 0


def with_training():
    global run, level
    run = False
    with open("curr_level.txt") as f:
        level = int(f.readline())


def new_game():
    global run, level
    run = False
    with open("save_level.txt", "w") as f:
        f.write("0")
        level = 0


def without_training():
    global run, level
    run = False
    with open("save_level.txt") as f:
        level = int(f.readline())


cl = pygame.time.Clock()
y = 0
r = 0.5
f = True
tt = 0
Button(30, 120, 400, 100, 'Новая игра', new_game)
Button(30, 230, 400, 100, 'Начать c обучения', with_training)
Button(30, 340, 400, 100, 'Начать игру с сохранения', without_training)
pygame.mixer.music.play(-1, 5)
while run:
    screen.fill("black")
    screen.blit(start_frames[0], (0, 0))
    screen.blit(start_frames[1], (-y - 30, 0))
    screen.blit(start_frames[2], (y * 2, 0))
    screen.blit(start_frames[3], (y - 30, 0))
    screen.blit(start_frames[4], (-y * 2, 0))
    screen.blit(start_frames[5], (0, 0))
    y += r
    if y >= 30 and f:
        r = -0.5
        f = False
    elif y <= -30 and not f:
        r = 0.5
        f = True
    for object in obj:
        object.process(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    cl.tick(60)
    pygame.display.flip()
pygame.mixer.music.pause()

MainFloor((w, h), floor)
player = Player(0.5 * w, 0.8 * h, all_units, (w, h), screen)
clock = pygame.time.Clock()
jump = False
f = False
fall = False
motion = ""
screen_image = pygame.transform.scale(load_image("screen.jpg"), (w, h))
screen_finish_image = pygame.transform.scale(load_image("screen_finish.jpg"), (0.5 * w, 0.5 * h))
x = 0
player_attack = False
the_first_download = False


running = True
while running:
    next_level = False
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen.fill((50, 50, 50))
    player.running = True
    while player.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or next_level:
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
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                player_attack = True
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
        jump, fall, player_attack = player.upd(jump, fall, objects, thorns, floor, bullets, heals, player_attack, all_enemy, player_bullets)
        # print(player_attack)
        screen.blit(screen_image, (0, 0))
        if level == 0:
            screen.fill((50, 50, 50))
            level_passed = training_level(screen, w, h, x, objects, thorns, all_enemy, heals, player, books, the_first_download)
            the_first_download = True
            if level_passed:
                next_level = True
        # screen.blit(screen2, (0, 0))
        objects.draw(screen)
        thorns.draw(screen)
        bullets.update(motion, player.v)
        player_bullets.update(motion, player.v)
        objects.update(motion, player.v)
        thorns.update(motion, player.v)
        heals.update(motion, player.v)
        bullets.draw(screen)
        player_bullets.draw(screen)
        heals.draw(screen)
        floor.draw(screen)
        books.draw(screen)
        all_enemy.update(floor, objects, motion, player, bullets, player_bullets)
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
f = open("curr_level.txt", "w")
f.write("0")
f.close()
pygame.quit()
