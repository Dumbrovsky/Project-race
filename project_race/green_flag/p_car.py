import pygame
from pygame.math import Vector2



class RaceCar(pygame.sprite.Sprite):
    def __init__(self, track_mask):
        super().__init__()
        self.original_image = pygame.image.load("F_race-p_car.png").convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (350, 500)
        self.speed = 5
        self.velocity = Vector2(1, 0)
        self.track_mask = track_mask
        self.last_valid_position = self.rect.center

    def update(self):
        keys = pygame.key.get_pressed()
        rotation_speed = 5  

        if keys[pygame.K_LEFT]:
            self.velocity.rotate_ip(-rotation_speed)
        if keys[pygame.K_RIGHT]:
            self.velocity.rotate_ip(rotation_speed)

        if keys[pygame.K_UP]:
            self.rect.move_ip(self.velocity * self.speed)

        if not self.track_mask.get_at((int(self.rect.centerx), int(self.rect.centery))):
            self.rect.center = (500, 500)  
            self.velocity = Vector2(1, 0) 

        self.last_valid_position = self.rect.center

        angle = self.velocity.angle_to(Vector2(0, -1)) 
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center) 

        self.rect.clamp_ip(pygame.display.get_surface().get_rect())
