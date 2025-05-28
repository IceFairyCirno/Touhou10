import pygame
from utils import*

pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
FIELD_WIDTH, FIELD_HEIGHT = 385*1.25, 447*1.25

pygame.display.set_icon(pygame.image.load('Assets\icon.png'))
pygame.display.set_caption("東方風神録2")
screen, background = set_background(WINDOW_WIDTH, WINDOW_HEIGHT)
sprite_sheet = pygame.image.load('Assets\spritesheet.png').convert_alpha()

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

player_pos = [(FIELD_WIDTH//2)+31, (4*FIELD_HEIGHT//5)+16]
player_frames = get_sprite_frames(sprite_sheet, 16, 16, 32, 48, 8)
player_radius = 5
player_speed = 4

enemy_pos = [(FIELD_WIDTH//2)+31, 70]

running = True
clock = pygame.time.Clock()
frame_timer, current_frame = 0, 0

bullets=[]

    
while running:
    keys = pygame.key.get_pressed()

    screen.blit(background, (0, 0))
    screen.blit(player_frames[0], ((FIELD_WIDTH//2)+31-(31//2), 70-(41//2))) #enemy
    
    player_pos = read_move(player_pos, player_radius, player_speed, keys, FIELD_WIDTH, FIELD_HEIGHT)
    player_centroid = (player_pos[0] + 16, player_pos[1] + 24)
    frame_timer, current_frame = get_current_frame(player_frames, frame_timer, current_frame)
    screen.blit(player_frames[current_frame], player_pos)
    if (keys[pygame.K_LSHIFT]):
        pygame.draw.circle(screen, BLACK, player_centroid, player_radius)
        pygame.draw.circle(screen, WHITE, player_centroid, player_radius-2)

    bullets, game_over = update_enemy_bullets(enemy_pos, bullets, player_centroid, player_radius, FIELD_WIDTH, FIELD_HEIGHT)
    for bullet, _ in bullets:
        pygame.draw.circle(screen, (255, 0, 128), bullet.center, 4)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    show_position(screen, player_pos)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()