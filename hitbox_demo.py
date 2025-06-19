import pygame
import math

class Hitbox:
    #Hitbox object with OBB method

    def __init__(self, center, width, height, angle):
        self.center = center
        self.width = width
        self.height = height
        self.angle = angle    #In degrees

        self.points = self.calculate_corners()

    def calculate_corners(self):
        """Calculate the corners of the OBB based on the center, width, height, and angle."""
        rad = math.radians(self.angle)
        hw = self.width / 2
        hh = self.height / 2

        corners = [
            (self.center[0] - hw * math.cos(rad) - hh * math.sin(rad),
             self.center[1] + hw * math.sin(rad) - hh * math.cos(rad)),
            (self.center[0] + hw * math.cos(rad) - hh * math.sin(rad),
             self.center[1] - hw * math.sin(rad) - hh * math.cos(rad)),
            (self.center[0] + hw * math.cos(rad) + hh * math.sin(rad),
             self.center[1] - hw * math.sin(rad) + hh * math.cos(rad)),
            (self.center[0] - hw * math.cos(rad) + hh * math.sin(rad),
             self.center[1] + hw * math.sin(rad) + hh * math.cos(rad)),
        ]
        return corners

    def display_hitbox(self, screen):
        #Show the exact hitbox
        pygame.draw.polygon(screen, (255, 0, 0), self.points, 1) 

    def update(self):
        #Recalculate the corners
        self.points = self.calculate_corners()

    def collides_with(self, other):

        if len(self.points) != 4 or len(other.points) != 4:
            raise ValueError("Each OBB must have exactly 4 corners")

        # Calculate edges for both OBBs
        edges1 = [
            (self.points[1][0] - self.points[0][0], self.points[1][1] - self.points[0][1]),  # Edge 0->1
            (self.points[2][0] - self.points[1][0], self.points[2][1] - self.points[1][1]),  # Edge 1->2
        ]
        edges2 = [
            (other.points[1][0] - other.points[0][0], other.points[1][1] - other.points[0][1]),  # Edge 0->1
            (other.points[2][0] - other.points[1][0], other.points[2][1] - other.points[1][1]),  # Edge 1->2
        ]

        # Get axes (normals to edges)
        axes = [
            (edges1[0][1], -edges1[0][0]),  # Normal to edge 0->1
            (edges1[1][1], -edges1[1][0]),  # Normal to edge 1->2
            (edges2[0][1], -edges2[0][0]),  # Normal to edge 0->1
            (edges2[1][1], -edges2[1][0]),  # Normal to edge 1->2
        ]

        # Test each axis
        for axis in axes:
            # Normalize axis to avoid scaling issues (optional, but improves robustness)
            mag = math.sqrt(axis[0]**2 + axis[1]**2)
            if mag == 0:
                continue  # Skip degenerate axis
            axis = (axis[0] / mag, axis[1] / mag)

            # Project corners onto axis
            proj1 = [self.points[i][0] * axis[0] + self.points[i][1] * axis[1] for i in range(4)]
            proj2 = [other.points[i][0] * axis[0] + other.points[i][1] * axis[1] for i in range(4)]

        # Check for overlap
            min1, max1 = min(proj1), max(proj1)
            min2, max2 = min(proj2), max(proj2)
            if max1 < min2 or max2 < min1:
                return False  # Separating axis found, no collision

        return True  # No separating axis, collision occurs

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Create player controlled by mouse
player = Hitbox(center=(400, 300), width=50, height=50, angle=45)

# Create obstacles
obstacles = [
    Hitbox(center=(200, 200), width=100, height=50, angle=30),
    Hitbox(center=(600, 400), width=150, height=80, angle=180),
    Hitbox(center=(100, 100), width=150, height=80, angle=45),
]
running = True
while running:
                

    # Update player position based on mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()
    player.center = (mouse_x, mouse_y)
    player.update()

    # Clear the screen
    screen.fill((255, 255, 255))  # White background

    # Draw obstacles

    obstacles[0].center = [obstacles[0].center[0]+1, obstacles[0].center[1]]
    for obstacle in obstacles:
        obstacle.update()
        obstacle.display_hitbox(screen)

    # Draw player
    #player.angle = (player.angle + 2) if player.angle < 360 else 0
    player.display_hitbox(screen)

    # Check for collisions
    for obstacle in obstacles:
        if player.collides_with(obstacle):
            print("Collision Detected!")

    pygame.display.flip()  # Update the display
    dt = clock.tick(60)/1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  # Right mouse button
                player.angle+=15

pygame.quit()