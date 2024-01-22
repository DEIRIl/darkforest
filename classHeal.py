import pygame

from libraryImages import load_image

class LittleHeal(pygame.sprite.Sprite):
    image = load_image('heal.png')
    def __init__(self, x, y, w, h, group, im=None):
        super().__init__(group)
        if im is None:
            self.image = pygame.transform.scale(LittleHeal.image, (0.03645 * w, 0.06481 * h))
        else:
            self.image = pygame.transform.scale(im, (0.03645 * w, 0.06481 * h))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(x, y)
        self.plus_hp = 20

    def update(self, motion, speed):
        if motion == "r":
            self.rect = self.rect.move(speed, 0)
        elif motion == "l":
            self.rect = self.rect.move(-speed, 0)


class BigHeal(LittleHeal):
    image = load_image("big_heal.png")
    def __init__(self, x, y, w, h, group):
        super().__init__(x, y, w, h, group, BigHeal.image)
        self.plus_hp = 50

