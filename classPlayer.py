import pygame

from libraryImages import load_image


class Player(pygame.sprite.Sprite):
    image1 = load_image("player.png")
    image2 = pygame.transform.flip(image1, True, False)
    def __init__(self, x, y, radius, speed, all_sprites, size):
        super().__init__(all_sprites)
        self.radius = radius
        self.image = pygame.transform.scale(Player.image1, (0.75 * radius, 1.75 * radius))
        self.rect = self.image.get_rect().move(x, y)
        self.mask = pygame.mask.from_surface(self.image)
        self.x1motoin = "n"
        self.x2motoin = "n"
        self.vx = 0
        self.vy = speed
        self.v = speed
        self.x = x
        self.y = y
        self.screen_size = size
        self.jump = False
        self.xx = 0

    def update(self, objects, floor):
        if self.x1motoin == "y" and self.x2motoin == "y":
            self.vx = 0
        elif self.x1motoin == "y":
            self.vx = self.v
            self.image = pygame.transform.scale(Player.image1, (0.75 * self.radius, 1.75 * self.radius))
        elif self.x2motoin == "y":
            self.vx = -self.v
            self.image = pygame.transform.scale(Player.image2, (0.75 * self.radius, 1.75 * self.radius))
        else:
            self.vx = 0
        if self.jump:
            self.xx = 30
            self.jump = False
        if self.xx == 0:
            self.vy = self.v
        elif self.xx != 0:
            self.vy = -self.v
            self.xx -= 1
        if pygame.sprite.spritecollideany(self, floor):
            self.vy -= self.v
        # if self.xx == 0 and pygame.sprite.spritecollideany(self, objects):
        #     self.vy -= self.v
        if pygame.sprite.spritecollideany(self, objects):
            self.xx = 0
            # self.vy -= self.v
        self.rect = self.rect.move(self.vx, self.vy)
