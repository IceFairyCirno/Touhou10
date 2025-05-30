import pygame
import math
import os

def set_background(WINDOW_WIDTH, WINDOW_HEIGHT):
    background = pygame.image.load('Assets\main_background.jpg')
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(background, (0, 0))
    return screen, background

def show_position(screen, player_pos):
    font = pygame.font.Font(None, 22)
    coord_text = font.render(f'X: {int(player_pos[0])}, Y: {int(player_pos[1])}', True, (255, 255, 255))
    screen.blit(coord_text, (10, 10))

def update_enemy_bullets(enemy_pos, bullets, player_pos, player_radius, FIELD_WIDTH, FIELD_HEIGHT):

    bullet_spawn_timer = getattr(update_enemy_bullets, 'timer', 0)
    bullet_spawn_timer += 1
    if bullet_spawn_timer >= 30:
        bullet = pygame.Rect(enemy_pos[0] - 4, enemy_pos[1], 8, 8)  # 8x8 bullet at enemy center
        speed = [0, 3]  # Downward speed
        bullets.append((bullet, speed))
        bullet_spawn_timer = 0
    update_enemy_bullets.timer = bullet_spawn_timer

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

def update_bullets(bullets, FIELD_WIDTH, FIELD_HEIGHT):
    for bullet, speed in bullets[:]:
        bullet.x += speed[0]
        bullet.y += speed[1]
        if not (0 <= bullet.x <= FIELD_WIDTH + 62 and 0 <= bullet.y <= FIELD_HEIGHT + 32):
            bullets.remove((bullet, speed))

def get_sprite_frames(sprite_sheet, start_x, start_y, frame_width, frame_height, num_frames, direction, debug=False):
    frames = []
    if debug:
        output_dir = "frames"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    for i in range(num_frames):
        x = start_x + (i * frame_width)
        y = start_y
        frame_rect = pygame.Rect(x, y, frame_width, frame_height)
        frame = sprite_sheet.subsurface(frame_rect)
        frames.append(frame)
        if debug:
            filename = os.path.join(output_dir, f"{direction}_frame_{i}.png")
            pygame.image.save(frame, filename)
            print(f"Saved {filename}")
    return frames

def get_next_frame(frames, frame_timer, direction):
    frame_index=0
    if direction==0:
        frame_index = min(int(frame_timer / 7.5), 7)
    else:
        frame_index = (int(frame_timer / 7.5) % 5) + 3
    return frames[frame_index]

