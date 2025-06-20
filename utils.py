import pygame
import math
import random


def load_background_image(WINDOW_WIDTH, WINDOW_HEIGHT):
    background = pygame.image.load('Assets/background.png')
    background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))
    return background

def load_menu(WINDOW_WIDTH, WINDOW_HEIGHT):
    menu_background = pygame.image.load('Assets/Menu_resized.jpg')
    sprite_sheet = pygame.image.load('Assets/Menu_items_sheet.png').convert_alpha()
    menu_background = pygame.transform.scale(menu_background, (WINDOW_WIDTH, WINDOW_HEIGHT))
    title_rect = pygame.Rect(45, 550, 507, 105)
    title = sprite_sheet.subsurface(title_rect)
    hovered_start_button_rect = pygame.Rect(693, 49, 148, 28)
    hovered_start_button = sprite_sheet.subsurface(hovered_start_button_rect)
    start_button_rect = pygame.Rect(853, 49, 148, 28)
    start_button = sprite_sheet.subsurface(start_button_rect)
    return menu_background, title, start_button, hovered_start_button

def build_menu(screen, menu, title, start_button, hovered_start_button):
    screen.blit(menu, (0, 0))
    screen.blit(title, (800//2 - title.get_width()//2, 90))
    screen.blit(start_button, (800//2 - start_button.get_width()//2, 450))

def build_sidebar_items(screen, items, player):
    hiscore_text, player_text, power_text, score_text, player_live_icon = items
    screen.blit(hiscore_text, (511, 50))
    screen.blit(score_text, (511, 80))
    screen.blit(player_text, (511, 122))
    for i in range(player.lives):
        screen.blit(player_live_icon, (595+(30*i), 128))
    screen.blit(power_text, (511, 157))
    

def fade(screen, fade_color=(0, 0, 0), out=True):
    fade_surface = pygame.Surface(screen.get_size())
    fade_surface.fill(fade_color)
    for alpha in range(0 if out else 255, 256 if out else -1, 5 if out else -5):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(30)

def display_loading_screen(screen):
    fade(screen, out=True)
    sprite_sheet = pygame.image.load('Assets/Menu_items_sheet.png').convert_alpha()
    loading_text_rect = pygame.Rect(1245, 539, 114, 24)
    loading_text = sprite_sheet.subsurface(loading_text_rect)
    screen.blit(loading_text, ((screen.get_width() - loading_text.get_width()) // 2, (screen.get_height() - loading_text.get_height()) // 2))
    pygame.display.flip()
    for i in range(3):
        pygame.draw.circle(screen, (255, 255, 255), (((screen.get_width() + loading_text.get_width())//2)+ 5+7*i , ((screen.get_height()//2) + loading_text.get_height() - 15)), 2)
        pygame.display.flip()
        pygame.time.delay(500)
    pygame.time.delay(1000)
    
def show_position(screen, player_pos):
    font = pygame.font.Font(None, 22)
    coord_text = font.render(f'X: {int(player_pos[0])}, Y: {int(player_pos[1])}', True, (255, 255, 255))
    screen.blit(coord_text, (0, 578))

def generate_coordinates(n):
    coordinates = []
    for _ in range(n):
        x = random.randint(76, 474)
        y = random.randint(38, 561)
        coordinates.append([x, y])
    return coordinates

def load_frames(surface, specs, status, debug=False):
    #Return the frames into a list of images
    sub_photos = []
    for i, spec in enumerate(specs):
        start_x, start_y, width, height = spec
        rect = pygame.Rect(start_x, start_y, width, height)
        sub_surface = surface.subsurface(rect)
        sub_photos.append(sub_surface)
        if debug:
            save_path = "debug_sprites/"
            pygame.image.save(sub_surface, f"{save_path}{status}sprite_{i}.png")
    return sub_photos

class Hitbox:
    #Hitbox object with OBB method
    def __init__(self, center: list, width, height, angle, circle=False):
        self.center = center
        self.width = width
        self.height = height
        self.angle = angle #degree
        self.circle = circle

        self.points = self.calculate_corners()

    def calculate_corners(self):
        """Calculate the corners of the OBB based on the center, width, height, and angle."""
        rad = math.radians(self.angle)
        hw = self.width // 2
        hh = self.height // 2

        corners = [
            (self.center[0] - hw * math.cos(rad) - hh * math.sin(rad),
             self.center[1] + hw * math.sin(rad) - hh * math.cos(rad)),
            (self.center[0] + hw * math.cos(rad) - hh * math.sin(rad),
             self.center[1] - hw * math.sin(rad) - hh * math.cos(rad)),
            (self.center[0] + hw * math.cos(rad) + hh * math.sin(rad),
             self.center[1] - hw * math.sin(rad) + hh * math.cos(rad)),
            (self.center[0] - hw * math.cos(rad) + hh * math.sin(rad),
             self.center[1] + hw * math.sin(rad) + hh * math.cos(rad))]
        return corners

    def display_hitbox(self, screen):
        #Show the exact hitbox
        pygame.draw.polygon(screen, (255, 0, 0), self.points, 1) 

    def update(self):
        #Recalculate the corners
        self.points = self.calculate_corners()

    def collides_with(self, other, check_contain=False):
        #Check collision for both Hitbox objects
        edges1 = [
            (self.points[1][0] - self.points[0][0], self.points[1][1] - self.points[0][1]),
            (self.points[2][0] - self.points[1][0], self.points[2][1] - self.points[1][1]),]
        edges2 = [
            (other.points[1][0] - other.points[0][0], other.points[1][1] - other.points[0][1]),
            (other.points[2][0] - other.points[1][0], other.points[2][1] - other.points[1][1]),]
        axes = [(edges1[0][1], -edges1[0][0]), (edges1[1][1], -edges1[1][0]), (edges2[0][1], -edges2[0][0]), (edges2[1][1], -edges2[1][0]),]
        
        if check_contain:
            # Project all points onto each axis
            for axis in axes:
                mag = math.sqrt(axis[0]**2 + axis[1]**2)
                if mag == 0:
                    continue
                axis = (axis[0] / mag, axis[1] / mag)
            
                # Project points of both rectangles
                proj1 = [self.points[i][0] * axis[0] + self.points[i][1] * axis[1] for i in range(4)]
                proj2 = [other.points[i][0] * axis[0] + other.points[i][1] * axis[1] for i in range(4)]
            
                min1, max1 = min(proj1), max(proj1)
                min2, max2 = min(proj2), max(proj2)
            
                # For containment, self's projection must be fully inside other's projection
                if not (min2 <= min1 and max1 <= max2):
                    return False
        
            # Additional check: ensure no edges of self intersect edges of other
            def line_segments_intersect(p1, p2, q1, q2):
                def ccw(A, B, C):
                    return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])
                return (ccw(p1, q1, q2) != ccw(p2, q1, q2) and 
                        ccw(p1, p2, q1) != ccw(p1, p2, q2))
        
            for i in range(4):
                for j in range(4):
                    p1 = self.points[i]
                    p2 = self.points[(i + 1) % 4]
                    q1 = other.points[j]
                    q2 = other.points[(j + 1) % 4]
                    if line_segments_intersect(p1, p2, q1, q2):
                        return False
        
            return True
    
        # Original collision detection logic
        else:
            for axis in axes:
                mag = math.sqrt(axis[0]**2 + axis[1]**2)
                if mag == 0:
                    continue
                axis = (axis[0] / mag, axis[1] / mag)
                proj1 = [self.points[i][0] * axis[0] + self.points[i][1] * axis[1] for i in range(4)]
                proj2 = [other.points[i][0] * axis[0] + other.points[i][1] * axis[1] for i in range(4)]
            
                min1, max1 = min(proj1), max(proj1)
                min2, max2 = min(proj2), max(proj2)
                if max1 < min2 or max2 < min1:
                    return False
            return True

Sanae_A_Bullets = [[3, 163, 59, 9], [67, 163, 59, 10], [131, 163, 59, 10], [195, 163, 59, 10]]
Sanae_B_Bullets = [[196, 177, 60, 14]]
Reimu_Bullets = [[40, 512, 14, 16]]

class Bullet:

    def __init__(self, shooter, speed, damage, centroid: list, angle, sprite_sheet):
        #Bullet basic data
        self.shooter = shooter
        self.speed = speed
        self.damage = damage
        self.centroid = centroid
        self.angle = angle #degree

        #Bullet frames data
        if self.shooter == "player":
            self.bullet_set = Sanae_A_Bullets
        else:
            self.bullet_set = Reimu_Bullets
        self.frames = load_frames(sprite_sheet, self.bullet_set, "bullet")
        self.frame_idx = 0
        self.frame_timer = 0
        self.sprite_pos = [self.centroid[0] - self.frames[self.frame_idx].get_width()//2, self.centroid[1] - self.frames[self.frame_idx].get_height()//2]

        #Bullet hitbox
        self.hitbox = Hitbox(self.centroid, self.frames[self.frame_idx].get_width(), self.frames[self.frame_idx].get_height(), angle)

        self.frames = [pygame.transform.rotate(image, angle) for image in self.frames]
        

    def update_sprite_pos(self):
        self.sprite_pos = [self.centroid[0] - self.frames[self.frame_idx].get_width()//2, self.centroid[1] - self.frames[self.frame_idx].get_height()//2]

    def draw(self, dt, screen, frame_duration = 0.1):
        #Return the exact image to display
        self.frame_timer+=dt

        if self.frame_timer >= frame_duration:
            self.frame_idx += int(self.frame_timer // frame_duration)
            self.frame_timer %= frame_duration
            self.frame_idx %= len(self.frames)

        screen.blit(self.frames[self.frame_idx], (self.sprite_pos[0], self.sprite_pos[1]))

def update_bullets(bullets, player, enemies):
    #Update every attribute for every bullets
    bullets_to_remove = []

    for bullet in bullets:
        dx, dy = bullet.speed*math.cos(math.radians(bullet.angle)), -bullet.speed*math.sin(math.radians(bullet.angle))
        bullet.centroid = [bullet.centroid[0]+dx, bullet.centroid[1]+dy]
        bullet.hitbox.center = [bullet.hitbox.center[0]+dx, bullet.hitbox.center[1]+dy]
        bullet.hitbox.update()
        bullet.update_sprite_pos()
        
        for enemy in enemies:
            if bullet.hitbox.collides_with(enemy.hitbox) and bullet.shooter == "player":
                enemy.health -= bullet.damage
                bullet.damage = 0
                bullets_to_remove.append(bullet)
                
        if bullet.hitbox.collides_with(player.hitbox) and bullet.shooter in ("boss", "fairy"):
            player.lives -= 1
            bullets_to_remove.append(bullet)
        
    for bullet in bullets_to_remove:
        bullets.remove(bullet)

    return bullets

class Dummy:
    def __init__(self, center, color):
        self.hitbox = Hitbox(center, 40, 40, 0)
        self.color = color
        self.lives = 3
        self.health = 10

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.hitbox.center[0]), int(self.hitbox.center[1])), 20)

def fire_rate_limitation(dt: float, rate: float, entity) -> bool:
    if not hasattr(entity, 'last_shot_time'):
        entity.last_shot_time = 0.0
    
    entity.last_shot_time += dt
    if entity.last_shot_time >= rate:
        entity.last_shot_time -= rate  # Reset, keeping remainder
        return True
    return False



