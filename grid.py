# File: grid.py
# Programmer: Connor Fricke (cd.fricke23@gmail.com)
# Last Revision:
#   5-MARCH-2024 --> Created, v1
#
# TODO:
#   - add gridlines to window
#   - add moving object with radial position vector visualized

import pygame

# *** INITIALIZE ***
WIDTH = 720
HEIGHT = 720
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

# *** COMMON VECTORS AND LOCATIONS ***
center = pygame.Vector2(WIDTH / 2, HEIGHT / 2)
origin = pygame.Vector2(0, 0)

while (running):

    # wipe away anything from the previous frame
    screen.fill("black")

    # *** RENDER THE GAME HERE ***
    pygame.draw.line(surface=screen, color="white", start_pos=origin, end_pos=center, width=1)

    # *** END RENDERING ***

    # pygame.QUIT means the user closed the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()