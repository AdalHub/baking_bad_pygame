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

# Scale down the original images to 75% of their size
base_scale = 0.75
front_image_original = pygame.transform.scale(
    front_image_original,
    (int(front_image_original.get_width() * base_scale), int(front_image_original.get_height() * base_scale))
)
side_image_original = pygame.transform.scale(
    side_image_original,
    (int(side_image_original.get_width() * base_scale), int(side_image_original.get_height() * base_scale))
)

# Load baggy goods image
baggy_goods_original = pygame.image.load(os.path.join(SCRIPT_DIR, "assets", "images", "baggy_goods.png"))

# Load the background image (ONCE, outside the loop)
background_path = os.path.join(SCRIPT_DIR, "assets", "images", "background_outside.png")
background_image = pygame.image.load(background_path)
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load lab station image
lab_image = pygame.image.load(os.path.join(SCRIPT_DIR, "assets", "images", "lab.png"))
lab_x = 100  # Position on the left side
lab_y = SCREEN_HEIGHT - lab_image.get_height()  # Bottom of screen

# Define the lab's "depth line" - this is the Y position that determines front/back
lab_depth_y = lab_y + (lab_image.get_height() * 2 // 3)  # Bottom third of the lab

# Define interaction zone around the lab
lab_interaction_rect = pygame.Rect(
    lab_x - 50,  # Extend interaction zone
    lab_y - 50,
    lab_image.get_width() + 100,
    lab_image.get_height() + 100
)

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

# Item holding state
holding_item = False  # Whether player is holding baggy goods

# Font for button
pygame.font.init()
font = pygame.font.Font(None, 36)  # Pixelated-style font

clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)

    # 1. Handle Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Check for E key press to interact with lab
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                # Check if player is near the lab
                player_center_x = player_x + scaled_width // 2 if 'scaled_width' in locals() else player_x
                player_center_y = player_y
                if lab_interaction_rect.collidepoint(player_center_x, player_center_y):
                    holding_item = True  # Pick up the item
    
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
    # At MAX_Y (bottom): scale = 1.0 (100% of base size)
    # At MIN_Y (top): scale = 0.5 (50% of base size - much smaller)
    y_range = MAX_Y - MIN_Y
    y_progress = (player_y - MIN_Y) / y_range  # 0.0 at top, 1.0 at bottom
    scale_factor = 0.5 + (0.5 * y_progress)  # Scale from 0.5 to 1.0

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

    # Check if player is near lab for interaction prompt
    player_center_x = player_x + scaled_width // 2
    player_center_y = player_y
    near_lab = lab_interaction_rect.collidepoint(player_center_x, player_center_y)

    # 3. DRAW EVERYTHING
    screen.blit(background_image, (0, 0))
    
    # Draw lab and player based on Y position (depth sorting)
    # If player's feet are below the lab's depth line, draw player in front
    if player_y > lab_depth_y:
        screen.blit(lab_image, (lab_x, lab_y))
        screen.blit(player_image, (draw_x, draw_y))
        
        # Draw baggy goods if holding (on top of player)
        if holding_item:
            baggy_scaled_width = int(baggy_goods_original.get_width() * scale_factor * 1.2)  # Changed from 0.6 to 1.2
            baggy_scaled_height = int(baggy_goods_original.get_height() * scale_factor * 1.2)  # Changed from 0.6 to 1.2
            baggy_goods_image = pygame.transform.scale(baggy_goods_original, (baggy_scaled_width, baggy_scaled_height))
            
            # Position baggy goods to the side of the player
            if current_direction == "right":
                baggy_x = draw_x + player_rect.width - 10
            else:
                baggy_x = draw_x - baggy_scaled_width + 10
            baggy_y = draw_y + player_rect.height // 3
            
            screen.blit(baggy_goods_image, (baggy_x, baggy_y))
    else:
        # Player is behind the lab
        screen.blit(player_image, (draw_x, draw_y))
        
        # Draw baggy goods if holding (on top of player when behind)
        if holding_item:
            baggy_scaled_width = int(baggy_goods_original.get_width() * scale_factor * 1.2)  # Changed from 0.6 to 1.2
            baggy_scaled_height = int(baggy_goods_original.get_height() * scale_factor * 1.2)  # Changed from 0.6 to 1.2
            baggy_goods_image = pygame.transform.scale(baggy_goods_original, (baggy_scaled_width, baggy_scaled_height))
            
            # Position baggy goods to the side of the player
            if current_direction == "right":
                baggy_x = draw_x + player_rect.width - 10
            else:
                baggy_x = draw_x - baggy_scaled_width + 10
            baggy_y = draw_y + player_rect.height // 3
            
            screen.blit(baggy_goods_image, (baggy_x, baggy_y))
        
        screen.blit(lab_image, (lab_x, lab_y))
    
    # Draw "BAKE" button if near lab and not holding item
    if near_lab and not holding_item:
        button_text = font.render("BAKE [E]", True, WHITE)
        button_rect = button_text.get_rect()
        button_rect.centerx = lab_x + lab_image.get_width() // 2
        button_rect.bottom = lab_y - 10
        
        # Draw button background
        padding = 10
        background_rect = pygame.Rect(
            button_rect.x - padding,
            button_rect.y - padding,
            button_rect.width + padding * 2,
            button_rect.height + padding * 2
        )
        pygame.draw.rect(screen, BLACK, background_rect)
        pygame.draw.rect(screen, WHITE, background_rect, 2)
        
        # Draw text
        screen.blit(button_text, button_rect)
    
    pygame.display.update()

pygame.quit()