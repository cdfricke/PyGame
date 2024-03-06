# File: grid.py
# Programmer: Connor Fricke (cd.fricke23@gmail.com)
# Last Revision:
#   5-MARCH-2024 --> Created, v1
#
# TODO:
#   - add moving object with radial position vector visualized

import pygame

# *** INITIALIZE ***
WIDTH = 720
HEIGHT = 720
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
# ******************

# *** COMMON VECTORS AND LOCATIONS ***

center = pygame.Vector2(WIDTH / 2, HEIGHT / 2)
origin = pygame.Vector2(0, 0)
xhat = pygame.Vector2(1, 0)
yhat = pygame.Vector2(0, 1)

# ************************************

# *** CLASS DEFINITIONS ***
class Grid:
    # Default grid is a 10 by 10
    numRows = 10
    numCols = 10
    xticks = list(range(0, WIDTH, int(WIDTH / numCols)))
    yticks = list(range(0, HEIGHT, int(HEIGHT / numRows)))

    def __init__(self, rows, columns):
        self.numRows = rows
        self.numCols = columns
        self.xticks = list(range(0, WIDTH, int(WIDTH / columns)))
        self.yticks = list(range(0, HEIGHT, int(HEIGHT / rows)))
    
    def draw(self, surface, color, thickness):
        for tick in self.xticks:
            start = tick*xhat
            end = start + HEIGHT*yhat
            pygame.draw.line(surface=surface, color=color, start_pos=start, end_pos=end, width=thickness)
        for tick in self.yticks:
            start = tick*yhat
            end = start + WIDTH*xhat
            pygame.draw.line(surface=surface, color=color, start_pos=start, end_pos=end, width=thickness)
        
# *************************

gameMap = Grid(5, 5)

# *** GAME LOOP ***
while (running):

    # wipe away anything from the previous frame
    screen.fill("black")

    # *** RENDER THE GAME HERE ***
    gameMap.draw(screen, "white", 1)

    # *** END RENDERING ***

    # pygame.QUIT means the user closed the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
# *****************
    
pygame.quit()