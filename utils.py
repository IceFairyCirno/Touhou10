import pygame
import math

def set_background(WINDOW_WIDTH, WINDOW_HEIGHT):
    background = pygame.image.load('Assets\main_background.jpg')
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(background, (0, 0))
    return screen, background

import pygame

def read_move(player_pos, player_radius, player_speed, keys, FIELD_WIDTH, FIELD_HEIGHT):
    # Remove redundant keys assignment (use the passed parameter)
    # Normalize diagonal movement
    dx, dy = 0, 0
    speed = player_speed - 2 if keys[pygame.K_LSHIFT] else player_speed

    if keys[pygame.K_LEFT]:
        dx -= speed
    if keys[pygame.K_RIGHT]:
        dx += speed
    if keys[pygame.K_UP]:
        dy -= speed
    if keys[pygame.K_DOWN]:
        dy += speed

    if dx != 0 and dy != 0:
        diagonal_factor = speed / (2 ** 0.5)
        dx *= diagonal_factor / speed
        dy *= diagonal_factor / speed

    new_x = player_pos[0] + dx
    new_y = player_pos[1] + dy

    new_x = max(39 + player_radius, min(new_x, FIELD_WIDTH + 41 - player_radius))
    new_y = max(21 + player_radius, min(new_y, FIELD_HEIGHT + 21 - player_radius))

    player_pos[0] = new_x
    player_pos[1] = new_y

    return player_pos

def show_position(screen, player_pos):
    font = pygame.font.Font(None, 24)
    coord_text = font.render(f'X: {int(player_pos[0])}, Y: {int(player_pos[1])}', True, (255, 255, 255))
    screen.blit(coord_text, (10, 10))

def update_enemy_bullets(enemy_pos, bullets, player_pos, player_radius, FIELD_WIDTH, FIELD_HEIGHT):
    """
    Manages enemy bullets: spawns downward bullets, updates positions, checks collisions.
    Args:
        enemy_pos: List [x, y] for enemy's center position.
        bullets: List of (rect, speed) tuples for bullets.
        player_hitbox: Pygame Rect for player's hitbox.
        FIELD_WIDTH, FIELD_HEIGHT: Playable field dimensions.
    Returns:
        Tuple: (bullets, game_over) where bullets is the updated list and game_over is True if player is hit.
    """
    # Spawn bullets every 0.5 seconds (30 frames at 60 FPS)
    bullet_spawn_timer = getattr(update_enemy_bullets, 'timer', 0)
    bullet_spawn_timer += 1
    if bullet_spawn_timer >= 30:
        bullet = pygame.Rect(enemy_pos[0] - 4, enemy_pos[1], 8, 8)  # 8x8 bullet at enemy center
        speed = [0, 3]  # Downward speed
        bullets.append((bullet, speed))
        bullet_spawn_timer = 0
    update_enemy_bullets.timer = bullet_spawn_timer

    # Update bullets and check collisions
    game_over = False
    bullet_radius = 4  # Bullets are drawn as 8-pixel diameter circles
    for bullet, speed in bullets[:]:
        bullet.x += speed[0]
        bullet.y += speed[1]
        # Remove bullets that leave the screen
        if not (0 <= bullet.x <= FIELD_WIDTH + 62 and 0 <= bullet.y <= FIELD_HEIGHT + 32):
            bullets.remove((bullet, speed))
        # Circle-circle collision with player
        else:
            # Distance between bullet center and player center
            dx = bullet.centerx - player_pos[0]
            dy = bullet.centery - player_pos[1]
            distance = math.sqrt(dx**2 + dy**2)
            if distance < player_radius + bullet_radius:
                game_over = True
                bullets.remove((bullet, speed))  # Optional: remove bullet on hit

    return bullets, game_over