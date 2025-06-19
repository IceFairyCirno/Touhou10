import pygame
from utils import *
from player import Player

class Dummy:
    def __init__(self, center, color, radius):
        self.hitbox = Hitbox(center, 2*radius, 2*radius, 0)
        self.color = color
        self.lives = 3
        self.health = 10
        self.radius = radius

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.hitbox.center[0]), int(self.hitbox.center[1])), self.radius)
        #self.hitbox.display_hitbox(screen)

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
# Placeholder sprite sheet (just a filled surface)
sprite_sheet = pygame.image.load("Assets\sanae_spritesheet.png")


player = Player(centroid=[100, 100], radius=5, speed=5, lives=3, spellcard=3, sprite_sheet=sprite_sheet)
enemy = Dummy([300, 100], (255, 0, 0), 20)
player = Dummy([300,300], (0, 255, 0), 10)
enemies = [enemy]

bullets = []
running = True
while running:
    dt = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Shoot bullet on space
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullets.append(Bullet("player", 5, 1, [player.hitbox.center[0]-16, player.hitbox.center[1]-6], 105, sprite_sheet))
            bullets.append(Bullet("player", 5, 1, [player.hitbox.center[0], player.hitbox.center[1]-6], 90, sprite_sheet))
            bullets.append(Bullet("player", 5, 1, [player.hitbox.center[0]+16, player.hitbox.center[1]-6], 75, sprite_sheet))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
            player.hitbox.center[0] -= 5
    if keys[pygame.K_RIGHT]:
            player.hitbox.center[0] += 5
    if keys[pygame.K_UP]:
            player.hitbox.center[1] -= 5
    if keys[pygame.K_DOWN]:
            player.hitbox.center[1] += 5
    player.hitbox.update()

    screen.fill((30, 30, 30))
    player.draw(screen)
    for e in enemies:
        e.draw(screen)
        e.hitbox.display_hitbox(screen)
        if fire_rate_limitation(dt, 0.5):
            for i in range(0, 346, 15):
                bullets.append(Bullet("enemy", 5, 1, enemy.hitbox.center, i, sprite_sheet))

    bullets = update_bullets(bullets, player, enemies)
    for bullet in bullets:
        bullet.draw(dt, screen)
        #bullet.hitbox.display_hitbox(screen)

    pygame.display.flip()
pygame.quit()
