import pygame

from libraryImages import load_image


class Player(pygame.sprite.Sprite):
    image1 = load_image("player2.png", -1)
    image2 = pygame.transform.flip(image1, True, False)

    def __init__(self, x, y, radius, speed, all_sprites, size, screen):
        super().__init__(all_sprites)
        self.radius = radius
        self.image = pygame.transform.scale(Player.image1, (radius, 1.5 * radius))
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
        self.jump_max = 20
        self.jump_count = 0
        self.max_hp = 100
        self.hp = 100
        self.sc = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen = screen

    def show_hp(self):
        pygame.draw.rect(self.sc, "grey", (28, self.screen_size[1] - 77, 304, 34))
        pygame.draw.rect(self.sc, "green", (30, self.screen_size[1] - 75, 3 * self.hp, 30))
        pygame.draw.rect(self.sc, "red", (30 + 3 * self.hp, self.screen_size[1] - 75, 3 * (self.max_hp - self.hp), 30))
        self.screen.blit(self.sc, (0, 0))

    def death(self):
        pass


    def update(self, jump, fall, objects, floor):
        if self.x1motoin == "y" and self.x2motoin == "y":
            self.vx = 0
        elif self.x1motoin == "y":
            self.vx = self.v
            self.image = pygame.transform.scale(Player.image1, (self.radius, 1.5 * self.radius))
        elif self.x2motoin == "y":
            self.vx = -self.v
            self.image = pygame.transform.scale(Player.image2, (self.radius, 1.5 * self.radius))
        else:
            self.vx = 0
        if jump:
            self.vy = -self.jump_count
            if self.jump_count > 0 and not pygame.sprite.spritecollideany(self,
                                                                          floor) and not pygame.sprite.spritecollideany(
                    self, objects):
                self.jump_count -= 1
            elif not pygame.sprite.spritecollideany(self, floor) and not pygame.sprite.spritecollideany(self, objects):
                jump = False
            elif pygame.sprite.spritecollideany(self, floor) and pygame.sprite.spritecollideany(self, objects):
                jump = False
                self.jump_count = 0
                self.vy = 0
        elif fall and self.jump_count <= 0:
            if not pygame.sprite.spritecollideany(self, floor) and pygame.sprite.spritecollideany(self, objects):
                self.jump_count -= 2
                self.vy = -self.jump_count
            elif not pygame.sprite.spritecollideany(self, floor) and not pygame.sprite.spritecollideany(self, objects):
                fall = False
                self.vy = -self.jump_count
                self.jump_count = self.vy
            elif pygame.sprite.spritecollideany(self, floor):
                fall = False
                self.vy = 0
        else:
            self.jump = False
            fall = False
            self.vy = self.jump_count if self.jump_count != 0 else self.vy
            self.jump_count += 1
            if pygame.sprite.spritecollideany(self, floor) or pygame.sprite.spritecollideany(self, objects):
                self.vy = 0
                self.jump_count = 0
        self.rect = self.rect.move(self.vx, self.vy)
        # print(jump, fall, self.jump_count)
        if self.hp == 0:
            self.death()
        return (jump, fall)
