import pygame

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Draw Circle on Left Shift")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(WHITE)

    # Check if left Shift is being held
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LSHIFT]:
        # Draw a red circle at the center of the screen
        pygame.draw.circle(screen, RED, (400, 300), 50)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()