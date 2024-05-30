import pygame



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("F_crash-p_car.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (400, 500)  
        self.lives = 3  

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 98:
            self.rect.x -= 10
        if keys[pygame.K_RIGHT] and self.rect.right < 715:
            self.rect.x += 10
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= 5
        if keys[pygame.K_DOWN] and self.rect.bottom < 600:
            self.rect.y += 5
