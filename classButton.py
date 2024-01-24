import pygame


from libraryImages import load_image

class Button():
    def __init__(self, x, y, width, height, buttonText, onclickFunction, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onePress = onePress
        self.alreadyPressed = False
        self.onclickFunction = onclickFunction

        self.fillColors = {
            'hover': pygame.transform.scale(load_image("floor_button.png"), (width, height)),
            'normal': pygame.transform.scale(load_image("floor_button1.png"), (width, height)),
            'pressed': pygame.transform.scale(load_image("floor_button2.png"), (width, height)),
        }
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, (255, 255, 255))
        obj.append(self)


    def process(self, screen):
        mousePos = pygame.mouse.get_pos()
        # self.buttonSurface.fill(self.fillColors['normal'])
        screen.blit(self.fillColors['normal'], (self.x, self.y))
        if self.buttonRect.collidepoint(mousePos):
            # self.buttonSurface.fill(self.fillColors['hover'])
            screen.blit(self.fillColors['hover'], (self.x, self.y))
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                screen.blit(self.fillColors['pressed'], (self.x, self.y))
                # self.buttonSurface.fill(self.fillColors['pressed'])
                if self.onePress:
                    self.onclickFunction()
                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False
        screen.blit(self.buttonSurf, [self.x +
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2, self.y +
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])
        # screen.blit(self.buttonSurface, self.buttonRect)


font = pygame.font.SysFont('Arial', 40)

obj = []
