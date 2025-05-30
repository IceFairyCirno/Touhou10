import pygame
import math
import os

class Player:
    def __init__(self, centroid, radius, sprite_pos, speed, bullets, direction):
        self.centroid = centroid
        self.radius = radius
        self.sprite_pos = sprite_pos
        self.speed = speed
        self.bullets = bullets
        self.direction = 0
    
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

        new_x = max(39 + self.radius, min(new_x, FIELD_WIDTH + 41 - self.radius))
        new_y = max(21 + self.radius, min(new_y, FIELD_HEIGHT + 21 - self.radius))

        self.centroid[0] = new_x
        self.centroid[1] = new_y
        self.sprite_pos = [self.centroid[0]-16, self.centroid[1]-24]

    def shoot(self):
        bullet = pygame.Rect(self.centroid[0], self.centroid[1]-28, 3, 3)
        speed = [0, -12]
        self.bullets.append((bullet, speed))
    
