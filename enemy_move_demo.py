import pygame
from utils import load_frames

class Enemy:
    def __init__(self, default_frames, left_frames, right_frames, attack_frames, frame_duration=0.1):
        """
        Initialize the Enemy with animation frames and timing.
        
        Args:
            default_frames (list): List of frames for default animation (looped)
            left_frames (list): List of frames for turning left
            right_frames (list): List of frames for turning right
            attack_frames (list): List of frames for attack animation (looped when attacking)
            frame_duration (float): Time (in seconds) to display each frame
        """
        self.default_frames = default_frames
        self.left_frames = left_frames
        self.right_frames = right_frames
        self.attack_frames = attack_frames
        self.frame_duration = frame_duration
        
        self.current_frame = 0
        self.frame_timer = 0
        self.state = "default"  # States: "default", "attacking", "turning_left", "turning_right", "reversing_left", "reversing_right"
        self.movement = "stopped"  # Movement: "stopped", "vertical", "left", "right"
        self.attack = False  # Attack state
        self.current_frames = self.default_frames

    def change_state(self):
        """
        Update the animation state and frames based on movement and attack status.
        """
        # Prioritize attacking state
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

        # Draw current frame to screen
        screen.blit(self.current_frames[self.current_frame],
                    (SCREEN_WIDTH // 2 - self.current_frames[self.current_frame].get_width() // 2,
                     SCREEN_HEIGHT // 2 - self.current_frames[self.current_frame].get_height() // 2))

# Frame coordinates
reimu_default_frames = [[576, 1580, 41, 72], [640, 1580, 41, 72], [704, 1580, 41, 72], [768, 1580, 41, 72]]
reimu_right_frames = [[574, 1660, 42, 72], [629, 1660, 54, 72], [694, 1663, 56, 63], [758, 1663, 56, 63]]
reimu_attack_frames = [[566, 1740, 51, 72], [631, 1740, 51, 72], [703, 1740, 54, 72], [768, 1738, 51, 75]]

# Pygame setup
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Enemy Animation Demo")
clock = pygame.time.Clock()
FPS = 60

# Load sprite sheet and frames
sprite_sheet = pygame.image.load('Assets/boss_spritesheet.png').convert_alpha()
DEFAULT_FRAMES = load_frames(sprite_sheet, reimu_default_frames, status="default")
RIGHT_FRAMES = load_frames(sprite_sheet, reimu_right_frames, status="default")
LEFT_FRAMES = [pygame.transform.flip(frame, True, False) for frame in RIGHT_FRAMES]
ATTACK_FRAMES = load_frames(sprite_sheet, reimu_attack_frames, status="default")

# Initialize enemy
enemy = Enemy(DEFAULT_FRAMES, LEFT_FRAMES, RIGHT_FRAMES, ATTACK_FRAMES, frame_duration=0.1)

def main():
    """Main game loop for the demo."""
    running = True
    keys_pressed = {pygame.K_LEFT: False, pygame.K_RIGHT: False, pygame.K_UP: False, pygame.K_DOWN: False, pygame.K_SPACE: False}

    while running:
        dt = clock.tick(FPS) / 1000.0  # Delta time in seconds

        # Handle input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in keys_pressed:
                    keys_pressed[event.key] = True
                if event.key == pygame.K_SPACE:
                    enemy.attack = not enemy.attack  # Toggle attack state
            elif event.type == pygame.KEYUP:
                if event.key in keys_pressed:
                    keys_pressed[event.key] = False

        # Update movement and attack state based on key presses
        if keys_pressed[pygame.K_LEFT]:
            enemy.movement = "left"
            enemy.attack = False
        elif keys_pressed[pygame.K_RIGHT]:
            enemy.movement = "right"
            enemy.attack = False
        elif keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_DOWN]:
            enemy.movement = "vertical"
            enemy.attack = False
        else:
            enemy.movement = "stopped"

        # Clear screen
        screen.fill((0, 0, 0))  # Black background

        # Update and draw enemy animation
        enemy.draw(dt, screen)

        # Display current state
        font = pygame.font.Font(None, 36)
        state_text = font.render(f"State: {enemy.state}", True, (255, 255, 255))
        screen.blit(state_text, (50, 50))
        movement_text = font.render(f"Movement: {enemy.movement}", True, (255, 255, 255))
        screen.blit(movement_text, (50, 80))
        attack_text = font.render(f"Attacking: {enemy.attack}", True, (255, 255, 255))
        screen.blit(attack_text, (50, 110))

        # Instructions
        instructions = [
            "Controls:",
            "UP/DOWN: Vertical movement (loop default frames)",
            "LEFT/RIGHT: Horizontal movement (play turn frames once)",
            "SPACE: Toggle attack (loop attack frames)",
            "Release keys: Stop (loop default or reverse turn)"
        ]
        for i, line in enumerate(instructions):
            instr_text = font.render(line, True, (255, 255, 255))
            screen.blit(instr_text, (50, 150 + i * 30))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
