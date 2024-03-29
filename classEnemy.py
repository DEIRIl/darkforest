import pygame

from libraryImages import load_image
from classBullet import Arrow, Branch


class StandartEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, group, size, im=None):
        super().__init__(group)
        self.frames1 = []
        self.cur_frame1 = 0
        if im is None:
            image1 = pygame.transform.scale(load_image("Walk_skeleton.png"), (0.3 * size[0], 0.3 * size[1]))
            image2 = pygame.transform.scale(load_image("Shot_skeleton.png"), (0.4 * size[0], 0.6 * size[1]))
            self.cut_sheet(image1, 4, 2)
            self.cut_sheet(image2, 4, 4)
            self.image = pygame.surface.Surface((0.06 * size[0], 0.16 * size[1]))
            self.image.blit(pygame.transform.scale(self.frames1[self.cur_frame1], (0.06 * size[0], 0.13 * size[1])),
                            (0, 0.03 * size[1]))
            self.mask = pygame.mask.from_surface(
                pygame.transform.scale(self.frames1[self.cur_frame1], (0.06 * size[0], 0.13 * size[1])))
        else:
            self.image = pygame.surface.Surface((im[1][0], im[1][1] + 0.03 * size[1]))
            self.image.blit(pygame.transform.scale(im[0], im[1]), (0, 0.03 * size[1]))
            self.mask = pygame.mask.from_surface(im[0])
        self.rect = self.image.get_rect().move(x, y)
        self.vx = 2
        self.vy = 5
        self.v = 5
        self.time = 0
        self.Ttime = 170
        self.frame_tick = 0
        self.frame_tick_walk = 0
        self.size = size
        self.hp = 100

    def show_hp(self):
        pygame.draw.rect(self.image, "black", (0, 0.01 * self.size[1], self.rect.w, 0.01 * self.size[1]))
        pygame.draw.rect(self.image, "red", (0, 0.01 * self.size[1], self.rect.w * self.hp / 100, 0.01 * self.size[1]))

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames1.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, floor, objects, motion, player, bullets, player_bullets):
        self.show_hp()
        if pygame.sprite.spritecollideany(self, player_bullets):
            for bullet in player_bullets:
                if self.rect.colliderect(bullet):
                    self.hp -= bullet.minus_hp
                    bullet.kill()
                    if self.hp <= 0:
                        self.kill()
        if motion == "r":
            self.rect = self.rect.move(player.v, 0)
        elif motion == "l":
            self.rect = self.rect.move(-player.v, 0)
        self.rect.y += self.vy
        if pygame.sprite.spritecollideany(self, objects) or pygame.sprite.spritecollideany(self, floor):
            if ((self.rect.x - player.rect.x) ** 2 + (self.rect.y - player.rect.y) ** 2) ** 0.5 <= 0.3 * self.size[0]:
                self.frame_tick += 1
                if self.frame_tick >= 10 and self.Ttime <= 170:
                    self.cur_frame1 = (self.cur_frame1 + 1) % 15
                    if self.rect.x > player.x:
                        self.image = pygame.transform.flip(self.frames1[self.cur_frame1 + 8], True, False)
                    else:
                        self.image = self.frames1[self.cur_frame1 + 8]
                    self.frame_tick = 0
                if self.Ttime >= 170:
                    self.cur_frame1 = 0
                    self.Ttime = 0
                    if player.rect.x > self.rect.x:
                        Arrow(self.rect.x, self.rect.y * 1.1, *self.size, bullets, 15)
                    else:
                        Arrow(self.rect.x, self.rect.y * 1.1, *self.size, bullets, -15)
                else:
                    self.Ttime += 1
                self.vy = 0
            else:
                self.Ttime = 200
                self.vy = 0
                self.rect.x += self.vx
                self.frame_tick_walk += 1
                if self.frame_tick_walk >= 10:
                    self.cur_frame1 = (self.cur_frame1 + 1) % 8
                    self.image = self.frames1[self.cur_frame1]
                    self.frame_tick_walk = 0
        else:
            if ((self.rect.x - player.rect.x) ** 2 + (self.rect.y - player.rect.y) ** 2) ** 0.5 <= 0.3 * self.size[0]:
                if self.Ttime >= 200:
                    self.Ttime = 0
                    if player.rect.x > self.rect.x:
                        Arrow(self.rect.x, self.rect.y * 1.1, *self.size, bullets, 15)
                    else:
                        Arrow(self.rect.x, self.rect.y * 1.1, *self.size, bullets, -15)
                else:
                    self.Ttime += 1
            else:
                self.Ttime = 200
                self.frame_tick_walk += 1
                if self.frame_tick_walk >= 10:
                    self.cur_frame1 = (self.cur_frame1 + 1) % 8
                    self.image = pygame.transform.flip(self.frames1[self.cur_frame1], True, False)
                    self.frame_tick_walk = 0
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
        self.hit_time = 0
        super().__init__(x, y, group, size, (self.frames[self.cur_frame], (0.055 * size[0], 0.06 * size[1])))

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, floor, objects, motion, player, bullets, player_bullets):
        self.show_hp()
        if pygame.sprite.spritecollideany(self, player_bullets):
            for bullet in player_bullets:
                if self.rect.colliderect(bullet):
                    self.hp -= bullet.minus_hp
                    bullet.kill()
                    if self.hp <= 0:
                        self.kill()
        if motion == "r":
            self.rect = self.rect.move(player.v, 0)
        elif motion == "l":
            self.rect = self.rect.move(-player.v, 0)
        self.rect.y += self.vy
        if self.rect.colliderect(player) and self.hit_time >= 50:
            player.hp -= 5
            self.hit_time = 0
        else:
            self.hit_time += 1
        if self.stop:
            self.cur_frame = 16
        elif self.vx <= 0:
            self.cur_frame = 0
        elif self.vx >= 0:
            self.cur_frame = 8
        self.image = self.frames[self.cur_frame]
        if pygame.sprite.spritecollideany(self, objects) or pygame.sprite.spritecollideany(self, floor):
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
    def __init__(self, x, y, group, size):
        image1 = pygame.transform.scale(load_image("enemy_tree_idle.png"), (0.18 * size[0], 0.2 * size[1]))
        image2 = pygame.transform.scale(load_image("enemy_tree_attack.png"), (0.5 * size[0], 0.1 * size[1]))
        image3 = pygame.transform.scale(load_image("enemy_tree_waiting.png"), (0.4 * size[0], 0.4 * size[1]))
        self.frames = []
        self.frame_tick = 20
        self.cut_sheet(image1, 2, 2)
        self.cut_sheet(image2, 5, 1)
        self.cut_sheet(image3, 4, 4)
        self.cur_frame = 0
        self.frame_tick_idle = 0
        self.frame_tick_waiting = 0
        self.Ttime = 300
        self.stop = False
        super().__init__(x, y, group, size,
                         (pygame.transform.flip(self.frames[self.cur_frame], True, False),
                          (0.1 * size[0], 0.1 * size[1])))

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, floor, objects, motion, player, bullets, player_bullets):
        self.show_hp()
        if pygame.sprite.spritecollideany(self, player_bullets):
            for bullet in player_bullets:
                if self.rect.colliderect(bullet):
                    self.hp -= bullet.minus_hp
                    bullet.kill()
                    if self.hp <= 0:
                        self.kill()
        if motion == "r":
            self.rect = self.rect.move(player.v, 0)
        elif motion == "l":
            self.rect = self.rect.move(-player.v, 0)
        self.rect.y += self.vy
        if pygame.sprite.spritecollideany(self, floor):
            if ((self.rect.x - player.x) ** 2 + (self.rect.y - player.y) ** 2) ** 0.5 <= 0.4 * self.size[0]:
                self.frame_tick_idle = 10
                self.frame_tick += 1
                self.vx = self.v
                if self.frame_tick >= 10 and self.Ttime <= 60:
                    self.cur_frame = (self.cur_frame + 1) % 5
                    if self.rect.x > player.x:
                        self.image = pygame.transform.flip(self.frames[self.cur_frame + 4], True, False)
                    else:
                        self.image = self.frames[self.cur_frame + 4]
                    self.frame_tick = 0
                else:
                    self.frame_tick_waiting += 1
                    self.vx = self.v
                    if self.frame_tick_waiting >= 10 and self.Ttime > 60:
                        self.cur_frame = (self.cur_frame + 1) % 16
                        if self.rect.x > player.x:
                            self.image = pygame.transform.flip(self.frames[self.cur_frame + 9], True, False)
                        else:
                            self.image = self.frames[self.cur_frame + 9]
                        self.frame_tick_waiting = 0
                if self.Ttime >= 300:
                    self.Ttime = 0
                    self.cur_frame = 4
                    Branch(self.rect.x, self.rect.y, *self.size, bullets,
                           (player.rect.x + player.rect.w // 2, player.rect.y))
                else:
                    self.Ttime += 1
                self.vy = 0
            else:
                self.frame_tick_idle += 1
                self.vx = self.v
                if self.frame_tick_idle >= 20:
                    self.cur_frame = (self.cur_frame + 1) % 4
                    self.image = pygame.transform.flip(self.frames[self.cur_frame], True, False)
                    self.frame_tick_idle = 0
                self.Ttime = 300
                self.vy = 0
