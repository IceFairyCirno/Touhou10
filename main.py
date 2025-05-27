import pygame
from utils import*


pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
FIELD_WIDTH, FIELD_HEIGHT = 385*1.25, 447*1.25

pygame.display.set_icon(pygame.image.load('Assets\icon.png'))
pygame.display.set_caption("東方風神録2")

screen, background = set_background(WINDOW_WIDTH, WINDOW_HEIGHT)
sprite_sheet = pygame.image.load('Assets\spritesheet.png').convert_alpha()
print("Sprite sheet loaded successfully!")

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

player_pos = [(FIELD_WIDTH//2)+31, (4*FIELD_HEIGHT//5)+16]
player_radius = 5
player_speed = 4

enemy_pos = [(FIELD_WIDTH//2)+31, 70]


running = True
clock = pygame.time.Clock()

bullets=[]
reimu_frames = []

frame_rect = pygame.Rect(18, 18, 32, 41)
frame = sprite_sheet.subsurface(frame_rect)
filename = f"reimu_frame_{1}.png"
pygame.image.save(frame, filename)
reimu_frames.append(frame)

    
while running:

    screen.blit(background, (0, 0))
    screen.blit(reimu_frames[0], ((FIELD_WIDTH//2)+31-(31//2), 70-(41//2)))
    
    player_pos = read_move(player_pos, player_radius, player_speed, pygame.key.get_pressed(), FIELD_WIDTH, FIELD_HEIGHT)
    pygame.draw.circle(screen, GREEN, player_pos, player_radius)

    bullets, game_over = update_enemy_bullets(enemy_pos, bullets, player_pos, player_radius, FIELD_WIDTH, FIELD_HEIGHT)
    for bullet, _ in bullets:
        pygame.draw.circle(screen, (255, 0, 128), bullet.center, 4)

    if game_over:
        running = False
    
    show_position(screen, player_pos)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False


    pygame.display.flip()

    clock.tick(60)

pygame.quit()