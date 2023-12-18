import pygame

class Branch(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, group):
        super().__init__(group)
        self.image = pygame.Surface((w, h), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, pygame.Color("white"), (0, 0, w, h))
        self.rect = pygame.Rect(x, y, w, h)

    def update(self, motion, speed):
        if motion == "r":
            self.rect = self.rect.move(speed, 0)
        else:
            self.rect = self.rect.move(-speed, 0)