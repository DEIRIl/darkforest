import pygame

from classBlock import Block
from classEnemy import StandartEnemy, NoBulletEnemy, NoMovementEnemy
from classHeal import LittleHeal, BigHeal
from classThorns import Thorns
from libraryImages import load_image


def training_level(screen, w, h, x, objects, thorns, all_enemy, heals, player, others, the_first_download):
    global fin, frames, frame_tick, current_frame
    font = pygame.font.Font(None, 50)
    text = font.render("Для движения нажмите и удерживайте клавиши 'A' или 'D'", True, "white")
    text2 = font.render("Для прыжка нажмите 'W' или 'SPACE'", True, "white")
    text3 = font.render("Вы можете запрыгнуть на платформу", True, "white")
    text4 = font.render("Находясь на платформе вы можете нажать одновременно 'S' и 'SPACE' чтобы спрыгнуть с платформы", True, "white")
    text5 = font.render("Чтобы ускориться зажмите 'SHIFT'", True, "white")
    text6 = font.render("Совет вам, игрок, не натыкайтесь на шипы, а то будет бобо...", True, "white")
    text7 = font.render("В вашем путешествии вам встретится множество врагов", True, "white")
    text8 = font.render("Простые туземцы", True, "white")
    text9 = font.render("Безобидный комок слизи, который кстати лучше не трогать", True, "white")
    text10 = font.render("Злобное дерево, которое так и норовит насадить вас на ветку)))", True, "white")
    text11 = font.render("Ха-ха я надеюсь с твоим здоровьем всё хорошо", True, "white")
    text12 = font.render("Но всё же на всякий случай, возьми излечись)", True, "white")
    text13 = font.render("Эх ладно, не могу я тебя просто так отпустить, вот возьми почитай", True, "white")
    text14 = font.render("Так вот к слову об этой замечательной книжечке", True, "white")
    text15 = font.render("Это книга по базовому владению магией огня", True, "white")
    text16 = font.render("И думаю, что ты заметил, что большинство текста замазано)", True, "white")
    text17 = font.render("Моя работка)))", True, "white")
    text18 = font.render("Ну, а по делу, чтобы запустить заряд огня, нажми на ЛКМ", True, "white")
    text19 = font.render("А теперь удачной дороги путник, вперёд и с песней в ТЁМНЫЙ ЛЕС", True, "white")
    screen.blit(text, (0.3 * w + x, 0.4 * h))
    screen.blit(text2, (1.3 * w + x, 0.4 * h))
    screen.blit(text3, (2.3 * w + x, 0.4 * h))
    screen.blit(text4, (3.3 * w + x, 0.4 * h))
    screen.blit(text5, (4.5 * w + x, 0.4 * h))
    screen.blit(text6, (6 * w + x, 0.4 * h))
    screen.blit(text7, (7 * w + x, 0.4 * h))
    screen.blit(text8, (8.5 * w + x, 0.4 * h))
    screen.blit(text9, (10 * w + x, 0.4 * h))
    screen.blit(text10, (11 * w + x, 0.4 * h))
    screen.blit(text11, (12 * w + x, 0.375 * h))
    screen.blit(text12, (12 * w + x, 0.425 * h))
    screen.blit(text13, (13 * w + x, 0.4 * h))
    screen.blit(text14, (14 * w + x, 0.4 * h))
    screen.blit(text15, (15 * w + x, 0.325 * h))
    screen.blit(text16, (15 * w + x, 0.375 * h))
    screen.blit(text17, (15 * w + x, 0.425 * h))
    screen.blit(text18, (16 * w + x, 0.4 * h))
    screen.blit(text19, (17 * w + x, 0.4 * h))
    if not the_first_download:
        Block(2.5 * w + x, 1, w, h, objects)
        Block(3.7 * w + x, 1, w, h, objects)
        Block(3.7 * w + x, 2, w, h, objects)
        Thorns(6.3 * w + x, 1, w, h, thorns)
        Block(8.65 * w + x, 1, w, h, objects)
        StandartEnemy(8.7 * w + x, 0.3 * h, all_enemy, (w, h))
        Block(10.2 * w + x, 1, w, h, objects)
        NoBulletEnemy(10.3 * w + x, 0.5 * h, all_enemy, (w, h))
        NoMovementEnemy(11.3 * w + x, 0.775 * h, all_enemy, (w, h))
        LittleHeal(12.3 * w + x, 0.8 * h, w, h, heals)
        BigHeal(12.4 * w + x, 0.8 * h, w, h, heals)
        fin = pygame.Rect(13.8 * w + x, 0, 0.1 * w, h)
        cut_sheet(pygame.transform.scale(load_image("magic_book.png"), (504, 735)), 6, 7)
        book.image = frames[current_frame]
        book.rect = book.image.get_rect()
        others.add(book)
    if the_first_download:
        book.rect.x = 13.6 * w + x
        book.rect.y = 0.8 * h
        if frame_tick >= 10:
            frame_tick = 0
            current_frame = (current_frame + 1) % 41
            book.image = frames[current_frame]
        else:
            frame_tick += 1
        fin.x = 17.8 * w + x
        if book.rect.colliderect(player):
            book.kill()
    return fin.x < player.x


def cut_sheet(sheet, columns, rows):
    rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                            sheet.get_height() // rows)
    for j in range(rows):
        for i in range(columns):
            frame_location = (rect.w * i, rect.h * j)
            frames.append(sheet.subsurface(pygame.Rect(
                frame_location, rect.size)))



def first_level(screen, w, h, x, objects, thorns, all_enemy, heals, player, others, the_first_download):
    global fin, first_level_frames, portal, current_frame, frames, frame_tick
    if not the_first_download:
        Block(0.7 * w + x, 1, w, h, objects)
        Block(0.8 * w + x, 1, w, h, objects)
        Block(0.8 * w + x, 2, w, h, objects)
        Block(0.9 * w + x, 1, w, h, objects)
        Thorns(0.8 * w + x, 1, w, h, thorns)
        NoBulletEnemy(0.8 * w + x, 0.5 * h, all_enemy, (w, h))
        Block(1.3 * w + x, 1, w, h, objects)
        Block(1.4 * w + x, 1, w, h, objects)
        Block(1.5 * w + x, 1, w, h, objects)
        Thorns(1.55 * w + x, 2, w, h, thorns)
        Thorns(1.6 * w + x, 2, w, h, thorns)
        Thorns(1.65 * w + x, 2, w, h, thorns)
        Block(1.6* w + x, 1, w, h, objects)
        Block(1.7 * w + x, 1, w, h, objects)
        NoMovementEnemy(1.875 * w + x, 0.775 * h, all_enemy, (w, h))
        NoMovementEnemy(1.975 * w + x, 0.775 * h, all_enemy, (w, h))
        Block(2.1 * w + x, 1, w, h, objects)
        Block(2.2 * w + x, 1, w, h, objects)
        Block(2.3 * w + x, 1, w, h, objects)
        Block(2.4 * w + x, 1, w, h, objects)
        Block(2.5 * w + x, 1, w, h, objects)
        StandartEnemy(2.5 * w + x, 0.5 * h, all_enemy, (w, h))
        BigHeal(2.8 * w + x, 0.8 * h, w, h, heals)
        Block(3 * w + x, 1, w, h, objects)
        Block(3.1 * w + x, 1, w, h, objects)
        Block(3.2 * w + x, 2, w, h, objects)
        Block(3.3 * w + x, 2, w, h, objects)
        Block(3.4 * w + x, 2, w, h, objects)
        Block(3.5 * w + x, 1, w, h, objects)
        Block(3.6 * w + x, 1, w, h, objects)
        Block(4.6 * w + x, 1, w, h, objects)
        Block(4.7 * w + x, 1, w, h, objects)
        Block(4.8 * w + x, 1, w, h, objects)
        Block(4.9 * w + x, 1, w, h, objects)
        Block(5 * w + x, 1, w, h, objects)
        Block(5.1 * w + x, 1, w, h, objects)
        Block(5.2 * w + x, 1, w, h, objects)
        Block(5.3 * w + x, 1, w, h, objects)
        NoBulletEnemy(4.8 * w + x, 0.5 * h, all_enemy, (w, h))
        NoBulletEnemy(4.9 * w + x, 0.5 * h, all_enemy, (w, h))
        NoBulletEnemy(5 * w + x, 0.5 * h, all_enemy, (w, h))
        NoBulletEnemy(5.1 * w + x, 0.5 * h, all_enemy, (w, h))
        NoMovementEnemy(5.6 * w + x, 0.775 * h, all_enemy, (w, h))
        Block(6 * w + x, 2, w, h, objects)
        Block(6 * w + x, 1, w, h, objects)
        Block(6.1 * w + x, 2, w, h, objects)
        Block(6.2 * w + x, 2, w, h, objects)
        NoBulletEnemy(6.1 * w + x, 0.2 * h, all_enemy, (w, h))
        Block(6.6 * w + x, 1, w, h, objects)
        StandartEnemy(6.65 * w + x, 0.5 * h, all_enemy, (w, h))
        LittleHeal(7 * w + x, 0.8 * h, w, h, heals)
        NoMovementEnemy(7.5 * w + x, 0.775 * h, all_enemy, (w, h))
        Thorns(7.8 * w + x, 1, w, h, thorns)
        Thorns(7.86 * w + x, 1, w, h, thorns)
        Thorns(7.9 * w + x, 1, w, h, thorns)
        Thorns(7.95 * w + x, 1, w, h, thorns)
        Thorns(8 * w + x, 1, w, h, thorns)
        Thorns(8.05 * w + x, 1, w, h, thorns)
        Thorns(8.6 * w + x, 1, w, h, thorns)
        NoMovementEnemy(8.9 * w + x, 0.775 * h, all_enemy, (w, h))
        Thorns(9.5 * w + x, 1, w, h, thorns)
        Thorns(9.55 * w + x, 1, w, h, thorns)
        Block(9.6 * w + x, 1, w, h, objects)
        Thorns(9.6 * w + x, 1, w, h, thorns)
        Thorns(9.65 * w + x, 1, w, h, thorns)
        Thorns(9.7 * w + x, 1, w, h, thorns)
        Thorns(9.75 * w + x, 1, w, h, thorns)
        BigHeal(10 * w + x, 0.8 * h, w, h, heals)
        fin = pygame.Rect(11.8 * w + x, 0, 0.1 * w, h)
        cut_sheet(pygame.transform.scale(load_image("portal.png"), (2048, 1152)), 8, 3)
        portal.image = frames[current_frame]
        portal.rect = portal.image.get_rect()
        others.add(portal)
        for i in range(1, 7):
            im = f"first_level_screen/MorningLayer{i}.png"
            first_level_frames.append(pygame.transform.scale(load_image(im), (w, h)))
    if the_first_download:
        portal.rect.x = 11.5 * w + x
        portal.rect.y = 0.6 * h
        if frame_tick >= 10:
            frame_tick = 0
            current_frame = (current_frame + 1) % 8
            portal.image = pygame.transform.flip(frames[current_frame], True, False)
        else:
            frame_tick += 1
        fin.x = 11.5 * w + x
        screen.blit(first_level_frames[5], (0, 0))
        for i in range(0, 13):
            screen.blit(first_level_frames[4], (i * w + 0.125 * x, 0))
            screen.blit(first_level_frames[3], (i * w + 0.25 * x, 0))
            screen.blit(first_level_frames[2], (i * w + 0.5 * x, 0))
            screen.blit(first_level_frames[1], (i * w + 0.75 * x, 0))
            screen.blit(first_level_frames[0], (i * w + x, 0))
        font = pygame.font.Font(None, 50)
        text = font.render("О чёрт, я облажался.... Тебе очень повезло, этот портал ведёт в сердце леса", True, "red")
        screen.blit(text, (10.8 * w + x, 0.4 * h))
    return fin.x < player.x


fin = None
book = pygame.sprite.Sprite()
portal = pygame.sprite.Sprite()
frames = []
frame_tick = 0
current_frame = 0
first_level_frames = []
