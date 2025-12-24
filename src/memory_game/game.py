import pygame
import os
import math
import random

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
DARK_RED = (139, 0, 0)

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

# Load sound effects
jesse_yea_sound = pygame.mixer.Sound(os.path.join(SCRIPT_DIR, "assets", "music", "jesse_yea.mp3"))

# Load all player images (ONCE) - keep originals for scaling
front_image_original = pygame.image.load(os.path.join(SCRIPT_DIR, "assets", "images", "front_heisenburg.png"))
side_image_original = pygame.image.load(os.path.join(SCRIPT_DIR, "assets", "images", "side_heisenburg.png"))

# Load enemy images
enemy_front_original = pygame.image.load(os.path.join(SCRIPT_DIR, "assets", "images", "front_fring.png"))
enemy_side_original = pygame.image.load(os.path.join(SCRIPT_DIR, "assets", "images", "side_fring.png"))

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

# Scale enemy images
enemy_front_original = pygame.transform.scale(
    enemy_front_original,
    (int(enemy_front_original.get_width() * base_scale), int(enemy_front_original.get_height() * base_scale))
)
enemy_side_original = pygame.transform.scale(
    enemy_side_original,
    (int(enemy_side_original.get_width() * base_scale), int(enemy_side_original.get_height() * base_scale))
)

# Load baggy goods image
baggy_goods_original = pygame.image.load(os.path.join(SCRIPT_DIR, "assets", "images", "baggy_goods.png"))

# Load gun image
gun_original = pygame.image.load(os.path.join(SCRIPT_DIR, "assets", "images", "gun.png"))

# Load Jesse image and scale to match player size
jesse_image_original = pygame.image.load(os.path.join(SCRIPT_DIR, "assets", "images", "jesse.png"))
# Scale Jesse to same base size as player (75% of original)
jesse_image_original = pygame.transform.scale(
    jesse_image_original,
    (int(jesse_image_original.get_width() * base_scale), int(jesse_image_original.get_height() * base_scale))
)
jesse_image = pygame.transform.flip(jesse_image_original, True, False)  # Flip horizontally

# Position Jesse at bottom right corner
jesse_x = SCREEN_WIDTH - jesse_image.get_width()  # Far right
jesse_y = SCREEN_HEIGHT  # Bottom of screen (jesse_y represents bottom of Jesse's feet)

# Define Jesse interaction zone
jesse_interaction_rect = pygame.Rect(
    jesse_x - 50,
    jesse_y - jesse_image.get_height() - 50,
    jesse_image.get_width() + 100,
    jesse_image.get_height() + 100
)

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

# Set boundaries
MIN_Y = (SCREEN_HEIGHT // 2) + 100  # Top boundary at halfway (300px)
MAX_Y = SCREEN_HEIGHT  # Bottom boundary

# Enemy class
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 2
        self.direction = "right"
        self.walk_cycle = 0
        self.walk_speed = 10
        self.rotation_angle = 5
        self.alive = True
    
    def update(self, player_x, player_y):
        if not self.alive:
            return
        
        # Calculate direction to player
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            # Normalize and move towards player
            dx = dx / distance
            dy = dy / distance
            
            self.x += dx * self.speed
            self.y += dy * self.speed
            
            # Update direction based on movement
            if abs(dx) > abs(dy):
                if dx > 0:
                    self.direction = "right"
                else:
                    self.direction = "left"
            else:
                self.direction = "front"
            
            # Update walk cycle
            self.walk_cycle += self.walk_speed
        
        # Keep enemy within boundaries
        self.y = max(MIN_Y, min(self.y, MAX_Y))
        
        # Calculate scale based on Y position
        y_range = MAX_Y - MIN_Y
        y_progress = (self.y - MIN_Y) / y_range
        self.scale_factor = 0.5 + (0.5 * y_progress)
    
    def get_image(self):
        # Select image based on direction
        if self.direction == "left":
            current_image = pygame.transform.flip(enemy_side_original, True, False)
        elif self.direction == "right":
            current_image = enemy_side_original
        else:  # front
            current_image = enemy_front_original
        
        # Scale based on Y position
        scaled_width = int(current_image.get_width() * self.scale_factor)
        scaled_height = int(current_image.get_height() * self.scale_factor)
        scaled_image = pygame.transform.scale(current_image, (scaled_width, scaled_height))
        
        # Apply rotation for walking animation
        current_rotation = math.sin(math.radians(self.walk_cycle)) * self.rotation_angle
        rotated_image = pygame.transform.rotate(scaled_image, current_rotation)
        
        return rotated_image, scaled_width, scaled_height
    
    def get_rect(self):
        # Get collision rect for enemy
        _, scaled_width, scaled_height = self.get_image()
        return pygame.Rect(self.x - scaled_width // 2, self.y - scaled_height, scaled_width, scaled_height)
    
    def check_bullet_collision(self, bullets):
        if not self.alive:
            return
        
        enemy_rect = self.get_rect()
        for bullet in bullets:
            if bullet.active:
                bullet_rect = pygame.Rect(bullet.x - bullet.size, bullet.y - bullet.size, bullet.size * 2, bullet.size * 2)
                if enemy_rect.colliderect(bullet_rect):
                    self.alive = False
                    bullet.active = False
                    return True
        return False

# Bullet class to manage bullet properties
class Bullet:
    def __init__(self, x, y, direction, scale):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 10
        self.size = int(8 * scale)  # Scale bullet with player
        self.active = True
    
    def update(self):
        # Move bullet based on direction
        if self.direction == "left":
            self.x -= self.speed
        elif self.direction == "right":
            self.x += self.speed
        elif self.direction == "front":
            self.y += self.speed  # Down
        elif self.direction == "back":
            self.y -= self.speed  # Up (if you add up movement)
        
        # Deactivate if off screen
        if self.x < 0 or self.x > SCREEN_WIDTH or self.y < 0 or self.y > SCREEN_HEIGHT:
            self.active = False
    
    def draw(self, screen):
        if self.active:
            pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.size)

# Game state
game_state = "playing"  # "playing" or "dead"

# Player starting position
player_x = 200
player_y = 500
player_speed = 5

# Current image selection
current_direction = "front"  # Track current direction

# Walking animation variables
walk_cycle = 0  # Counter for walking animation
walk_speed = 10  # How fast the rotation cycles (higher = faster)
rotation_angle = 5  # Maximum rotation angle in degrees
is_moving = False  # Track if player is currently moving

# Item holding state
holding_item = False  # Whether player is holding baggy goods

# Gun state
holding_gun = False  # Whether player is holding gun
bullets = []  # List to store active bullets

# Enemy list
enemies = []
# Spawn initial enemies
for _ in range(3):
    enemy_x = random.randint(50, SCREEN_WIDTH - 50)
    enemy_y = random.randint(MIN_Y, MAX_Y)
    enemies.append(Enemy(enemy_x, enemy_y))

# Money system
money = 0
show_money_popup = False
money_popup_timer = 0
money_popup_duration = 60  # Show for 60 frames (1 second at 60 FPS)

# Font for button and money
pygame.font.init()
font = pygame.font.Font(None, 36)  # Pixelated-style font
money_font = pygame.font.Font(None, 48)  # Larger font for money display
death_font = pygame.font.Font(None, 72)  # Large font for death screen

def reset_game():
    global player_x, player_y, game_state, enemies, bullets, money, holding_item, holding_gun
    player_x = 200
    player_y = 500
    game_state = "playing"
    bullets = []
    holding_item = False
    holding_gun = False
    money = 0
    
    # Respawn enemies
    enemies = []
    for _ in range(3):
        enemy_x = random.randint(50, SCREEN_WIDTH - 50)
        enemy_y = random.randint(MIN_Y, MAX_Y)
        enemies.append(Enemy(enemy_x, enemy_y))

clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)

    # 1. Handle Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Check for key presses
        if event.type == pygame.KEYDOWN:
            if game_state == "playing":
                # E key for interactions
                if event.key == pygame.K_e:
                    player_center_x = player_x + scaled_width // 2 if 'scaled_width' in locals() else player_x
                    player_center_y = player_y
                    
                    # Check if player is near the lab
                    if lab_interaction_rect.collidepoint(player_center_x, player_center_y) and not holding_item:
                        holding_item = True  # Pick up the item
                    
                    # Check if player is near Jesse and holding item
                    elif jesse_interaction_rect.collidepoint(player_center_x, player_center_y) and holding_item:
                        holding_item = False  # Sell the item
                        money += 100  # Add $100
                        show_money_popup = True  # Show the popup
                        money_popup_timer = money_popup_duration  # Reset timer
                        jesse_yea_sound.play()  # Play Jesse sound effect
                
                # F key to toggle gun
                if event.key == pygame.K_f:
                    holding_gun = not holding_gun
                
                # SPACE key to shoot
                if event.key == pygame.K_SPACE and holding_gun:
                    # Create bullet at player position
                    bullet_x = player_x + scaled_width // 2 if 'scaled_width' in locals() else player_x
                    bullet_y = player_y - (scaled_height // 2) if 'scaled_height' in locals() else player_y
                    bullet = Bullet(bullet_x, bullet_y, current_direction, scale_factor if 'scale_factor' in locals() else 1.0)
                    bullets.append(bullet)
            
            # Retry button on death screen
            elif game_state == "dead":
                if event.key == pygame.K_r:
                    reset_game()
        
        # Mouse click for retry button
        if event.type == pygame.MOUSEBUTTONDOWN and game_state == "dead":
            mouse_x, mouse_y = event.pos
            # Check if clicked on retry button
            button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 60)
            if button_rect.collidepoint(mouse_x, mouse_y):
                reset_game()
    
    # 2. Update Game State
    if game_state == "playing":
        keys = pygame.key.get_pressed()
        
        # Update money popup timer
        if show_money_popup:
            money_popup_timer -= 1
            if money_popup_timer <= 0:
                show_money_popup = False
        
        # Update bullets
        for bullet in bullets[:]:  # Use slice to avoid modifying list while iterating
            bullet.update()
            if not bullet.active:
                bullets.remove(bullet)
        
        # Update enemies
        for enemy in enemies[:]:
            enemy.update(player_x, player_y)
            enemy.check_bullet_collision(bullets)
            if not enemy.alive:
                enemies.remove(enemy)
        
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
        y_range = MAX_Y - MIN_Y
        y_progress = (player_y - MIN_Y) / y_range
        scale_factor = 0.5 + (0.5 * y_progress)

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
        draw_y = player_y - player_rect.height
        draw_x = player_x - (player_rect.width - scaled_width) // 2

        # Keep player within X boundaries
        player_x = max(0, min(player_x, SCREEN_WIDTH - scaled_width))

        # Check collision with enemies
        player_collision_rect = pygame.Rect(player_x - scaled_width // 2, player_y - scaled_height, scaled_width, scaled_height)
        for enemy in enemies:
            if enemy.alive and player_collision_rect.colliderect(enemy.get_rect()):
                game_state = "dead"
                break

        # Check if player is near lab or Jesse for interaction prompt
        player_center_x = player_x + scaled_width // 2
        player_center_y = player_y
        near_lab = lab_interaction_rect.collidepoint(player_center_x, player_center_y)
        near_jesse = jesse_interaction_rect.collidepoint(player_center_x, player_center_y)

    # 3. DRAW EVERYTHING
    screen.blit(background_image, (0, 0))
    
    if game_state == "playing":
        # Draw Jesse at bottom right
        jesse_draw_y = jesse_y - jesse_image.get_height()
        screen.blit(jesse_image, (jesse_x, jesse_draw_y))
        
        # Collect all entities for depth sorting
        entities = []
        
        # Add player
        entities.append(("player", player_y, draw_x, draw_y, player_image))
        
        # Add enemies
        for enemy in enemies:
            if enemy.alive:
                enemy_image, enemy_width, enemy_height = enemy.get_image()
                enemy_rect = enemy_image.get_rect()
                enemy_draw_y = enemy.y - enemy_rect.height
                enemy_draw_x = enemy.x - (enemy_rect.width - enemy_width) // 2
                entities.append(("enemy", enemy.y, enemy_draw_x, enemy_draw_y, enemy_image))
        
        # Add lab
        entities.append(("lab", lab_depth_y, lab_x, lab_y, lab_image))
        
        # Sort by Y position (depth)
        entities.sort(key=lambda e: e[1])
        
        # Draw all entities in order
        for entity in entities:
            entity_type, _, x, y, image = entity
            screen.blit(image, (x, y))
            
            # Draw extras on player
            if entity_type == "player":
                # Draw baggy goods if holding
                if holding_item:
                    baggy_scaled_width = int(baggy_goods_original.get_width() * scale_factor * 1.2)
                    baggy_scaled_height = int(baggy_goods_original.get_height() * scale_factor * 1.2)
                    baggy_goods_image = pygame.transform.scale(baggy_goods_original, (baggy_scaled_width, baggy_scaled_height))
                    
                    if current_direction == "right":
                        baggy_x = x + player_rect.width - 10
                    else:
                        baggy_x = x - baggy_scaled_width + 10
                    baggy_y = y + player_rect.height // 3
                    
                    screen.blit(baggy_goods_image, (baggy_x, baggy_y))
                
                # Draw gun if holding
                if holding_gun:
                    gun_scaled_width = int(gun_original.get_width() * scale_factor)
                    gun_scaled_height = int(gun_original.get_height() * scale_factor)
                    gun_image = pygame.transform.scale(gun_original, (gun_scaled_width, gun_scaled_height))
                    
                    if current_direction == "left":
                        gun_image = pygame.transform.flip(gun_image, True, False)
                        gun_x = x - gun_scaled_width + 20
                    else:
                        gun_x = x + player_rect.width - 20
                    
                    gun_y = y + player_rect.height // 2 - gun_scaled_height // 2
                    screen.blit(gun_image, (gun_x, gun_y))
        
        # Draw all bullets on top
        for bullet in bullets:
            bullet.draw(screen)
        
        # Draw interaction buttons
        if near_lab and not holding_item:
            button_text = font.render("BAKE [E]", True, WHITE)
            button_rect = button_text.get_rect()
            button_rect.centerx = lab_x + lab_image.get_width() // 2
            button_rect.bottom = lab_y - 10
            
            padding = 10
            background_rect = pygame.Rect(
                button_rect.x - padding,
                button_rect.y - padding,
                button_rect.width + padding * 2,
                button_rect.height + padding * 2
            )
            pygame.draw.rect(screen, BLACK, background_rect)
            pygame.draw.rect(screen, WHITE, background_rect, 2)
            screen.blit(button_text, button_rect)
        
        if near_jesse and holding_item:
            button_text = font.render("SELL [E]", True, WHITE)
            button_rect = button_text.get_rect()
            button_rect.centerx = jesse_x + jesse_image.get_width() // 2
            button_rect.bottom = jesse_draw_y - 10
            
            padding = 10
            background_rect = pygame.Rect(
                button_rect.x - padding,
                button_rect.y - padding,
                button_rect.width + padding * 2,
                button_rect.height + padding * 2
            )
            pygame.draw.rect(screen, BLACK, background_rect)
            pygame.draw.rect(screen, WHITE, background_rect, 2)
            screen.blit(button_text, button_rect)
        
        # Draw money counter
        money_text = money_font.render(f"${money}", True, GREEN)
        screen.blit(money_text, (20, 20))
        
        # Draw money popup
        if show_money_popup:
            popup_text = money_font.render("+$100", True, GREEN)
            popup_rect = popup_text.get_rect()
            popup_rect.centerx = draw_x + player_rect.width // 2
            popup_rect.bottom = draw_y - 20
            screen.blit(popup_text, popup_rect)
    
    elif game_state == "dead":
        # Draw death screen overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(DARK_RED)
        screen.blit(overlay, (0, 0))
        
        # Draw "YOU DIED" text
        death_text = death_font.render("YOU DIED", True, WHITE)
        death_rect = death_text.get_rect()
        death_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
        screen.blit(death_text, death_rect)
        
        # Draw retry button
        button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 60)
        pygame.draw.rect(screen, BLACK, button_rect)
        pygame.draw.rect(screen, WHITE, button_rect, 3)
        
        button_text = font.render("RETRY [R]", True, WHITE)
        text_rect = button_text.get_rect()
        text_rect.center = button_rect.center
        screen.blit(button_text, text_rect)
    
    pygame.display.update()

pygame.quit()