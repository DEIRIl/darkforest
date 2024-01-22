import pygame

from libraryImages import load_image
from classBullet import Arrow, Branch


class StandartEnemy(pygame.sprite.Sprite):
    image = load_image("player41.png")

    def __init__(self, x, y, group, size, im=None):
        super().__init__(group)
        self.radius = radius = 0.07 * size[1]
        if im is None:
            self.image = pygame.transform.scale(StandartEnemy.image, (radius, 2.1 * radius))
        else:
            self.image = pygame.transform.scale(im[0], im[1])
        self.rect = self.image.get_rect().move(x, y)
        self.mask = pygame.mask.from_surface(self.image)
        self.vx = 2
        self.vy = 5
        self.v = 5
        self.time = 0
        self.Ttime = 200
        self.size = size

    def update(self, floor, objects, motion, player, bullets):
        if motion == "r":
            self.rect = self.rect.move(player.v, 0)
        elif motion == "l":
            self.rect = self.rect.move(-player.v, 0)
        self.rect.y += self.vy
        if pygame.sprite.spritecollideany(self, objects):
            if ((self.rect.x - player.rect.x) ** 2 + (self.rect.y - player.rect.y) ** 2) ** 0.5 <= 0.3 * self.size[0]:
                if self.Ttime >= 200:
                    self.Ttime = 0
                    if player.rect.x > self.rect.x:
                        Arrow(self.rect.x, self.rect.y, *self.size, bullets, 15)
                    else:
                        Arrow(self.rect.x, self.rect.y, *self.size, bullets, -15)
                else:
                    self.Ttime += 1
            else:
                self.Ttime = 200
                self.rect.x += self.vx
            self.vy = 0
        else:
            if ((self.rect.x - player.rect.x) ** 2 + (self.rect.y - player.rect.y) ** 2) ** 0.5 <= 0.3 * self.size[0]:
                if self.Ttime >= 200:
                    self.Ttime = 0
                    if player.rect.x > self.rect.x:
                        Arrow(self.rect.x, self.rect.y, *self.size, bullets, 15)
                    else:
                        Arrow(self.rect.x, self.rect.y, *self.size, bullets, -15)
                else:
                    self.Ttime += 1
            else:
                self.Ttime = 200
                if self.time >= 100:
                    self.vx = -self.vx
                    self.rect.x += self.vx
                    self.time = 0
                else:
                    self.time += 1


class NoBulletEnemy(StandartEnemy):
    image = load_image("enemy_slime.png")

    def __init__(self, x, y, group, size):
        self.frames = []
        self.frame_tick = 20
        self.cut_sheet(NoBulletEnemy.image, 8, 3)
        self.cur_frame = 16
        self.stop = False
        super().__init__(x, y, group, size, (self.frames[self.cur_frame], (0.055 * size[0], 0.06 * size[1])))

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, floor, objects, motion, player, bullets):
        if motion == "r":
            self.rect = self.rect.move(player.v, 0)
        elif motion == "l":
            self.rect = self.rect.move(-player.v, 0)
        self.rect.y += self.vy
        if self.stop:
            self.cur_frame = 16
        elif self.vx <= 0:
            self.cur_frame = 0
        elif self.vx >= 0:
            self.cur_frame = 8
        self.image = self.frames[self.cur_frame]
        if pygame.sprite.spritecollideany(self, objects):
            self.vy = 0
            self.rect.x += self.vx
            self.stop = False
        else:
            if self.time >= 200:
                self.vx = -self.vx
                self.rect.x += self.vx
                self.time = 0
                self.stop = False
            else:
                self.time += 1
                self.stop = True


class NoMovementEnemy(StandartEnemy):
    image = load_image("enemy_ent.png")

    def __init__(self, x, y, group, size):
        self.frames = []
        self.frame_tick = 20
        self.cut_sheet(NoMovementEnemy.image, 8, 3)
        self.cur_frame = 16
        self.stop = False
        super().__init__(x, y, group, size, (NoMovementEnemy.image, (0.075 * size[0], 0.15 * size[1])))

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, floor, objects, motion, player, bullets):
        if motion == "r":
            self.rect = self.rect.move(player.v, 0)
        elif motion == "l":
            self.rect = self.rect.move(-player.v, 0)
        self.rect.y += self.vy
        if pygame.sprite.spritecollideany(self, floor):
            if ((self.rect.x - player.x) ** 2 + (self.rect.y - player.y) ** 2) ** 0.5 <= 0.4 * self.size[0]:
                if self.Ttime >= 200:
                    self.Ttime = 0
                    Branch(self.rect.x, self.rect.y, *self.size, bullets, (player.rect.x, player.rect.y))
                else:
                    self.Ttime += 1
            else:
                self.Ttime = 200
            self.vy = 0
