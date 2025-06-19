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
            attack_frames (list): List of frames for attack animation (looped when stopped and attacking)
            frame_duration (float): Time (in seconds) to display each frame
        """
        self.default_frames = default_frames
        self.left_frames = left_frames
        self.right_frames = right_frames
        self.attack_frames = attack_frames
        self.frame_duration = frame_duration
        
        self.current_frame = 0
        self.frame_timer = 0
        self.state = "stopped" # stopped, turing, attack
        self.direction = None # right, left, None
        self.current_frames = self.default_frames

    def draw(self, dt):
        
        self.frame_timer += dt

        if self.state == "attack" and self.direction == None:
            self.current_frame = 0
            self.current_frames = self.attack_frames
        elif self.state == "stopped" and self.direction == None:
            self.current_frames = self.default_frames
        elif self.direction in ("right", "left"):
            frames = self.right_frames if self.direction == "right" else self.left_frames
            if self.state == "turning":
                self.current_frames = frames[::-1]
                self.current_frame = 0
            else:
                self.current_frames = frames
                self.current_frame = 0


        if self.frame_timer >= self.frame_duration:
            if (self.state in ("stopped", "attack") and self.direction == None) or self.state == "turning":
                self.current_frame = ((self.current_frame + 1) % len(self.current_frames)) if self.state != "turning" else self.current_frame + 1
                if self.current_frame == len(self.current_frames) - 1 and self.state == "turning":
                    self.state = "stopped"
                    self.direction = None
            if self.state != "turning" and self.direction in ("right", "left"):
                self.current_frame += 1
                if self.current_frame >= len(self.current_frames):
                    self.current_frame = len(self.current_frames) - 1
            self.frame_timer = 0

        

        return self.current_frames[self.current_frame]

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
        keys = pygame.key.get_pressed()

        # Handle input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if keys[pygame.K_LEFT]:
            enemy.direction = "left"
        if keys[pygame.K_RIGHT]:
            enemy.direction = "right"
        if keys[pygame.K_UP] or keys[pygame.K_DOWN]:
            enemy.direction = None
            enemy.state = "stopped"
        if keys[pygame.K_z]:
            enemy.state = "turning"
        # Update enemy animation
        current_frame = enemy.draw(dt)

        # Clear screen
        screen.fill((0, 0, 0))  # Black background

        # Render current frame
        screen.blit(current_frame, (SCREEN_WIDTH // 2 - current_frame.get_width() // 2, 
                                  SCREEN_HEIGHT // 2 - current_frame.get_height() // 2))

        # Display current state and movement
        font = pygame.font.Font(None, 36)
        state_text = font.render(f"State: {enemy.state}", True, (255, 255, 255))
        screen.blit(state_text, (50, 50))
        movement_text = font.render(f"Direction: {enemy.direction}", True, (255, 255, 255))
        screen.blit(movement_text, (50, 80))

        # Instructions
        instructions = [
            "Controls:",
            "UP/DOWN: Vertical movement (default animation)",
            "LEFT/RIGHT: Horizontal movement (turn left/right)",
            "SPACE: Toggle attack when stopped",
            "Release keys: Stop movement"
        ]
        for i, line in enumerate(instructions):
            instr_text = font.render(line, True, (255, 255, 255))
            screen.blit(instr_text, (50, 150 + i * 30))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()