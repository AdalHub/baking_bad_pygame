import pygame
import os
import math

# initializes all pygame modules
pygame.init()

# your family approved colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (185, 185, 255)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("You dishonor the family")

# set a music
music_path = os.path.join(SCRIPT_DIR, "assets", "music", "mcmusic1.mp3")
pygame.mixer.music.load(music_path)
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(.5)

# Load all player images (ONCE) - keep originals for scaling
front_image_original = pygame.image.load(os.path.join(SCRIPT_DIR, "assets", "images", "front_heisenburg.png"))
side_image_original = pygame.image.load(os.path.join(SCRIPT_DIR, "assets", "images", "side_heisenburg.png"))

# Load the background image (ONCE, outside the loop)
background_path = os.path.join(SCRIPT_DIR, "assets", "images", "background_outside.png")
background_image = pygame.image.load(background_path)
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Player starting position
player_x = 200
player_y = 500
player_speed = 5

# Set boundaries
MIN_Y = (SCREEN_HEIGHT // 2) + 100  # Top boundary at halfway (300px)
MAX_Y = SCREEN_HEIGHT  # Bottom boundary

# Current image selection
current_direction = "front"  # Track current direction

# Walking animation variables
walk_cycle = 0  # Counter for walking animation
walk_speed = 10  # How fast the rotation cycles (higher = faster)
rotation_angle = 5  # Maximum rotation angle in degrees
is_moving = False  # Track if player is currently moving

clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)

    # 1. Handle Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # 2. Update Game State
    keys = pygame.key.get_pressed()
    
    # Check which key is pressed and update direction
    is_moving = False
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
        current_direction = "left"
        is_moving = True
    elif keys[pygame.K_RIGHT]:
        player_x += player_speed
        current_direction = "right"
        is_moving = True
    elif keys[pygame.K_UP]:
        player_y -= player_speed
        current_direction = "front"
        is_moving = True
    elif keys[pygame.K_DOWN]:
        player_y += player_speed
        current_direction = "front"
        is_moving = True

    # Update walk cycle if moving
    if is_moving:
        walk_cycle += walk_speed
    else:
        walk_cycle = 0  # Reset when not moving

    # Calculate rotation angle using sine wave for smooth back-and-forth
    current_rotation = math.sin(math.radians(walk_cycle)) * rotation_angle

    # Keep player within Y boundaries FIRST (before scaling calculations)
    player_y = max(MIN_Y, min(player_y, MAX_Y))

    # Calculate scale based on Y position (perspective effect)
    # At MAX_Y (bottom): scale = 1.0 (100%)
    # At MIN_Y (top/halfway): scale = 0.25 (25%, which is 75% smaller)
    y_range = MAX_Y - MIN_Y
    y_progress = (player_y - MIN_Y) / y_range  # 0.0 at top, 1.0 at bottom
    scale_factor = 0.25 + (0.75 * y_progress)  # Scale from 0.25 to 1.0

    # Select the appropriate original image based on direction
    if current_direction == "left":
        current_image = pygame.transform.flip(side_image_original, True, False)
    elif current_direction == "right":
        current_image = side_image_original
    else:  # front
        current_image = front_image_original

    # Scale the image based on Y position
    scaled_width = int(current_image.get_width() * scale_factor)
    scaled_height = int(current_image.get_height() * scale_factor)
    scaled_image = pygame.transform.scale(current_image, (scaled_width, scaled_height))

    # Apply rotation for walking animation
    player_image = pygame.transform.rotate(scaled_image, current_rotation)

    # Get the rect of the rotated image to handle position correctly
    player_rect = player_image.get_rect()

    # Adjust Y position so bottom of image touches the boundary
    # player_y represents the bottom of the image, not the top
    draw_y = player_y - player_rect.height

    # Center the rotated image on the player's x position
    draw_x = player_x - (player_rect.width - scaled_width) // 2

    # Keep player within X boundaries (using original scaled width for movement)
    player_x = max(0, min(player_x, SCREEN_WIDTH - scaled_width))

    # 3. DRAW EVERYTHING
    screen.blit(background_image, (0, 0))
    screen.blit(player_image, (draw_x, draw_y))
    
    pygame.display.update()

pygame.quit()