import pygame

from libraryImages import load_image


class LittleHeal(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, group, size=0):
        super().__init__(group)
        sizes = ((0.05 * w, 0.05 * h), (0.08 * w, 0.08 * h))
        self.image = load_image('Heal_heart.png')
        self.frames = []
        self.cut_sheet(self.image, 5, 1, sizes[size])
        self.cur_frame = 0
        self.frame_tick = 0
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(x, y)
        self.plus_hp = 20


    def cut_sheet(self, sheet, columns, rows, size):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(pygame.transform.scale(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)), size))

    def update(self, motion, speed):
        if motion == "r":
            self.rect = self.rect.move(speed, 0)
        elif motion == "l":
            self.rect = self.rect.move(-speed, 0)
        self.frame_tick += 1
        if self.frame_tick >= 10:
            self.cur_frame = (self.cur_frame + 1) % 5
            self.image = self.frames[self.cur_frame]
            self.frame_tick = 0


class BigHeal(LittleHeal):
    def __init__(self, x, y, w, h, group):
        super().__init__(x, y, w, h, group, 1)
        self.plus_hp = 50
