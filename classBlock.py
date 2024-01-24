import pygame

from libraryImages import load_image


class Block(pygame.sprite.Sprite):
    image = load_image('block3.png')

    def __init__(self, x, coord, w, h, group):
        super().__init__(group)
        coords = {1: 0.6 * h, 2: 0.25 * h}
        self.image = pygame.transform.scale(Block.image, (0.15 * w, 0.08 * h))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(x, coords[coord])
        self.rect.h = 10
         # self.rect = pygame.Rect((x, coords[coord]), (0.1 * w, 1))

    def update(self, motion, speed):
        if motion == "r":
            self.rect = self.rect.move(speed, 0)
        elif motion == "l":
            self.rect = self.rect.move(-speed, 0)
