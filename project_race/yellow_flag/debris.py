import pygame
import random



class Obstacle(pygame.sprite.Sprite):
    def __init__(self, width, height, speed):
        super().__init__()

        self.speed = speed

        self.image = pygame.image.load("tyre.png").convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(114, 699 - width)  
        self.rect.y = -height 

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600: 
            self.kill()



