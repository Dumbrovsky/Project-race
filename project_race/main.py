import pygame
import sys
from yellow_flag.menu import show_menu as show_yellow_flag_menu
from green_flag.menu import show_menu as show_green_flag_menu
from pitstop.menu import show_menu as show_pitstop_menu  



pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Závodní hra")

def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def main_menu(screen, WIDTH, HEIGHT):
    menu = True
    while menu:
        screen.fill((0, 0, 0))
        draw_text(screen, "Main Menu", 64, WIDTH // 2, HEIGHT // 4)
        draw_text(screen, "1. Yellow Flag", 36, WIDTH // 2, HEIGHT // 2)
        draw_text(screen, "2. Green Flag", 36, WIDTH // 2, HEIGHT // 2 + 50)
        draw_text(screen, "3. Pitstop", 36, WIDTH // 2, HEIGHT // 2 + 100)  
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    show_yellow_flag_menu(screen, WIDTH, HEIGHT)
                if event.key == pygame.K_2:
                    show_green_flag_menu(screen, WIDTH, HEIGHT)
                if event.key == pygame.K_3:
                    show_pitstop_menu(screen, WIDTH, HEIGHT)

def main():
    main_menu(screen, WIDTH, HEIGHT)

if __name__ == "__main__":
    main()

pygame.quit()
sys.exit()
