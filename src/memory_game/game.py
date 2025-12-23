import pygame
import os
# initializes all pygame modules
pygame.init()
# Create a window (width, height)
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("You dishonor the family")# Window title

# your family approved colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHT_BLUE= (185, 185, 255)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


# set a music
music_path = os.path.join(SCRIPT_DIR, "assets", "music", "mcmusic1.mp3")
pygame.mixer.music.load(music_path)
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(.5)

# create a player surface
player_model_path = os.path.join(SCRIPT_DIR, "assets", "images", "heisenburg.png")
player_image = pygame.image.load(player_model_path)

#this the background
screen.fill(LIGHT_BLUE)
# this the floor
pygame.draw.rect(screen, GREEN, (0,590, 800, 10))
# place a player on the floor
screen.blit(player_image, (200,500))


clock = pygame.time.Clock()
running = True
while running:

    clock.tick(60)
    


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running= False
        if event.type == pygame.KEYDOWN:
            print("key has been pressed")
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            print(f"mouse has been pressed at {x} {y} ")
        
        if event.type == pygame.K_UP:
            player_image.move_
    

    pygame.display.update()
