import pygame
from utils import*
from player import*

pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
FIELD_WIDTH, FIELD_HEIGHT = 400, 525

pygame.display.set_icon(pygame.image.load('Assets\icon.png'))
pygame.display.set_caption("東方風神録2")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
background = load_background(WINDOW_WIDTH, WINDOW_HEIGHT)
menu, title, start_button, hovered_start_button = load_menu(WINDOW_WIDTH, WINDOW_HEIGHT)
sprite_sheet = pygame.image.load('Assets\spritesheet.png').convert_alpha()

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

frame_timer = 0

player_init_pos = [(FIELD_WIDTH//2)+75+16, (4*FIELD_HEIGHT//5)+37]
player = Player(player_init_pos, radius=5, speed=4, bullets=[], sprite_sheet=sprite_sheet)


running = True
clock = pygame.time.Clock()
game_started = False

bullets=[]

enemy = Enemy("boss", [(FIELD_WIDTH//2)+75, 70], 10000, 2, [], sprite_sheet)
path = [[100, 100], [400, 200], [300, 50], [288, 288]]
current_target_index = 0
enemys = [enemy]

while running:
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_started:
            clicked_pos = pygame.mouse.get_pos()
            if start_button.get_rect(topleft=(WINDOW_WIDTH//2 - start_button.get_width()//2, 450)).collidepoint(clicked_pos):
                fade(screen, fade_duration_ms=1000, out=True)
                fade(screen, fade_duration_ms=500, out=False)
                game_started = True


    if not game_started:
        screen.blit(menu, (0, 0))
        screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, 70))
        screen.blit(start_button, (WINDOW_WIDTH//2 - start_button.get_width()//2, 450))

        hover_pos = pygame.mouse.get_pos()
        if start_button.get_rect(topleft=(WINDOW_WIDTH//2 - start_button.get_width()//2, 450)).collidepoint(hover_pos):
            screen.blit(hovered_start_button, (WINDOW_WIDTH//2 - hovered_start_button.get_width()//2, 450))
        else:
            screen.blit(start_button, (WINDOW_WIDTH//2 - start_button.get_width()//2, 450))

    #Main Game Loop
    if game_started:

        screen.blit(background, (0, 0))
        enemy.display_health_bar(screen)

        #Enemy
        for enemy in enemys:
            if enemy.identity=="boss":
                enemy.display_health_bar(screen)
            enemy_current_frame = enemy.frame_to_display(frame_timer)
            screen.blit(enemy_current_frame, enemy.sprite_pos)
            if current_target_index != -1:
                current_target_index = move_through_path(enemy, path, current_target_index)
        #Player
        player.read_move(keys, FIELD_WIDTH, FIELD_HEIGHT)
        current_frame = player.frame_to_display(frame_timer)
        screen.blit(current_frame, player.sprite_pos)

        if (keys[pygame.K_LSHIFT]):
            player.display_centroid(screen)
        if (keys[pygame.K_z]):
            player.shoot(sprite_sheet, frame_timer, 5)
        player.update_bullet(screen, enemys)

    show_position(screen, player.centroid)
    pygame.display.flip()
    clock.tick(60)
    frame_timer = (frame_timer+1) if frame_timer < 60 else 0

pygame.quit()