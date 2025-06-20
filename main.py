import pygame
from utils import*
from player import*
from enemy import*
from collections import deque

pygame.init()
pygame.mixer.init()

#Initial window specs
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
FIELD_WIDTH, FIELD_HEIGHT = 400, 525
FIELD_TOPLEFT = [75, 37]
FIELD_CENTER = [FIELD_TOPLEFT[0]+FIELD_WIDTH//2, FIELD_TOPLEFT[1]+FIELD_HEIGHT//2]

#Initial window setup
pygame.display.set_icon(pygame.image.load('Assets/icon.png'))
pygame.display.set_caption("東方風神録2")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

#Menu setup
menu, title, start_button, hovered_start_button = load_menu(WINDOW_WIDTH, WINDOW_HEIGHT)
start_menu_music = True

#Main game background setup
background = pygame.Surface((400, 525))
background.fill((0, 0, 0))
background_edge = pygame.image.load('Assets/background_edge.png').convert_alpha()
sidebar_items = pygame.image.load('Assets/sidebar_items_spritesheet.png').convert_alpha()
texts = load_frames(sidebar_items, [[359, 5, 166, 47], [535, 5, 144, 74], [689, 5, 138, 43], [837, 5, 122, 39], [973, 12, 42, 35]], "texts")
texts = [pygame.transform.smoothscale(text, (text.get_width()//2, text.get_height()//2)) for text in texts]


#Field setup
field_box = Hitbox(FIELD_CENTER, FIELD_WIDTH, FIELD_HEIGHT, 0)

#Main game assets
player_sprite_sheet = pygame.image.load('Assets/sanae_spritesheet.png').convert_alpha()
enemy_sprite_sheet = pygame.image.load('Assets/enemy_spritesheet.png').convert_alpha()
boss_sprite_sheet = pygame.image.load('Assets/boss_spritesheet.png').convert_alpha()
bullet_sprite_sheet = pygame.image.load("Assets/boss_bullets_spritesheet.png").convert_alpha()
#Game audios
pygame.mixer.music.load('Assets/menu_music.mp3')

#Player initialization
player_initial_position = [FIELD_TOPLEFT[0]+FIELD_WIDTH//2, FIELD_TOPLEFT[1]+FIELD_HEIGHT//2]
player = Player(FIELD_CENTER, radius=5, speed=5, lives=3, spellcard=3, sprite_sheet=player_sprite_sheet)

#Enemy initialization
path = deque(generate_coordinates(10))
enemy = Enemy("boss", "Reimu", FIELD_CENTER, 1000, 2, boss_sprite_sheet, bullet_sprite_sheet)
enemies = [enemy]

#Main game attributes
running = True
clock = pygame.time.Clock()
game_started = True
global_bullets = []
FPS = 60


#Main game initialization
while running:

    dt = clock.tick(FPS)/1000.0
    keys = pygame.key.get_pressed()

    #[FOR ALL] Obtain events
    for event in pygame.event.get():
        #[FOR ALL] Quit game options
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        #[MENU] Player click options
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_started:
            clicked_pos = pygame.mouse.get_pos()
            if start_button.get_rect(topleft=(WINDOW_WIDTH//2 - start_button.get_width()//2, 450)).collidepoint(clicked_pos):
                pygame.mixer.music.stop()
                display_loading_screen(screen)
                game_started = True

    #[MENU] Menu operations
    if not game_started:
        #[MENU] Set up background music
        if start_menu_music:
            pygame.mixer.music.set_volume(0.15)
            pygame.mixer.music.play(-1, fade_ms=3000)
        #[MENU] Display menu
        build_menu(screen, menu, title, start_button, hovered_start_button)
        #[MENU] Handle cursor hovering effect
        hover_pos = pygame.mouse.get_pos()
        if start_button.get_rect(topleft=(WINDOW_WIDTH//2 - start_button.get_width()//2, 450)).collidepoint(hover_pos):
            screen.blit(hovered_start_button, (WINDOW_WIDTH//2 - hovered_start_button.get_width()//2, 450))
        else:
            screen.blit(start_button, (WINDOW_WIDTH//2 - start_button.get_width()//2, 450))
        start_menu_music = False
    #[MAIN GAME] Main game operations
    if game_started:
        #[MAIN GAME] Display background
        screen.blit(background, (75, 37))

        #[MAIN GAME] Player Handling
        player.read_move(keys, field_box=field_box, screen=screen)
        player.draw(dt, screen)
        if keys[pygame.K_z]:
            if fire_rate_limitation(dt, 0.1, player):
                player.shoot(global_bullets)
        if keys[pygame.K_LSHIFT]:
            player.display_centroid(screen)

        #[MAIN GAME] Enemy handling
        for enemy in enemies:
            path = enemy.move_by_path(path)
            enemy.draw(dt, screen)
            if fire_rate_limitation(dt, 0.2, enemy):
                enemy.shoot(global_bullets, "flower")
        
        #[MAIN GAME] Bullet handling
        global_bullets = update_bullets(global_bullets, player, enemies)
        for bullet in global_bullets:
            bullet.draw(dt, screen)

        #[MAIN GAME] Update edge
        screen.blit(background_edge, (0, 0))
        build_sidebar_items(screen, texts, player)
        show_position(screen, player.centroid)
        enemy.display_health_bar(screen)

    pygame.display.flip()

pygame.quit()