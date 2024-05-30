import pygame
import sys
import json
from pitstop.game import run_pitstop



def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def show_menu(screen, WIDTH, HEIGHT):
    background_image = pygame.image.load("Pmenu_picture.png").convert()

    menu = True
    while menu:
        screen.blit(background_image, (0, 0))

        draw_text(screen, "Pitstop", 64, WIDTH // 2, HEIGHT // 4)
        draw_text(screen, "1. Hrát", 36, WIDTH // 2, HEIGHT // 2)
        draw_text(screen, "2. Tabulka nejlepších", 36, WIDTH // 2, HEIGHT // 2 + 50)
        draw_text(screen, "Stiskněte ESC pro návrat do menu", 24, WIDTH // 2, HEIGHT - 50)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    player_name = get_player_name(screen, WIDTH, HEIGHT)
                    if player_name == "":
                        return
                    run_pitstop(screen, WIDTH, HEIGHT, player_name)
                if event.key == pygame.K_2:
                    show_high_scores(screen, WIDTH, HEIGHT)
                if event.key == pygame.K_ESCAPE:
                    return

def get_player_name(screen, WIDTH, HEIGHT):
    name = ""
    input_active = True
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_ESCAPE:
                    return ""
                else:
                    name += event.unicode

        screen.fill((0, 0, 0))
        draw_text(screen, "Enter your name:", 36, WIDTH // 2, HEIGHT // 2 - 50)
        draw_text(screen, name, 36, WIDTH // 2, HEIGHT // 2)
        pygame.display.flip()

    return name

def show_high_scores(screen, WIDTH, HEIGHT):
    try:
        with open("pitstop_scores.json", "r") as file:
            scores = json.load(file)
    except FileNotFoundError:
        scores = []

    scores.sort(key=lambda x: x.get('distance', 0), reverse=True)

    show_scores = True
    while show_scores:
        screen.fill((0, 0, 0))
        draw_text(screen, "High Scores", 64, WIDTH // 2, HEIGHT // 4)
        y_offset = HEIGHT // 4 + 50
        for i, entry in enumerate(scores):
            name = entry.get('name', 'Unknown')
            distance = entry.get('distance', 0)
            draw_text(screen, f"{i + 1}. {name} - {distance:.2f} m", 36, WIDTH // 2, y_offset)
            y_offset += 40

        draw_text(screen, "Stiskněte ESC pro návrat do menu", 24, WIDTH // 2, HEIGHT - 50)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    show_scores = False
                    show_menu(screen, WIDTH, HEIGHT)
                    return

