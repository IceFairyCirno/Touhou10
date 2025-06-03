import pygame
import math
import os
import random

def set_background(WINDOW_WIDTH, WINDOW_HEIGHT):
    background = pygame.image.load('Assets\main_background.png')
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(background, (0, 0))
    return screen, background

def show_position(screen, player_pos):
    font = pygame.font.Font(None, 22)
    coord_text = font.render(f'X: {int(player_pos[0])}, Y: {int(player_pos[1])}', True, (255, 255, 255))
    screen.blit(coord_text, (0, 578))

def remove_outbound_bullets(bullets, FIELD_WIDTH, FIELD_HEIGHT):
    bullets[:] = [bullet for bullet in bullets if 75+8 <= bullet.position[0] <= FIELD_WIDTH + 75+8 and 37+8 <= bullet.position[1] <= FIELD_HEIGHT + 37+8]

def get_sprite_frames(sprite_sheet, start_x, start_y, frame_width, frame_height, num_frames, direction, debug=False):
    frames = []
    if debug:
        output_dir = "frames"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    for i in range(num_frames):
        x = start_x + (i * frame_width)
        y = start_y
        frame_rect = pygame.Rect(x, y, frame_width, frame_height)
        frame = sprite_sheet.subsurface(frame_rect)
        frames.append(frame)
        if debug:
            filename = os.path.join(output_dir, f"{direction}_frame_{i}.png")
            pygame.image.save(frame, filename)
            print(f"Saved {filename}")
    return frames

def get_next_frame(frames, frame_timer, direction):
    frame_index=0
    if direction==0:
        frame_index = min(int(frame_timer / 7.5), 7)
    else:
        frame_index = (int(frame_timer / 7.5) % 5) + 3
    return frames[frame_index]

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

    
    







        


