import pygame
from utils import*
from player import*

pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
FIELD_WIDTH, FIELD_HEIGHT = 400, 525

pygame.display.set_icon(pygame.image.load('Assets\icon.png'))
pygame.display.set_caption("東方風神録2")
screen, background = set_background(WINDOW_WIDTH, WINDOW_HEIGHT)
sprite_sheet = pygame.image.load('Assets\spritesheet.png').convert_alpha()

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

frame_timer = 0

player_init_pos = [(FIELD_WIDTH//2)+75+16, (4*FIELD_HEIGHT//5)+37]
player = Player(player_init_pos, 5, 4, [], sprite_sheet)


running = True
clock = pygame.time.Clock()

bullets=[]

enemy = Enemy([(FIELD_WIDTH//2)+75, 70], 10000, 2, [], sprite_sheet)
path = [[100, 100], [400, 200], [300, 50], [288, 288]]
current_target_index = 0

while running:
    keys = pygame.key.get_pressed()

    screen.blit(background, (0, 0))
    enemy.display_health_bar(screen)
    #enemy
    enemy_current_frame = enemy.frame_to_display(frame_timer)
    screen.blit(enemy_current_frame, enemy.sprite_pos)

    current_target_index = move_through_path(enemy, path, current_target_index)
    if current_target_index == -1:
        pass

    #player
    player.read_move(keys, FIELD_WIDTH, FIELD_HEIGHT)
    current_frame = player.frame_to_display(frame_timer)
    screen.blit(current_frame, player.sprite_pos)

    if (keys[pygame.K_LSHIFT]):
        pygame.draw.circle(screen, BLACK, player.centroid, player.radius)
        pygame.draw.circle(screen, WHITE, player.centroid, player.radius-2)

    if (keys[pygame.K_z]):
        player.shoot()

    update_bullets(player.bullets, FIELD_WIDTH, FIELD_HEIGHT)
    for bullet in player.bullets:
        bullet.move()
        pygame.draw.circle(screen, (0, 255, 0), bullet.position, 4)
        if bullet.hitbox.colliderect(enemy.hitbox):
            player.bullets.remove(bullet)
            enemy.health -=10

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    show_position(screen, player.centroid)
    pygame.display.flip()
    clock.tick(60)
    frame_timer = (frame_timer+1) if frame_timer < 60 else 0

pygame.quit()