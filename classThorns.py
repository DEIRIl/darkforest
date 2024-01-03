import pygame

from libraryImages import load_image

class Thorns(pygame.sprite.Sprite):
    image = load_image('thorns.png')
    def __init__(self, x, coord, w, h, group):
        super().__init__(group)
        coords = {1: 0.86 * h, 2: 0.46 * h}
        self.image = pygame.transform.scale(Thorns.image, (0.03 * w, 0.04 * h))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(x, coords[coord])

    def update(self, motion, speed):
        if motion == "r":
            self.rect = self.rect.move(speed, 0)
        else:
            self.rect = self.rect.move(-speed, 0)