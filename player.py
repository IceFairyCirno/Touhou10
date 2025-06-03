import pygame
import math
import os
from utils import *

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

        new_x = max(75 + self.radius, min(new_x, FIELD_WIDTH + 75 - self.radius))
        new_y = max(37 + self.radius, min(new_y, FIELD_HEIGHT + 37 - self.radius))

        self.centroid[0] = new_x
        self.centroid[1] = new_y
        self.sprite_pos = [self.centroid[0]-16, self.centroid[1]-24]

    def shoot(self, sprite_sheet, frame_timer):
        if frame_timer%10 ==0:
            bullet = Bullet([0, -12],70, [self.centroid[0], self.centroid[1]-28], sprite_sheet)
            self.bullets.append(bullet)
    
    def frame_to_display(self, frame_timer):
        frames = self.stand_frame if self.direction==0 else (self.right_frames if self.direction=="right" else self.left_frames)
        current_frame = get_next_frame(frames, frame_timer, self.direction)
        return current_frame
    
    def display_centroid(self, screen):
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        pygame.draw.circle(screen, BLACK, self.centroid, self.radius)
        pygame.draw.circle(screen, WHITE, self.centroid, self.radius-2)

    def update_bullet(self, screen, enemys):
        for bullet in self.bullets:
            screen.blit(bullet.sprite[0], bullet.sprite_pos)
            bullet.move()
            for enemy in enemys:
                if bullet.hitbox.colliderect(enemy.hitbox):
                    self.bullets.remove(bullet)
                    enemy.health -=10
            remove_outbound_bullets(self.bullets, 400, 525)
        


    
class Enemy:
    def __init__(self, identity, centroid, health, speed, bullets, sprite_sheet):
        self.identity = identity
        self.centroid = centroid
        self.health = health
        self.speed = speed
        self.alpha = 698/health
        self.bullets = bullets
        self.direction = 0
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

    

    


