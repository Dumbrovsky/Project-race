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
        self.velocity = Vector2(1, 0)  # Původní směr vozidla (vpravo)
        self.track_mask = track_mask
        self.last_valid_position = self.rect.center
        self.tire_wear = 100  # Přidáme parametr pro opotřebení pneumatik

    def update(self):
        keys = pygame.key.get_pressed()
        rotation_speed = 5  # Rychlost otáčení auta

        # Změna směru vozidla podle stisknutých kláves
        if keys[pygame.K_LEFT]:
            self.velocity.rotate_ip(-rotation_speed)
            self.tire_wear -= 1  # Opotřebení pneumatik při zatáčení
        if keys[pygame.K_RIGHT]:
            self.velocity.rotate_ip(rotation_speed)
            self.tire_wear -= 1  # Opotřebení pneumatik při zatáčení

        # Pohyb vozidla
        if keys[pygame.K_UP]:
            self.rect.move_ip(self.velocity * self.speed)

        # Omezení pohybu vozidla na trajektorii trati
        if not self.track_mask.get_at((int(self.rect.centerx), int(self.rect.centery))):
            self.rect.center = self.last_valid_position  # Vrátit auto na poslední validní pozici
            self.velocity = Vector2(1, 0)  # Resetovat směr pohybu

        self.last_valid_position = self.rect.center

        # Otočení obrázku podle směru pohybu
        angle = self.velocity.angle_to(Vector2(0, -1))  # Vypočítat úhel mezi aktuálním směrem a směrem nahoru
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)  # Udržovat pozici vozidla

        # Omezení pohybu vozidla do hranic okna (volitelné)
        self.rect.clamp_ip(pygame.display.get_surface().get_rect())

