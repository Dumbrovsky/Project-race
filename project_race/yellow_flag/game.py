import pygame
import json
import random
from .p_car import Player
from .debris import Obstacle
from .gravel import BonusObstacle



# Funkce pro spuštění hry
def run_game(screen, WIDTH, HEIGHT, player_name):
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    background = pygame.image.load("trať.png").convert()
    score = 0
    player = Player()
    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    bonusobstacle = pygame.sprite.Group()
    all_sprites.add(player)
    bg_y = 0

    # Časová značka pro počítání skóre a rychlost pozadí
    last_score_time = pygame.time.get_ticks()
    score_interval = 500  # Interval pro přičítání skóre (v milisekundách)
    bg_speed = 9
    obstacle_spawn_time = 500  # Interval pro generování překážek (v milisekundách) - zkráceno
    bonusobstacle_spawn_time = 500
    last_obstacle_spawn = pygame.time.get_ticks()
    last_bonusobstacle_spawn = pygame.time.get_ticks()

    # Flag pro kontrolu, zda hráč právě narazil do překážky
    collided_recently = False
    collision_cooldown = 500  # 2 sekundy cooldown po kolizi
    last_collision_time = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        all_sprites.update()

        # Aktuální čas
        current_time = pygame.time.get_ticks()

        # Zvýšení skóre na základě aktuálního intervalu
        if current_time - last_score_time >= score_interval:
            score += 1
            last_score_time = current_time
            print(f"Score: {score}")  # Ladicí výpis pro kontrolu skóre

        # Dynamická rychlost pozadí na základě skóre
        base_bg_speed = 9 + score // 10  # Základní rychlost pozadí na základě skóre
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            bg_speed = base_bg_speed + 2
            score_interval = max(100, score_interval - 10)  # Zrychlení přičítání skóre
        elif keys[pygame.K_DOWN]:
            bg_speed = max(1, base_bg_speed - 2)  # Zajištění, že rychlost nebude menší než 1
            score_interval += 10  # Zpomalení přičítání skóre
        else:
            bg_speed = base_bg_speed
            score_interval = 500  # Reset intervalu pro přičítání skóre

        print(f"Background Speed: {bg_speed}, Score Interval: {score_interval}")  # Ladicí výpis pro kontrolu rychlosti a intervalu

        # Pohyb pozadí
        bg_y += bg_speed
        if bg_y >= HEIGHT:
            bg_y = 0

        # Vykreslení pohybujícího se pozadí
        screen.blit(background, (0, bg_y))
        screen.blit(background, (0, bg_y - HEIGHT))

        # Generování běžných překážek
        if current_time - last_obstacle_spawn >= obstacle_spawn_time:
            for _ in range(random.randint(1, 3)):  # Generování 1 až 2 běžných překážek najednou
                obstacle = Obstacle(50, 50, bg_speed)  # Předání pouze šířky, výšky a rychlosti
                all_sprites.add(obstacle)
                obstacles.add(obstacle)
            last_obstacle_spawn = current_time

        # Generování bonusových překážek
        if current_time - last_bonusobstacle_spawn >= bonusobstacle_spawn_time:
            for _ in range(random.randint(0, 1)):  # Generování 1 bonusové překážky
                bonus_obstacle = BonusObstacle(50, 50, bg_speed)  # Předání pouze šířky, výšky a rychlosti
                all_sprites.add(bonus_obstacle)
                bonusobstacle.add(bonus_obstacle)
            last_bonusobstacle_spawn = current_time



        all_sprites.draw(screen)

        # Vykreslení skóre a životů
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))  # Černá barva
        screen.blit(score_text, (10, 10))
        lives_text = font.render(f"Lives: {player.lives}", True, (0, 0, 0))  # Černá barva
        screen.blit(lives_text, (10, 40))

        pygame.display.flip()

        # Kontrola srážky hráče s překážkami
        if pygame.sprite.spritecollideany(player, obstacles):
            if not collided_recently:  # Kontrola zda nebyla nedávná kolize
                player.lives -= 1
                last_collision_time = current_time
                collided_recently = True
                print(f"Životy zbývající: {player.lives}")
                if player.lives <= 0:
                    print("Srážka! Konec hry.")
                    running = False
        else:
            # Resetovat collided_recently, pokud uplyne čas cooldownu pro kolizi
            if collided_recently and current_time - last_collision_time >= collision_cooldown:
                collided_recently = False

        # Kontrola srážky hráče s štěrkem
        if pygame.sprite.spritecollideany(player, bonusobstacle):
            if not collided_recently:  # Kontrola zda nebyla nedávná kolize
                score -= 10
                last_collision_time = current_time
                collided_recently = True
                print(f"Životy zbývající: {player.lives}")
        else:
            # Resetovat collided_recently, pokud uplyne čas cooldownu pro kolizi
            if collided_recently and current_time - last_collision_time >= collision_cooldown:
                collided_recently = False


        # Nastavení framerate na 60 FPS
        clock.tick(60)

    save_score(player_name, score)
    from yellow_flag.menu import show_menu
    show_menu(screen, WIDTH, HEIGHT)

# Najít a aktualizovat nejlepší skóre pro dané jméno
def save_score(name, score):
    try:
        with open("high_scores.json", "r") as file:
            high_scores = json.load(file)
    except FileNotFoundError:
        high_scores = []

        player_exists = False
    for entry in high_scores:
        if entry["name"] == name:
            player_exists = True
            if score > entry["score"]:
                entry["score"] = score  
            break

    if not player_exists:
        high_scores.append({"name": name, "score": score})

    # Sort and keep only the top 10 scores
    high_scores = sorted(high_scores, key=lambda x: x["score"], reverse=True)[:10]

    with open("high_scores.json", "w") as file:
        json.dump(high_scores, file)