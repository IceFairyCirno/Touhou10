import pygame
from utils import *

reimu_default_frames = [[576, 1580, 41, 72], [640, 1580, 41, 72], [704, 1580, 41, 72], [768, 1580, 41, 72]]
reimu_right_frames = [[574, 1660, 42, 72], [629, 1660, 54, 72], [694, 1663, 56, 63], [758, 1663, 56, 63]]
reimu_attack_frames = [[566, 1740, 51, 72], [631, 1740, 51, 72], [703, 1740, 54, 72], [768, 1738, 51, 75]]

marisa_default_frames = [[581, 1881, 53, 62], [645, 1881, 53, 62], [708, 1881, 53, 62], [773, 1881, 53, 62]]
marisa_right_frames = [[579, 1964, 56, 60], [644, 1964, 55, 55], [710, 1960, 52, 59], [773, 1961, 53, 57]]
marisa_attack_frames = [[581, 2041, 53, 64]]

blue_fairy_default_frames = [[49 ,1383, 30, 30], [82, 1383, 30, 30], [113, 1383, 30, 30], [145, 1383, 30, 30], [177, 1383, 30, 30]]
blue_fairy_right_frames = [[210, 1383, 30, 30], [241, 1383, 30, 30], [274, 1383, 30, 30], [307, 1383, 30, 30], [338, 1383, 30, 30], [369, 1383, 30, 30], [402, 1383, 30, 30]]

Patterns = {
    "flower": [(base_angle + offset) % 360 for base_angle in range(0, 360, 45) for offset in [-10, 0, 10]], 
    "double spiral": [(270 + angle) % 360 for angle in range(0, 180, 18)] + [(270 + 180 + angle) % 360 for angle in range(0, 180, 18)],
    "star": [(base_angle + offset) % 360 for base_angle in range(0, 360, 72) for offset in [-8, 0, 8]],
    "chaos": [random.uniform(0, 360) for _ in range(10)]
}

class Enemy:
    def __init__(self, identity, name, centroid, health, speed, sprite_sheet, frame_duration=0.1):
        self.identity = identity
        self.name = name
        self.centroid = centroid
        self.health = health
        self.speed = speed
        self.sprite_sheet = sprite_sheet
        self.frame_duration = frame_duration
        
        self.current_frame = 0
        self.frame_timer = 0
        self.state = "default"  # States: "default", "attacking", "turning_left", "turning_right", "reversing_left", "reversing_right"
        self.movement = "stopped"  # Movement: "stopped", "vertical", "left", "right"
        self.attack = False

        if self.identity == "boss":
            self.health_factor = 698 / health
            if self.name == "Reimu":
                self.default_frames = load_frames(sprite_sheet, reimu_default_frames, status="default")
                self.right_frames = load_frames(sprite_sheet, reimu_right_frames, status="right")
                self.left_frames = [pygame.transform.flip(frame, True, False) for frame in self.right_frames]
                self.attack_frames = load_frames(sprite_sheet, reimu_attack_frames, status="attack")
                self.current_frames = self.default_frames
                self.hitbox = Hitbox(self.centroid, self.current_frames[0].get_width(), self.current_frames[0].get_height(), 0)
            if self.name == "Marisa":
                self.default_frames = load_frames(sprite_sheet, marisa_default_frames)
                self.right_frames = load_frames(sprite_sheet, marisa_right_frames)
                self.left_frames = [pygame.transform.flip(frame, True, False) for frame in self.right_frames]
                self.attack_frames = load_frames(sprite_sheet, marisa_attack_frames)
                self.current_frames = self.default_frames
                self.hitbox = Hitbox(self.centroid, self.current_frames[0].get_width(), self.current_frames[0].get_height(), 0)
        elif self.identity == "fairy":
            if self.name == "Blue Fairy":
                self.default_frames = load_frames(sprite_sheet, blue_fairy_default_frames)
                self.right_frames = load_frames(sprite_sheet, blue_fairy_right_frames)
                self.left_frames = [pygame.transform.flip(frame, True, False) for frame in self.right_frames]
                self.attack_frames = self.default_frames  # no attack frames for Blue Fairy
                self.current_frames = self.default_frames
                self.hitbox = Hitbox(self.centroid, self.current_frames[0].get_width(), self.current_frames[0].get_height(), 0)

    def move(self, destination):
        start_x, start_y = self.centroid[0], self.centroid[1]
        dest_x, dest_y = destination[0], destination[1]

        dx, dy = dest_x-start_x, dest_y - start_y
        distance = math.sqrt(dx**2 + dy**2)

        if distance <= self.speed or distance < 1.0:
            self.centroid[0] = dest_x
            self.centroid[1] = dest_y
            self.hitbox.center = self.centroid
            self.hitbox.update()
            self.movement = "stopped"
            return True
        else:
            unit_x, unit_y = dx / distance, dy / distance
            v_x, v_y = unit_x * self.speed, unit_y * self.speed
            self.centroid[0] += v_x
            self.centroid[1] += v_y
            self.hitbox.center = self.centroid
            self.hitbox.update()
            if v_x == 0:
                self.movement = "vertical"
            elif v_x > 0:
                self.movement = "right"
            elif v_x < 0:
                self.movement = "left"
            return False
        
    def display_health_bar(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (50, 4, 700, 10))
        pygame.draw.rect(screen, (0, 255, 0), (51, 5, self.health_factor*self.health, 8))

    def change_state(self):
        #Support function for draw()
        if self.attack:
            if self.state != "attacking":
                self.state = "attacking"
                self.current_frames = self.attack_frames
                self.current_frame = 0
            return

        # Handle stopped or vertical movement
        if self.movement in ["stopped", "vertical"]:
            if self.state in ["turning_left", "turning_right"] and self.current_frame >= len(self.current_frames) - 1:
                # Start reverse animation when turn is complete
                self.state = "reversing_left" if self.state == "turning_left" else "reversing_right"
                self.current_frame = len(self.current_frames) - 1
            elif self.state in ["reversing_left", "reversing_right"]:
                # Continue reversing until draw handles frame 0
                pass
            elif self.state != "default":
                # Transition to default state only if not already default
                self.state = "default"
                self.current_frames = self.default_frames
                self.current_frame = 0
        # Handle horizontal movement
        elif self.movement == "left" and self.state != "turning_left":
            self.state = "turning_left"
            self.current_frames = self.left_frames
            self.current_frame = 0
        elif self.movement == "right" and self.state != "turning_right":
            self.state = "turning_right"
            self.current_frames = self.right_frames
            self.current_frame = 0
    
    def draw(self, dt, screen):
        self.frame_timer += dt

        self.change_state()

        # Update frame for current animation
        if self.frame_timer >= self.frame_duration:
            if self.state in ["default", "attacking"]:
                # Loop default or attack animation
                self.current_frame = (self.current_frame + 1) % len(self.current_frames)
            elif self.state in ["turning_left", "turning_right"]:
                # Play turning animation once
                self.current_frame += 1
                if self.current_frame >= len(self.current_frames):
                    self.current_frame = len(self.current_frames) - 1  # Stay on last frame
            elif self.state in ["reversing_left", "reversing_right"]:
                # Play reverse animation
                self.current_frame -= 1
                if self.current_frame < 0:
                    self.state = "default"
                    self.current_frames = self.default_frames
                    self.current_frame = 0
            self.frame_timer = 0

        
        sprite_pos = (self.centroid[0]-(self.current_frames[self.current_frame].get_width()//2), self.centroid[1]-(self.current_frames[self.current_frame].get_height()//2))
        screen.blit(self.current_frames[self.current_frame], sprite_pos)
    
    def move_by_path(self, path):
        if path:
            target_position = path[0]
            if self.move(target_position):
                self.movement = "stopped"
                if not self.attack:
                    self.attack = True
                    self.timer_start = pygame.time.get_ticks()
            if self.attack and (pygame.time.get_ticks() - self.timer_start >= 2000):
                self.attack = False
                path.popleft()
        return path
    
    def shoot(self, bullets, sprite_sheet):
        if self.attack == True:
            pattern = random.choice(["star", "double spiral", "chaos", "flower"])
            for angle in Patterns[pattern]:
                bullet = Bullet("enemy", 5, 5, self.centroid, angle, sprite_sheet)
                bullets.append(bullet)




    

            
            