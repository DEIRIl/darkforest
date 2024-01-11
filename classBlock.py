import pygame

from libraryImages import load_image

class Block(pygame.sprite.Sprite):
    image = load_image('block2.png')
    def __init__(self,x, coord, w, h, group):
        super().__init__(group)
        coords = {1: 0.6 * h, 2: 0.25 * h}
        self.image = pygame.transform.scale(Block.image, (0.15 * w, 0.08 * h))
        self.mask = pygame.mask.from_surface(self.image)
        self.rectt = self.image.get_rect().move(x, coords[coord])
        self.rect = pygame.Rect((x, coords[coord]), (0.15 * w, 1))

    def update(self, motion, speed):
        if motion == "r":
            self.rect = self.rect.move(speed, 0)
        else:
            self.rect = self.rect.move(-speed, 0)
