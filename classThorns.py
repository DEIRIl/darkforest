import pygame

from libraryImages import load_image


class Thorns(pygame.sprite.Sprite):
    image = load_image('thorns2.png')

    def __init__(self, x, coord, w, h, group):
        super().__init__(group)
        coords = {1: 0.821 * h, 2: 0.53 * h, 3: 0.2 * h}
        self.image = pygame.transform.scale(Thorns.image, (0.07 * w, 0.08 * h))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(x, coords[coord])

    def update(self, motion, speed):
        if motion == "r":
            self.rect = self.rect.move(speed, 0)
        elif motion == "l":
            self.rect = self.rect.move(-speed, 0)
