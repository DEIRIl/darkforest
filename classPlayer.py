import pygame

from libraryImages import load_image
from classBullet import Flame


class Player(pygame.sprite.Sprite):
    # image = pygame.transform.scale(load_image("Idle.png"), (600, 150))
    # image1 = pygame.transform.scale(load_image("Jump.png"), (1100, 150))
    # image2 = pygame.transform.scale(load_image("Run.png"), (800, 150))
    # attack_image = pygame.transform.scale(load_image("Attack_3.png"), (1792, 150))

    def __init__(self, x, y, all_sprites, size, screen):
        image = pygame.transform.scale(load_image("Idle.png"), (0.6 * size[1], 0.15 * size[1]))
        image1 = pygame.transform.scale(load_image("Jump.png"), (1.1 * size[1], 0.15 * size[1]))
        image2 = pygame.transform.scale(load_image("Run.png"), (0.8 * size[1], 0.15 * size[1]))
        attack_image = pygame.transform.scale(load_image("Attack_3.png"), (1.8 * size[1], 0.15 * size[1]))
        super().__init__(all_sprites)
        self.frames = []
        self.frame_tick = 20
        self.frame_tick_idle = 0
        self.cut_sheet(image, 6, 1)
        self.cut_sheet(image1, 11, 1)
        self.cut_sheet(image2, 8, 1)
        self.cut_sheet(attack_image, 7, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.cur_frame_idle = 1
        self.radius = radius = 0.07 * size[1]
        self.rect = self.image.get_rect().move(x, y)
        self.mask = pygame.mask.from_surface(self.image)
        self.x1motoin = "n"
        self.x2motoin = "n"
        self.vx = 0
        self.vy = 5
        self.v = 10
        self.x = x
        self.y = y
        self.screen_size = size
        self.jump_max = 22
        self.jump_count = 0
        self.max_hp = 100
        self.hp = 100
        self.sc = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen = screen
        self.running = True
        self.attack = 12
        self.attack_time = 5
        self.curr_attack_frame = 0
        self.leftdv = False
        self.one_damage = False
        self.have_damage_tick = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def show_hp(self):
        pygame.draw.rect(self.sc, "gray", (
            0.0145 * self.screen_size[0], self.screen_size[1] - 0.0712 * self.screen_size[1],
            3.04 * self.max_hp,
            0.0315 * self.screen_size[1]))
        pygame.draw.rect(self.sc, "red", (
            0.0152 * self.screen_size[0], self.screen_size[1] - 0.06929 * self.screen_size[1], 3 * self.hp,
            0.015625 * self.screen_size[0]))
        pygame.draw.rect(self.sc, "black", (
            0.0152 * self.screen_size[0] + 3 * self.hp, self.screen_size[1] - 0.06929 * self.screen_size[1],
            3 * (self.max_hp - self.hp), 0.015625 * self.screen_size[0]))
        self.screen.blit(self.sc, (0, 0))

    def death(self):
        self.running = False

    def rest(self):
        self.rect.x = self.x
        self.rect.y = self.y
        self.x1motoin = "n"
        self.x2motoin = "n"
        self.vx = 0
        self.vy = 5
        self.v = 10
        self.jump_max = 22
        self.jump_count = 0
        self.max_hp = 100
        self.hp = 100
        self.sc = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.running = True
        self.attack = 12
        self.attack_time = 5
        self.curr_attack_frame = 0
        self.leftdv = False
        self.one_damage = False
        self.have_damage_tick = 0
        self.running = True


    def upd(self, jump, fall, objects, thorns, floor, bullets, heals, attack, enemys, player_bullets):
        a = False
        if attack:
            self.vx = 0
            if self.attack_time % 5 == 0:
                self.attack_time += 1
                self.cur_frame = (self.cur_frame + 1) % 7
                if self.leftdv and self.attack_time <= 2:
                    self.rect.x += 106
                self.image = pygame.transform.flip(self.frames[self.cur_frame + 25], self.leftdv, False)
            elif self.attack_time < 35:
                self.attack_time += 1
            else:
                Flame(self.rect.x + self.rect.w // 2, self.rect.y + self.rect.h // 2, *self.screen_size, player_bullets, self.attack, self.leftdv)
                self.attack_time = 0
                attack = False
                self.one_damage = False
            if pygame.sprite.spritecollideany(self, enemys) and not self.one_damage:
                self.one_damage = True
                for enemy in enemys:
                    if self.rect.colliderect(enemy):
                        enemy.hp -= self.attack
                        if enemy.hp <= 0:
                            enemy.kill()
        elif self.x1motoin == "y" and self.x2motoin == "y":
            self.vx = 0
        elif self.x1motoin == "y":
            self.leftdv = False
            self.frame_tick_idle = 10
            self.frame_tick += 1
            self.vx = self.v
            if self.frame_tick >= 10:
                if not jump:
                    self.cur_frame = (self.cur_frame + 1) % 8
                    self.image = self.frames[self.cur_frame + 17]
                else:
                    self.cur_frame = (self.cur_frame + 1) % 11
                    self.image = self.frames[self.cur_frame + 6]
                self.frame_tick = 0
        elif self.x2motoin == "y":
            self.leftdv = True
            self.frame_tick_idle = 10
            self.frame_tick += 1
            self.vx = -self.v
            if self.frame_tick >= 10:
                if not jump:
                    self.cur_frame = (self.cur_frame + 1) % 8
                    self.image = pygame.transform.flip(self.frames[self.cur_frame + 17], True, False)
                else:
                    self.cur_frame = (self.cur_frame + 1) % 11
                    self.image = pygame.transform.flip(self.frames[self.cur_frame + 6], True, False)
                self.frame_tick = 0
        else:
            self.vx = 0
            self.cur_frame = 0
            if self.frame_tick_idle >= 10:
                self.cur_frame_idle = (self.cur_frame_idle + 1) % 6
                self.frame_tick_idle = 0
            else:
                self.frame_tick_idle += 1
            self.image = pygame.transform.flip(self.frames[self.cur_frame_idle], self.leftdv, False)
            self.frame_tick = 10
        if jump:
            self.vy = -self.jump_count
            if self.jump_count > 0 and not pygame.sprite.spritecollideany(self,
                                                                          floor) and not pygame.sprite.spritecollideany(
                self, objects):
                self.jump_count -= 1
            elif not pygame.sprite.spritecollideany(self, floor) and not pygame.sprite.spritecollideany(self, objects):
                jump = False
            elif pygame.sprite.spritecollideany(self, floor) and pygame.sprite.spritecollideany(self, objects):
                jump = False
                self.jump_count = 0
                self.vy = 0
        elif fall and self.jump_count <= 0:
            if not pygame.sprite.spritecollideany(self, floor) and pygame.sprite.spritecollideany(self, objects):
                self.jump_count -= 2
                self.vy = -self.jump_count
            elif not pygame.sprite.spritecollideany(self, floor) and not pygame.sprite.spritecollideany(self, objects):
                fall = False
                self.vy = -self.jump_count
                self.jump_count = self.vy
            elif pygame.sprite.spritecollideany(self, floor):
                fall = False
                self.vy = 0
        else:
            self.jump = False
            fall = False
            self.vy = self.jump_count if self.jump_count != 0 else self.vy
            self.jump_count += 1
            if pygame.sprite.spritecollideany(self, floor) or pygame.sprite.spritecollideany(self, objects):
                self.vy = 0
                self.jump_count = 0
        if pygame.sprite.spritecollideany(self, thorns) and not a:
            for thorn in thorns:
                if self.rect.colliderect(thorn.rect):
                    if thorn.rect.x + thorn.rect.w // 2 <= self.rect.x + self.rect.w // 2:
                        self.rect.x += 50
                        self.rect.y -= 40
                        self.vx = 0
                    elif thorn.rect.x + thorn.rect.w // 2 > self.rect.x + self.rect.w // 2:
                        self.rect.x -= 50
                        self.rect.y -= 40
                        self.vx = 0
                #     if self.x1motoin == "y":
                #         self.rect = self.rect.move(-self.v * 23, -self.v * 5)
                #     if self.x2motoin == "y":
                #         self.rect = self.rect.move(self.v * 23, -self.v * 5)
                #     if self.x1motoin != "y" and self.x2motoin != "y":
                #         self.rect = self.rect.move(-self.v * 23, -self.v * 5)
                # if fall:
                #     self.rect = self.rect.move(self.v * 15, 0)
                if self.have_damage_tick >= 10:
                    self.hp -= 5
                    self.have_damage_tick = 0
                a = True
        if pygame.sprite.spritecollideany(self, bullets):
            for bullet in bullets:
                if self.rect.colliderect(bullet.rect):
                    if self.have_damage_tick >= 10:
                        self.hp -= bullet.minus_hp
                        self.have_damage_tick = 0
                    bullet.kill()
        if pygame.sprite.spritecollideany(self, heals):
            for heal in heals:
                if self.rect.colliderect(heal.rect):
                    self.hp += heal.plus_hp
                    if self.hp >= 100:
                        self.hp = 100
                    heal.kill()
        if not a:
            self.rect = self.rect.move(self.vx, self.vy)
        if self.hp <= 0:
            self.death()
            self.hp = 100
        self.have_damage_tick += 1
        return (jump, fall, attack)
