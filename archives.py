"""
This Python file is to store not-used/ out-dated function created before for reference
"""

#player.py
"""
class Player:
    def __init__(self, centroid, radius, speed, bullets, sprite_sheet):
        self.centroid = centroid
        self.radius = radius
        self.sprite_pos = [centroid[0]-16, centroid[1]-24]
        self.speed = speed
        self.bullets = bullets
        self.direction = 0
        self.stand_frame = get_sprite_frames(sprite_sheet, 16, 16, 32, 48, 8, "up or down")
        self.right_frames = get_sprite_frames(sprite_sheet, 16, 112, 32, 48, 8, "right")
        self.left_frames = get_sprite_frames(sprite_sheet, 16, 64, 32, 48, 8, "left")
    
    def read_move(self, keys, FIELD_WIDTH, FIELD_HEIGHT):
        dx, dy = 0, 0
        speed = self.speed - 2 if keys[pygame.K_LSHIFT] else self.speed
        self.direction=0
        if keys[pygame.K_LEFT]:
            dx -= speed
            self.direction = "left"
        if keys[pygame.K_RIGHT]:
            dx += speed
            self.direction = "right"
        if keys[pygame.K_UP]:
            dy -= speed
        if keys[pygame.K_DOWN]:
            dy += speed

        if dx != 0 and dy != 0:
            diagonal_factor = speed / (2 ** 0.5)
            dx *= diagonal_factor / speed
            dy *= diagonal_factor / speed

        new_x = self.centroid[0] + dx
        new_y = self.centroid[1] + dy

        new_x = max(75 + 32//2, min(new_x, FIELD_WIDTH + 75 - 32//2))
        new_y = max(37 + 48//2, min(new_y, FIELD_HEIGHT + 37 - 48//2))

        self.centroid[0] = new_x
        self.centroid[1] = new_y
        self.sprite_pos = [self.centroid[0]-16, self.centroid[1]-24]

    def shoot(self, sprite_sheet, frame_timer, rate):
        if frame_timer%rate ==0:
            x, y = self.centroid
            bullet, bullet2 = Bullet([0, -12], 20, [x-10, y-28], sprite_sheet), Bullet([0, -12], 20, [x+10, y-28], sprite_sheet)
            self.bullets.extend([bullet, bullet2])
    
    def frame_to_display(self, frame_timer):
        frames = self.stand_frame if self.direction==0 else (self.right_frames if self.direction=="right" else self.left_frames)
        current_frame = get_next_frame(frames, frame_timer, self.direction)
        return current_frame
    
    def display_centroid(self, screen):
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        pygame.draw.circle(screen, BLACK, self.centroid, self.radius)
        pygame.draw.circle(screen, WHITE, self.centroid, self.radius-2)

    def update_bullet(self, screen, enemies, background_rect, main_background_edge):
        bullets_to_remove = []
    
        for bullet in self.bullets[:]:
            screen.blit(bullet.sprite[0], bullet.sprite_pos) if bullet.hitbox.colliderect(background_rect) else bullets_to_remove.append(bullet)
            rebuild_background(screen, enemies, main_background_edge)
            bullet.move() if bullet.hitbox.colliderect(background_rect) else bullets_to_remove.append(bullet)
            for enemy in enemies[:]:
                if bullet.hitbox.colliderect(enemy.hitbox):
                    bullets_to_remove.append(bullet)
                    enemy.health -= bullet.damage
        for bullet in bullets_to_remove:
            if bullet in self.bullets:
                self.bullets.remove(bullet)
        remove_outbound_bullets(self.bullets, background_rect)
        

class Enemy:
    def __init__(self, identity, centroid, health, speed, bullets, sprite_sheet):
        self.identity = identity
        self.centroid = centroid
        self.health = health
        self.speed = speed
        self.alpha = 698/health
        self.bullets = bullets
        self.direction = 0
        self.current_path_index = 0
        self.hitbox = pygame.Rect(self.centroid[0]-16, self.centroid[1]-24, 32, 48)
        self.sprite_pos = [centroid[0]-16, centroid[1]-24]
        self.stand_frames = get_sprite_frames(sprite_sheet, 282, 16, 32, 48, 8, "up or down")
        self.right_frames = get_sprite_frames(sprite_sheet, 282, 112, 32, 48, 8, "right")
        self.left_frames = get_sprite_frames(sprite_sheet, 282, 64, 32, 48, 8, "left")

    def move(self, destination):
        start_x, start_y = self.centroid[0], self.centroid[1]
        dest_x, dest_y = destination[0], destination[1]

        dx = dest_x - start_x
        dy = dest_y - start_y
        distance = math.sqrt(dx**2 + dy**2)

        if distance <= self.speed or distance < 1.0:
            self.centroid[0] = dest_x
            self.centroid[1] = dest_y
            self.direction = 0
            self.sprite_pos = [self.centroid[0]-16, self.centroid[1]-24]
            self.hitbox.x, self.hitbox.y = self.centroid[0]-16, self.centroid[1]-24
            return True
        else:
            unit_x = dx / distance
            unit_y = dy / distance
            v_x = unit_x * self.speed
            v_y = unit_y * self.speed
            self.centroid[0] += v_x
            self.centroid[1] += v_y
            self.direction = "right" if v_x > 0 else ("left" if v_x < 0 else 0)
            self.sprite_pos = [self.centroid[0]-16, self.centroid[1]-24]
            self.hitbox.x, self.hitbox.y = self.centroid[0]-16, self.centroid[1]-24
            return False

    def display_health_bar(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (50, 4, 700, 10))
        pygame.draw.rect(screen, (0, 255, 0), (51, 5, self.alpha*self.health, 8))

    def frame_to_display(self, frame_timer):
        frames = self.stand_frames if self.direction==0 else (self.right_frames if self.direction=="right" else self.left_frames)
        current_frame = get_next_frame(frames, frame_timer, self.direction)
        return current_frame
"""

#utils.py
"""
def remove_outbound_bullets(bullets, background_rect):
    # Remove bullets that are out of bounds
    bullets[:] = [bullet for bullet in bullets if bullet.hitbox.colliderect(background_rect)]

def get_sprite_frames(sprite_sheet, start_x, start_y, frame_width, frame_height, num_frames, direction, width_between, debug=False):
    frames = []
    if debug:
        output_dir = "frames"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    for i in range(num_frames):
        x = start_x + (i * width_between)
        y = start_y
        frame_rect = pygame.Rect(x, y, frame_width, frame_height)
        frame = sprite_sheet.subsurface(frame_rect)
        frames.append(frame)
        if debug:
            filename = os.path.join(output_dir, f"{direction}_frame_{i}.png")
            pygame.image.save(frame, filename)
            print(f"Saved {filename}")
    return frames

class Bullet:
    def __init__(self, speed, damage, position, sprite_sheet):
        self.speed = speed
        self.damage = damage
        self.position = position
        self.sprite = [pygame.transform.rotate(frame, 90) for frame in get_sprite_frames(sprite_sheet, 17, 194, 63, 12, 1, "up or down")]
        self.sprite_pos = [position[0]-6, position[1]-(63//2)]
        self.hitbox = pygame.Rect(position[0]-6, position[1]-(63//2), 12, 63)
        
    def move(self):
        self.position[0] += self.speed[0]
        self.position[1] += self.speed[1]
        self.hitbox.x = self.position[0] - 6
        self.hitbox.y = self.position[1] - (63//2)
        self.sprite_pos = [self.position[0]-6, self.position[1]-(63//2)]
        
def move_through_path(enemy, path, current_target_index):
    if current_target_index >= len(path):
        return -1
    current_destination = path[current_target_index]
    reached = enemy.move(current_destination)
    if reached:
        current_target_index += 1
    return current_target_index

def rebuild_background(screen, enemies, main_background_edge):
    screen.blit(main_background_edge, (0, 0))
    for enemy in enemies:
        if enemy.identity == "boss":
            enemy.display_health_bar(screen)
    
def generate_coordinates(n):
    coordinates = []
    for _ in range(n):
        x = random.randint(76, 474)
        y = random.randint(38, 561)
        coordinates.append([x, y])
    return coordinates
"""

#main.py
"""import pygame
from utils import*
from player import*
from enemy import*
from collections import deque

pygame.init()
pygame.mixer.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
FIELD_WIDTH, FIELD_HEIGHT = 400, 525

pygame.display.set_icon(pygame.image.load('Assets\icon.png'))
pygame.display.set_caption("東方風神録2")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
background = load_background_image(WINDOW_WIDTH, WINDOW_HEIGHT)
background_rect = pygame.Rect(75, 37, WINDOW_WIDTH, WINDOW_HEIGHT)
main_background_edge = pygame.image.load('Assets\main_background_edge.png').convert_alpha()
menu, title, start_button, hovered_start_button = load_menu(WINDOW_WIDTH, WINDOW_HEIGHT)
sprite_sheet = pygame.image.load('Assets\spritesheet.png').convert_alpha()

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

#player_init_pos = [(FIELD_WIDTH//2)+75+16, (4*FIELD_HEIGHT//5)+37]
#player = Player(player_init_pos, radius=5, speed=4, bullets=[], sprite_sheet=sprite_sheet)

#enemy = Enemy("boss", [(FIELD_WIDTH//2)+75, 70], 10000, 2, [], sprite_sheet)
Reimu = Enemy01("boss", "Reimu", [300, 300], 10000, 2, pygame.image.load('Assets/enemy_spritesheet2.png').convert_alpha())
path = generate_coordinates(5)
path = deque(path)
enemies = [Reimu]
current_index = 0


pygame.mixer.music.load('Assets\menu_music.mp3')
menu_music = True

running = True
clock = pygame.time.Clock()
game_started = False
frame_timer = 0
current_time = 0
current_stage = 0

while running:
    dt = clock.tick(60)/1000.0
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_started:
            clicked_pos = pygame.mouse.get_pos()
            if start_button.get_rect(topleft=(WINDOW_WIDTH//2 - start_button.get_width()//2, 450)).collidepoint(clicked_pos):
                pygame.mixer.music.stop()
                display_loading_screen(screen)
                game_started = True

    if not game_started:
        if menu_music:
            pygame.mixer.music.set_volume(0.15)
            pygame.mixer.music.play(-1, fade_ms=3000)
        build_menu(screen, menu, title, start_button, hovered_start_button)
        hover_pos = pygame.mouse.get_pos()
        if start_button.get_rect(topleft=(WINDOW_WIDTH//2 - start_button.get_width()//2, 450)).collidepoint(hover_pos):
            screen.blit(hovered_start_button, (WINDOW_WIDTH//2 - hovered_start_button.get_width()//2, 450))
        else:
            screen.blit(start_button, (WINDOW_WIDTH//2 - start_button.get_width()//2, 450))
        menu_music = False

    #Main Game Loop
    if game_started:

        screen.blit(background, (0, 0))

        #Enemy
        for enemy in enemies:
            if path:
                target_position = path[0]
                if enemy.move(target_position):
                    path.popleft()
            current_frame = enemy.update_animation(dt)
            screen.blit(current_frame, )


        #Stage
        

        #Player
        
        player.read_move(keys, FIELD_WIDTH, FIELD_HEIGHT)
        current_frame = player.frame_to_display(frame_timer)
        screen.blit(current_frame, player.sprite_pos)

        if (keys[pygame.K_LSHIFT]):
            player.display_centroid(screen)
        if (keys[pygame.K_z]):
            player.shoot(sprite_sheet, frame_timer, 5)
        player.update_bullet(screen, enemies, background_rect, main_background_edge)

        show_position(screen, player.centroid)
        
        rebuild_background(screen, enemies, main_background_edge)
    pygame.display.flip()
    frame_timer = (frame_timer+1) if frame_timer < 60 else 0
    if frame_timer == 60:
        current_time+=1

pygame.quit()
"""

