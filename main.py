# Simple pygame program

# Import and initialize the pygame library
import pygame

pygame.font.init()

from Player import Player
from Enemy import Enemy

# Import pygame.locals for easier access to key coordinates
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Initialize pygame
pygame.init()

# Define constants for the screen width and height
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

LEVEL = 1
LIVES = 5
MAIN_FONT = pygame.font.SysFont("comicsans", 30)

# Set up the drawing window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
BACKGROUND = pygame.image.load("./images/background.jpg")

# Create a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

# Instantiate player. Right now, this is just a rectangle.
player = Player(SCREEN_HEIGHT, SCREEN_WIDTH, LIVES)

# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Run until the user asks to quit
running = True


def draw_screen(screen):
    screen.blit(BACKGROUND, (0, 0))
    live_label = MAIN_FONT.render(f"Live: {LIVES}", True, (255, 255, 255))
    level_label = MAIN_FONT.render(f"Live: {LEVEL}", True, (255, 255, 255))

    screen.blit(live_label, (10, 10))
    screen.blit(level_label, (SCREEN_WIDTH - level_label.get_width() - 10, 10))
    pygame.display.update()


while running:

    # Setup the clock for a decent framerate
    clock = pygame.time.Clock()

    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key?
            if event.key == K_ESCAPE:
                running = False
        # Did the user click the window close button?
        elif event.type == QUIT:
            running = False

        # Add a new enemy?
        elif event.type == ADDENEMY:
            # Create the new enemy and add it to sprite groups
            new_enemy = Enemy(SCREEN_HEIGHT, SCREEN_WIDTH)
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    # Update the player sprite based on user keypresses
    player.update(pressed_keys)

    # Update enemy position
    enemies.update()

    # Fill the background with white
    screen.fill((0, 0, 0))
    draw_screen(screen)
    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)  # NOTE: blit() puts the
        # top-left corner of surf at the location given

    # TODO: fix lose lives
    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        player.lose_life()
        print(player.get_lives())
        if player.is_dead():
            player.kill()
            running = False

    # Draw a solid blue circle in the center
    # pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

    # Flip the display
    pygame.display.flip()

    # Ensure program maintains a rate of 30 frames per second
    clock.tick(60)

# Done! Time to quit.
pygame.quit()
