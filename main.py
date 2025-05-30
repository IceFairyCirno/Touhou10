import pygame
from utils import*
from player import*

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

player_stand_frames = get_sprite_frames(sprite_sheet, 16, 16, 32, 48, 8, "up or down")
player_right_frames = get_sprite_frames(sprite_sheet, 16, 112, 32, 48, 8, "right")
player_left_frames = get_sprite_frames(sprite_sheet, 16, 64, 32, 48, 8, "left")

frame_timer = 0

player = Player([(FIELD_WIDTH//2)+31+16, (4*FIELD_HEIGHT//5)+16+24], 5, [(FIELD_WIDTH//2)+31, (4*FIELD_HEIGHT//5)+16], 4, [], 0)

enemy_pos = [(FIELD_WIDTH//2)+31, 70]
enemy_stand_frames = get_sprite_frames(sprite_sheet, 282, 16, 32, 48, 8, "up or down")

running = True
clock = pygame.time.Clock()

bullets=[]

    
while running:
    keys = pygame.key.get_pressed()

    screen.blit(background, (0, 0))
    #enemy
    enemy_current_frame = enemy_stand_frames
    enemy_current_frame = get_next_frame(enemy_current_frame, frame_timer, 0)
    screen.blit(enemy_current_frame, ((FIELD_WIDTH//2)+31-(31//2), 70-(41//2)))

    #player
    player.read_move(keys, FIELD_WIDTH, FIELD_HEIGHT)
    current_frame = player_stand_frames if player.direction==0 else (player_right_frames if player.direction=="right" else player_left_frames)
    current_frame = get_next_frame(current_frame, frame_timer, player.direction)
    screen.blit(current_frame, player.sprite_pos)
    if (keys[pygame.K_LSHIFT]):
        pygame.draw.circle(screen, BLACK, player.centroid, player.radius)
        pygame.draw.circle(screen, WHITE, player.centroid, player.radius-2)
    if (keys[pygame.K_z]):
        player.shoot()
    update_bullets(player.bullets, FIELD_WIDTH, FIELD_HEIGHT)
    for bullet, _ in player.bullets:
        pygame.draw.circle(screen, (0, 255, 0), bullet.center, 4)


    bullets, game_over = update_enemy_bullets(enemy_pos, bullets, player.centroid, player.radius, FIELD_WIDTH, FIELD_HEIGHT)
    for bullet, _ in bullets:
        pygame.draw.circle(screen, (255, 0, 128), bullet.center, 4)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    show_position(screen, player.centroid)
    pygame.display.flip()
    clock.tick(60)
    frame_timer = (frame_timer+1) if frame_timer < 60 else 0

pygame.quit()