import pygame

from classBlock import Block
from classEnemy import StandartEnemy, NoBulletEnemy, NoMovementEnemy
from classHeal import LittleHeal, BigHeal
from classThorns import Thorns


def training_level(screen, w, h, x, objects, thorns, all_enemy, heals, player):
    global the_first_download, fin
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
    text13 = font.render("А теперь удачной дороги путник, вперёд и с песней в ТЁМНЫЙ ЛЕС", True, "white")
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
    if not the_first_download:
        the_first_download = True
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
    if the_first_download:
        fin.x = 13.8 * w + x
    return fin.x < player.x


the_first_download = False
fin = None