import pygame

from libraryImages import load_image

class Enemy(pygame.sprite.Sprite):
    image = load_image("enemy.png")

    def __init__(self, x, y, group):
        super().__init__(group)
        self.image = pygame.transform.scale(Enemy.image, (100, 150))
        self.rect = self.image.get_rect().move(x, y)
        self.mask = pygame.mask.from_surface(self.image)
        self.vx = 0
        self.vy = 5
        self.v = 5

    def update(self, floor, objects, motion):
        if motion == "r":
            self.rect = self.rect.move(5, 0)
        elif motion == "l":
            self.rect = self.rect.move(-5, 0)
        # self.rect.x += self.vx
        self.rect.y += self.vy
        if pygame.sprite.spritecollideany(self, floor) or pygame.sprite.spritecollideany(self, objects):
            self.vy = 0
            self.jump_count = 0
