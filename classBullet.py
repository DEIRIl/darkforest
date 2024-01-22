import pygame

from libraryImages import load_image
from math import atan2, pi


class Arrow(pygame.sprite.Sprite):
    image = load_image('arrow.png')

    def __init__(self, x, y, w, h, group, speed):
        super().__init__(group)
        self.speed = speed
        self.image = pygame.transform.scale(Arrow.image, (0.035 * w, 0.05 * h))
        if speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(x, y)
        self.minus_hp = 15

    def update(self, motion, speed):
        if motion == "r":
            self.rect = self.rect.move(speed, 0)
        elif motion == "l":
            self.rect = self.rect.move(-speed, 0)
        self.rect.x += self.speed


class Branch(pygame.sprite.Sprite):
    image = load_image("branch.png")

    def __init__(self, x, y, w, h, group, target):
        super().__init__(group)
        self.x_speed = (target[0] - x) / 60
        self.y_speed = (target[1] - y) / 60
        self.size = (w, h)
        angle = atan2(self.y_speed, self.x_speed) * (180 / pi)
        if self.x_speed < 0:
            angle += 180
        else:
            angle = abs(angle)
        self.image = pygame.transform.rotate(pygame.transform.scale(Branch.image, (0.07 * w, 0.08 * h)), angle)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(x, y)
        self.minus_hp = 25
        self.time = 11


    def update(self, motion, speed):
        if motion == "r":
            self.rect = self.rect.move(speed, 0)
        elif motion == "l":
            self.rect = self.rect.move(-speed, 0)
        if self.time % 60 == 0:
            self.rect.x += self.x_speed
            self.rect.y += self.y_speed
        else:
            self.time += 1
        if self.time >= 601:
            self.kill()
