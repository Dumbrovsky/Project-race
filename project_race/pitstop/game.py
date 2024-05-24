import pygame
import time
import json
from pitstop.p_car import RaceCar  # Importujeme RaceCar z pitstop_p_car.py



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
    track_image = pygame.image.load("race_track.png")
    track_image = pygame.transform.scale(track_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
    background_color = (86, 125, 70)
    track_mask = create_track_mask(track_image, background_color)
    return track_mask

def run_pitstop(screen, WIDTH, HEIGHT, player_name):
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    background = pygame.image.load("race_track.png").convert()

    track_mask = load_track()
    race_car = RaceCar(track_mask)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(race_car)

    distance_traveled = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            distance_traveled += 1

        all_sprites.update()

        if race_car.tire_wear <= 0:
            save_score(player_name, distance_traveled)
            from pitstop.menu import show_menu
            show_menu(screen, WIDTH, HEIGHT)
            return

        screen.blit(background, (0, 0))
        all_sprites.draw(screen)

        tire_wear_text = font.render(f"Opotřebení pneumatik: {race_car.tire_wear}%", True, (255, 255, 255))
        distance_text = font.render(f"Vzdálenost: {distance_traveled} m", True, (255, 255, 255))
        screen.blit(tire_wear_text, (10, 10))
        screen.blit(distance_text, (10, 50))
        pygame.display.flip()

        clock.tick(60)

    from pitstop.menu import show_menu
    show_menu(screen, WIDTH, HEIGHT)

def save_score(player_name, distance):
    try:
        with open("pitstop_scores.json", "r") as file:
            scores = json.load(file)
    except FileNotFoundError:
        scores = []

    updated = False
    for entry in scores:
        if entry['name'] == player_name:
            if distance > entry.get('distance', 0):
                entry['distance'] = distance
            updated = True
            break

    if not updated:
        scores.append({'name': player_name, 'distance': distance})

    with open("pitstop_scores.json", "w") as file:
        json.dump(scores, file)
