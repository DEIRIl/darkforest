import pygame

class MainFloor(pygame.sprite.Sprite):
    def __init__(self, size, group):
        super().__init__(group)
        self.image = pygame.Surface((size[0], 0.1 * size[1]), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, pygame.Color("white"), (0, 0, size[0], size[1]))
        self.rect = pygame.Rect(0, 0.9 * size[1], size[0], size[1])
