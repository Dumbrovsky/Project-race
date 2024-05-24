import pygame
import random

class BonusObstacle(pygame.sprite.Sprite):
    def __init__(self, width, height, speed):
        super().__init__()

        # Inicializace proměnných
        self.speed = speed

        # Načítání obrázku pneumatiky
        self.image = pygame.image.load("gravel.png").convert_alpha()

        # Nastavení obdélníku pro kolize
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(114, 699 - width)  # Předpokládáme šířku obrazovky 800
        self.rect.y = -height  # Začíná mimo obrazovku

    def update(self):
        # Aktualizace pozice
        self.rect.y += self.speed

        # Kontrola, zda je překážka mimo obrazovku
        if self.rect.top > 600:  # Předpokládáme výšku obrazovky 600
            self.kill()
