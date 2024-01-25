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
others = pygame.sprite.Group()

from classPlayer import Player
from classBullet import Flame
from classEnemy import StandartEnemy, NoBulletEnemy, NoMovementEnemy
from classMainFloor import MainFloor
from classBlock import Block
from classThorns import Thorns
from classHeal import LittleHeal, BigHeal
from Levels import training_level, first_level, second_level
from classButton import Button, obj

start_frames = []
for i in range(1, 7):
    im = f"start_screen/{i}.png"
    start_frames.append(pygame.transform.scale(load_image(im), (0.5 * w, 0.5 * h)))
finish_frames = []
for i in range(1, 8):
    im = f"finish_screen/{i}.png"
    finish_frames.append(pygame.transform.scale(load_image(im), (0.5 * w, 0.5 * h)))


run = True
level = 0


def new_game():
    global run, level
    run = False
    with open("curr_level.txt") as f:
        level = int(f.readline())


def continue_game():
    global run, level
    run = False
    with open("save_level.txt") as f:
        level = int(f.readline()) + 1


cl = pygame.time.Clock()
y = 0
r = 0.5
f = True
tt = 0
Button(0.005 * w, 0.2407 * h, 0.2083 * w, 0.0925 * h, 'Новая игра', new_game)
with open("save_level.txt") as c:
    if c.read():
        Button(0.005 * w, 0.3518 * h, 0.2083 * w, 0.0925 * h, 'Продолжить игру', continue_game)
pygame.mixer.music.play(-1, 5)
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
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
    cl.tick(60)
    pygame.display.flip()
pygame.mixer.music.pause()
obj.clear()

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
    if level == 0:
        pygame.mixer.music.load("data\music_for_training_level.mp3")
        pygame.mixer.music.play(-1)
    elif level == 1:
        pygame.mixer.music.load("data\music_for_first_level.mp3")
        pygame.mixer.music.play(-1)
    next_level = False
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen.fill((50, 50, 50))
    player.running = True
    while player.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or next_level:
                player.running = False
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
                jump = False
                f = False
                fall = False
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
            if x < 0:
                x += player.v
            else:
                motion = ""
                player.rect = player.rect.move(-player.v, 0)
                if player.rect.x - player.rect. w < 0:
                    player.rest()
        elif player.rect.x + player.radius > 0.55 * w and (level == 2 and x > -4400):
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
            level_passed = training_level(screen, w, h, x, objects, thorns, all_enemy, heals, player, others,
                                          the_first_download)
            the_first_download = True
            if level_passed:
                next_level = True
        elif level == 1:
            screen.fill((50, 50, 50))
            level_passed = first_level(screen, w, h, x, objects, thorns, all_enemy, heals, player, others, the_first_download)
            the_first_download = True
            if level_passed:
                next_level = True
        elif level == 2:
            screen.fill((50, 50, 50))
            level_passed = second_level(screen, w, h, x, objects, thorns, all_enemy, heals, player, others, the_first_download)
            the_first_download = True
            if level_passed:
                next_level = True
        # screen.blit(screen2, (0, 0))
        objects.draw(screen)
        thorns.draw(screen)
        bullets.update(motion, player.v, objects)
        player_bullets.update(motion, player.v)
        objects.update(motion, player.v)
        thorns.update(motion, player.v)
        heals.update(motion, player.v)
        bullets.draw(screen)
        player_bullets.draw(screen)
        heals.draw(screen)
        if level == 0:
            floor.draw(screen)
        others.draw(screen)
        all_enemy.update(floor, objects, motion, player, bullets, player_bullets)
        all_enemy.draw(screen)
        all_units.draw(screen)
        player.show_hp()
        clock.tick(120)
        pygame.display.flip()
    screen = pygame.display.set_mode((0.5 * w - 180, 0.5 * h))
    run = True
    r = 0.5
    y = -r
    f = True
    x = 0
    mission_passed = pygame.transform.scale(load_image("mission_passed.png"), (0.2135 * w, 0.1305 * h))
    mission_failed = pygame.transform.scale(load_image("mission_failed.png"), (0.2135 * w, 0.1305 * h))
    pygame.mixer.music.stop()


    def retry():
        global run, x, the_first_download, jump, f, fall
        run = False
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
        jump = False
        f = False
        fall = False
        player.rest()


    def next_lvl():
        global run, level, x, the_first_download, jump, f, fall
        run = False
        level += 1
        player.rest()
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
        jump = False
        f = False
        fall = False
        with open("curr_level.txt", "w") as c:
            c.write(str(level))


    def save_level():
        with open("save_level.txt", "w") as c:
            c.write(str(level))


    if level == 0 and next_level:
        Button(0.1015625 * w, 0.2685 * h, 0.1953125 * w, 0.0925 * h, 'Сохраниться', save_level)
        Button(0.1015625 * w, 0.3888 * h, 0.1953125 * w, 0.0925 * h, 'Следующий уровень', next_lvl)
    elif not next_level:
        Button(0.1015625 * w, 0.3888 * h, 0.1953125 * w, 0.0925 * h, 'Заново', retry)
    elif level > 0 and next_level:
        Button(0.1015625 * w, 0.2685 * h, 0.1953125 * w, 0.0925 * h, 'Сохраниться', save_level)
        Button(0.005 * w, 0.3888 * h, 0.1953125 * w, 0.0925 * h, 'Заново', retry)
        Button(0.203125 * w, 0.3888 * h, 0.1953125 * w, 0.0925 * h, 'Следующий уровень', next_lvl)
    pygame.mixer.music.load("data/music_for_finish_window.mp3")
    pygame.mixer.music.play(-1)
    while run:
        screen.fill("black")
        screen.blit(finish_frames[0], (y * 0.2 - 30, 0))
        screen.blit(finish_frames[1], (y * 0.8 - 30, 0))
        screen.blit(finish_frames[2], (y * 2 - 60, 0))
        screen.blit(finish_frames[3], (y * 3 - 90, 0))
        screen.blit(finish_frames[4], (y - 90, 0))
        screen.blit(finish_frames[5], (0, 0))
        screen.blit(finish_frames[6], (0, 0))
        if level == 0 and next_level:
            screen.blit(mission_passed, (0.15 * w - 105, 0))
            font = pygame.font.SysFont('Arial', 40)
            text = font.render("Поздравляю! Вы завершили обучение!", True, "white")
            text1 = font.render("Успеха вам в тёмном лесу!", True, "white")
            screen.blit(text, (0.04 * w, 0.13 * h))
            screen.blit(text1, (0.04 * w, 0.175 * h))
        elif not next_level:
            screen.blit(mission_failed, (0.15 * w - 105, 0))
            font = pygame.font.SysFont('Arial', 40)
            if level == 0:
                text = font.render("Сочувствую, вы провалили обучение(", True, "white")
                screen.blit(text, (0.04 * w, 0.13 * h))
            text1 = font.render("C такими навыками в Тёмный лес нельзя((", True, "white")
            text2 = font.render("Попробуйте снова!", True, "white")
            screen.blit(text1, (0.04 * w, 0.175 * h))
            screen.blit(text2, (0.04 * w, 0.22 * h))
        elif level > 0 and next_level:
            screen.blit(mission_passed, (0.15 * w - 105, 0))
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
                running = False
                run = False
            # if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            #     run = False
        cl.tick(60)
        pygame.display.flip()
    obj.clear()
    pygame.mixer.music.stop()
f = open("curr_level.txt", "w")
f.write("0")
f.close()
pygame.quit()
