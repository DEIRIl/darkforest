import pygame


class Player:
    def __init__(self, x, y, radius, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.xspeed = 0
        self.yspeed = 0
        self.v = speed

    def move(self):
        global x
        self.x += self.xspeed
        if x > 0:
            self.y -= 10
            x -= 0.2


pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
w, h = screen.get_size()
running = True
x = 0
circle = Player(0.5 * w - 20, 0.8 * h - 20, 20, 5   )
clock = pygame.time.Clock()
FALL = pygame.USEREVENT + 1
pygame.time.set_timer(FALL, 1)
object = [0.1 * w, 0.6 * h, 0.1 * w, 0.2 * h]
while running:
    screen.fill("black")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                circle.xspeed = circle.v
            if event.key == pygame.K_a:
                circle.xspeed = -circle.v
            if (event.key == pygame.K_w or event.key == pygame.K_SPACE) and x <= 0:
                x = 10
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                circle.xspeed = 0
            if event.key == pygame.K_a:
                circle.xspeed = 0
        if event.type == FALL:
            if object[0] < circle.x < object[0] + object[2]:
                if circle.y < object[1] - circle.radius:
                    circle.y += 1
            elif circle.y < 0.8 * h - circle.radius:
                circle.y += 1
    if circle.x < 0.3 * w:
        circle.x += 5
        object[0] += 5
    if circle.x > 0.7 * w:
        circle.x -= 5
        object[0] -= 5
    if circle.y < 0.3 * h:
        circle.y += 5
        object[1] += 5
    if circle.y > 0.9 * h:
        circle.y -= 5
        object[1] -= 5
    circle.move()
    pygame.draw.rect(screen, "white", (0, 0.8 * h, w, 0.2 * h))
    pygame.draw.rect(screen, "white", object)
    pygame.draw.circle(screen, "red", (circle.x, circle.y), circle.radius)
    pygame.draw.rect(screen, "green", (0.3 * w, 0.3 * h, 0.4 * w, 0.6 * h), 2)
    clock.tick(120)
    pygame.display.flip()
pygame.quit()