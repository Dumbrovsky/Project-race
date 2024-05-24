import pygame
import time
import json
from green_flag.p_car import RaceCar

# Definice šířky a výšky okna
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

def create_track_mask(track_image, background_color):
    track_mask = pygame.mask.from_surface(track_image)
    width, height = track_image.get_size()
    for x in range(width):
        for y in range(height):
            if track_image.get_at((x, y)) == background_color:
                track_mask.set_at((x, y), 0)
            else:
                track_mask.set_at((x, y), 1)
    return track_mask

def load_track():
    # Načtení obrázku trati
    track_image = pygame.image.load("race_track.png")
    track_image = pygame.transform.scale(track_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
    
    # Barva pozadí
    background_color = (86, 125, 70)

    # Vytvoření masky trati
    track_mask = create_track_mask(track_image, background_color)

    return track_mask

def run_race(screen, WIDTH, HEIGHT, player_name):
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    background = pygame.image.load("race_track.png").convert()

    # Načtení a vytvoření masky trati
    track_mask = load_track()

    race_car = RaceCar(track_mask)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(race_car)

    # Definování cílové čáry jako obdélníku
    finish_line_rect = pygame.Rect(387, 415, 1, 123)  # Nastavení pozice a velikosti cílové čáry
    finish_cooldown_rect = pygame.Rect(387, 415 - 50, 1, 123 + 100)  # Cooldown zóna kolem cílové čáry

    total_laps = 3
    current_lap = 0
    race_start_time = None
    race_end_time = None
    finish_line_delay = 0.2  # Zpoždění pro detekci průjezdu cílem (v sekundách)
    finish_line_crossed = False  # Flag pro zajištění, že cílová čára je překročena pouze jednou za kolo
    cooldown_zone_left = True  # Flag pro zajištění, že auto opustilo cooldown zónu

    running = True
    race_started = False  # Označení, zda závod začal

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if not race_started and (keys[pygame.K_UP] or keys[pygame.K_DOWN]):
            race_started = True
            race_start_time = time.time()

        all_sprites.update()

        # Kontrola, zda auto přejelo cílovou čáru
        if race_car.rect.colliderect(finish_line_rect):
            if not finish_line_crossed and cooldown_zone_left:
                finish_line_crossed = True
                passed_finish_line_time = time.time()

        # Zajistit, že auto opustilo cooldown zónu před započítáním dalšího kola
        if not race_car.rect.colliderect(finish_cooldown_rect):
            cooldown_zone_left = True

        # Zajistit legitimní překročení cílové čáry se zpožděním
        if finish_line_crossed and time.time() - passed_finish_line_time >= finish_line_delay:
            finish_line_crossed = False
            cooldown_zone_left = False
            if race_started:
                current_lap += 1
                if current_lap > total_laps:
                    race_end_time = time.time()
                    total_race_time = race_end_time - race_start_time
                    print(f"Race finished! Time: {total_race_time:.2f} seconds")
                    save_race_time(player_name, total_race_time)
                    from green_flag.menu import show_menu
                    show_menu(screen, WIDTH, HEIGHT)
                    return  # Zajistit, že hra skončí po zobrazení menu

        screen.blit(background, (0, 0))

        # Zajistit, že auto zůstane na trati
        if not track_mask.get_at((int(race_car.rect.centerx), int(race_car.rect.centery))):
            race_car.rect.center = (400, 500)  # Reset pozice auta
            race_car.velocity = pygame.math.Vector2(1, 0)  # Reset směru pohybu auta

        # Vykreslení cílové čáry
        pygame.draw.rect(screen, (255, 0, 0), finish_line_rect)
        # Vykreslení cooldown zóny (volitelné, pro ladění)
        pygame.draw.rect(screen, (0, 255, 0), finish_cooldown_rect, 1)

        all_sprites.draw(screen)

        lap_text = font.render(f"Lap: {current_lap}/{total_laps}", True, (255, 255, 255))
        screen.blit(lap_text, (10, 10))
        pygame.display.flip()

        clock.tick(60)

    from main import main_menu
    main_menu(screen, WIDTH, HEIGHT)


def save_race_time(name, lap_time):
    lap_time = round(lap_time, 3)  # Zaokrouhlení času na tisíciny sekundy
    try:
        with open("race_times.json", "r") as file:
            race_times = json.load(file)
    except FileNotFoundError:
        race_times = []

    # Najít a aktualizovat nejlepší čas pro dané jméno
    found = False
    for record in race_times:
        if record["name"] == name:
            found = True
            if lap_time < record["time"]:
                record["time"] = lap_time
            break

    if not found:
        race_times.append({"name": name, "time": lap_time})

    race_times = sorted(race_times, key=lambda x: x["time"])[:10]

    with open("race_times.json", "w") as file:
        json.dump(race_times, file)