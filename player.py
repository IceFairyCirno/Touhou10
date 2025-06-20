import pygame
from utils import load_frames, Hitbox, Bullet

Sanae_default_frames = [[3, 3, 26, 44], [35, 3, 26, 44], [67, 3, 26, 44], [99, 3, 26, 44], [131, 3, 26, 44], [163, 3, 26, 44], [195, 3, 26, 44], [227, 3, 26, 44]]
Sanae_left_frames = [[3, 53, 26, 40], [33, 53, 28, 41], [64, 53, 27, 40], [99, 53, 28, 41], [131, 53, 28, 41], [163, 53, 28, 41], [195, 53, 28, 41], [227, 53, 28, 41]]
Sanae_right_frames = [[5, 101, 26, 40], [37, 101, 28, 41], [68, 102, 27, 40], [99, 102, 28, 41], [131, 102, 28, 41], [163, 102, 28, 41], [195, 102, 28, 41], [227, 102, 28, 41]]

class Player():
    def __init__(self, centroid: list, radius, speed, lives, spellcard, sprite_sheet, frame_duration = 0.1):
        #Player basic data
        self.centroid = centroid
        self.radius = radius
        self.speed = speed
        self.lives = lives
        self.spellcard = spellcard

        #Player sprite data
        self.sprite_sheet = sprite_sheet
        self.default_frames = load_frames(sprite_sheet, Sanae_default_frames, "default")
        self.right_frames = load_frames(sprite_sheet, Sanae_right_frames, "right")
        self.left_frames = load_frames(sprite_sheet, Sanae_left_frames, "left")
        self.current_frames = self.default_frames
        self.current_frame = 0

        #Player position data (change based on centroid)
        sprite_image = self.current_frames[self.current_frame]
        self.sprite_pos = [self.centroid[0] - sprite_image.get_width()//2, self.centroid[1] - sprite_image.get_height()//2]
        self.hitbox = Hitbox(self.centroid, 2*self.radius -1, 2*self.radius -1, 90)

        #Player animation data
        self.frame_timer = 0.0
        self.frame_duration = frame_duration
        self.play_once = False  # Whether to play animation once then loop last 4 frames
        self.has_played_once = False  # Tracks if single playthrough is done
        self.status = "stationary"  # Movement state: stationary, up, down, right, left, up_right, up_left, down_right, down_left
        self.prev_status = "stationary"
        self.is_last_four = False

    def update_positions(self):
        #Update the positions
        sprite_image = self.current_frames[self.current_frame]
        self.sprite_pos = [self.centroid[0] - sprite_image.get_width()//2, self.centroid[1] - sprite_image.get_height()//2]
        self.hitbox.center = self.centroid
        self.hitbox.update()

    def draw(self, dt: float, screen: pygame.Surface):
        # Update frame timer
        self.frame_timer += dt

        # Check if transitioning to stationary/up/down from right/left/diagonal
        if self.status in ("stationary", "up", "down") and self.prev_status not in ("stationary", "up", "down"):
            self.current_frame = 0
            self.frame_timer = 0.0
            self.is_last_four = False

        # Determine animation based on status
        if self.status in ("stationary", "up", "down"):
            self.current_frames = self.default_frames
            self.is_last_four = False
        elif self.status in ("right", "up_right", "down_right"):
            self.current_frames = self.right_frames
            self.is_last_four = True
            self.current_frame = 4 + (self.current_frame % 4)  # Restrict to frames 4–7
        elif self.status in ("left", "up_left", "down_left"):
            self.current_frames = self.left_frames
            self.is_last_four = True
            self.current_frame = 4 + (self.current_frame % 4)  # Restrict to frames 4–7

        # Update frame index based on frame_timer
        while self.frame_timer >= self.frame_duration:
            self.frame_timer -= self.frame_duration
            self.current_frame += 1
            if self.is_last_four:
                self.current_frame = 4 + (self.current_frame % 4)  # Loop frames 4–7
            else:
                self.current_frame %= 8  # Loop all 8 frames

        # Blit current frame
        frame_index = int(self.current_frame) % 8
        screen.blit(self.current_frames[frame_index], self.sprite_pos)

        # Update previous status
        self.prev_status = self.status
    
    def read_move(self, keys, field_box, screen):
        dy, dx = 0, 0
        speed = self.speed
        #Slower is pressed left shift
        if keys[pygame.K_LSHIFT]:
            speed = self.speed - 2
            self.display_centroid(screen)

        #Check keys and update status
        self.status = "stationary"
        if keys[pygame.K_LEFT]:
            dx -= speed
            self.status = "left"
        if keys[pygame.K_RIGHT]:
            dx += speed
            self.status = "right"
        if keys[pygame.K_UP]:
            dy -= speed 
            self.status = "up"
        if keys[pygame.K_DOWN]:
            dy += speed
            self.status = "down"
        if not any(pygame.key.get_pressed()[i] for i in {pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT}):
            self.status = "stationary"

        #Adjust diagonal movement
        if dx != 0 and dy != 0:
            diagonal_factor = speed / (2 ** 0.5)
            dx *= diagonal_factor / speed
            dy *= diagonal_factor / speed
            self.status = "left" if dx < 0 else "right"

        #Define new positions
        new_centroid = [self.centroid[0] + dx, self.centroid[1] + dy]
        new_hitbox = Hitbox(new_centroid, 2*self.radius -1, 2*self.radius -1, 90)

        #Check validity
        valid_move = False
        if new_hitbox.collides_with(field_box, check_contain=True):
            valid_move = True
        
        #Update everything
        if valid_move:
            self.centroid = new_centroid
            self.update_positions()

    def shoot(self, bullets):
        bullet_positions = [[self.centroid[0]-12, self.centroid[1]-10],
                            [self.centroid[0]+12, self.centroid[1]-10]]
        for bullet_pos in bullet_positions:
            bullet = Bullet("player", speed=12, damage=3, centroid=bullet_pos, angle=90, sprite_sheet=self.sprite_sheet)
            bullets.append(bullet)

    def display_centroid(self, screen):
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        pygame.draw.circle(screen, BLACK, self.centroid, self.radius)
        pygame.draw.circle(screen, WHITE, self.centroid, self.radius-2)

    


