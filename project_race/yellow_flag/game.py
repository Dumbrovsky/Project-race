import pygame
import json
import random
import os
from .p_car import Player
from .debris import Obstacle
from .gravel import BonusObstacle


# Funkce pro uložení skóre
def save_score(name, score):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "..", "high_scores.json")
    
    try:
        with open(file_path, "r") as file:
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

    high_scores = sorted(high_scores, key=lambda x: x["score"], reverse=True)[:10]

    with open(file_path, "w") as file:
        json.dump(high_scores, file)

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

    last_score_time = pygame.time.get_ticks()
    score_interval = 500
    bg_speed = 9
    obstacle_spawn_time = 500
    bonusobstacle_spawn_time = 500
    last_obstacle_spawn = pygame.time.get_ticks()
    last_bonusobstacle_spawn = pygame.time.get_ticks()

    collided_recently = False
    collision_cooldown = 500
    last_collision_time = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        all_sprites.update()
        current_time = pygame.time.get_ticks()

        if current_time - last_score_time >= score_interval:
            score += 1
            last_score_time = current_time
            print(f"Score: {score}")  # Ladicí výpis pro kontrolu skóre

        base_bg_speed = 9 + score // 10
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            bg_speed = base_bg_speed + 2
            score_interval = max(100, score_interval - 10)
        elif keys[pygame.K_DOWN]:
            bg_speed = max(1, base_bg_speed - 2)
            score_interval += 10
        else:
            bg_speed = base_bg_speed
            score_interval = 500

        print(f"Background Speed: {bg_speed}, Score Interval: {score_interval}")  # Ladicí výpis

        bg_y += bg_speed
        if bg_y >= HEIGHT:
            bg_y = 0

        screen.blit(background, (0, bg_y))
        screen.blit(background, (0, bg_y - HEIGHT))

        if current_time - last_obstacle_spawn >= obstacle_spawn_time:
            for _ in range(random.randint(1, 3)):
                obstacle = Obstacle(50, 50, bg_speed)
                all_sprites.add(obstacle)
                obstacles.add(obstacle)
            last_obstacle_spawn = current_time

        if current_time - last_bonusobstacle_spawn >= bonusobstacle_spawn_time:
            for _ in range(random.randint(0, 1)):
                bonus_obstacle = BonusObstacle(50, 50, bg_speed)
                all_sprites.add(bonus_obstacle)
                bonusobstacle.add(bonus_obstacle)
            last_bonusobstacle_spawn = current_time

        all_sprites.draw(screen)

        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        lives_text = font.render(f"Lives: {player.lives}", True, (0, 0, 0))
        screen.blit(lives_text, (10, 40))

        pygame.display.flip()

        if pygame.sprite.spritecollideany(player, obstacles):
            if not collided_recently:
                player.lives -= 1
                last_collision_time = current_time
                collided_recently = True
                print(f"Životy zbývající: {player.lives}")
                if player.lives <= 0:
                    print("Srážka! Konec hry.")
                    save_score(player_name, score)  # Uložení skóre při ukončení hry
                    running = False
        else:
            if collided_recently and current_time - last_collision_time >= collision_cooldown:
                collided_recently = False

        if pygame.sprite.spritecollideany(player, bonusobstacle):
            if not collided_recently:
                score -= 10
                last_collision_time = current_time
                collided_recently = True
                print(f"Životy zbývající: {player.lives}")
        else:
            if collided_recently and current_time - last_collision_time >= collision_cooldown:
                collided_recently = False

        clock.tick(60)

    print(f"Final Score: {score}")  # Ladicí výpis konečného skóre
    save_score(player_name, score)  # Uložení skóre při ukončení hry
    from yellow_flag.menu import show_menu
    show_menu(screen, WIDTH, HEIGHT)
