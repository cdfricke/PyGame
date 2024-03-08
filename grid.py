# File: grid.py
# Programmer: Connor Fricke (cd.fricke23@gmail.com)
# Last Revision:
#   4-MAR-2024 --> Created, v1
#   7-MAR-2024 --> added grid colors
#
# ************************************************

import pygame
import random as r

# *** INITIALIZE ***
WIDTH = 720
HEIGHT = 720
pygame.init()
screen = pygame.display.set_mode((WIDTH+1, HEIGHT+1))
clock = pygame.time.Clock()
running = True
# ******************

# *** COMMON VECTORS AND LOCATIONS ***
center = pygame.Vector2(WIDTH / 2, HEIGHT / 2)
origin = pygame.Vector2(0, 0)
xhat = pygame.Vector2(1, 0)
yhat = pygame.Vector2(0, 1)
# ************************************

def colorFunction(x, xmax):
    r = int(float(x)/float(xmax) * 100)
    g = 0
    b = int(float(x)/float(xmax) * 100)
    return pygame.Color(r, g, b)

# *** CLASS DEFINITIONS ***
# NOTE THAT THESE CLASS DEFINITIONS RELY ON SOME OF THE DEFINED VARIABLES ABOVE

# ARROW : class object for drawing arrows between positions on the screen.
class Arrow:
    def __init__(self, tail, tip):
        self.tip = tip
        self.tail = tail
        self.length = (tip - tail).magnitude()
        self.direction = (tip - tail) / self.length
        self.perpendicular = pygame.Vector2(self.direction.y, -self.direction.x)

    def draw(self, surface, color, thickness):
        # central body
        pygame.draw.line(surface=surface, color=color, start_pos=self.tail, end_pos=self.tip, width=thickness)
        # angled tip
        leftAngled = self.tail + (0.98 * self.length * self.direction) + (0.02 * self.length * self.perpendicular)
        rightAngled = self.tail + (0.98 * self.length * self.direction) - (0.02 * self.length * self.perpendicular)
        points = [leftAngled, self.tip, rightAngled]
        pygame.draw.lines(surface=surface, color=color, closed=False, points=points, width=thickness)

# GRID: class object for drawing a grid with a certain number of rows and columns on the screen.
class Grid:
    def __init__(self, rows, columns):
        self.numRows = rows
        self.numCols = columns
        self.xticks = list(range(0, WIDTH + 1, int(WIDTH / columns)))
        self.yticks = list(range(0, HEIGHT + 1, int(HEIGHT / rows)))
        self.Matrix = [[r.random() for x in range(columns)] for y in range(rows)]
    
    def drawLines(self, surface, color, thickness):
        for tick in self.xticks:
            start = tick*xhat
            end = start + HEIGHT*yhat
            pygame.draw.line(surface=surface, color=color, start_pos=start, end_pos=end, width=thickness)
        for tick in self.yticks:
            start = tick*yhat
            end = start + WIDTH*xhat
            pygame.draw.line(surface=surface, color=color, start_pos=start, end_pos=end, width=thickness)
            
    def drawRectangles(self, surface):
        for x in range(0, self.numCols):
            for y in range(0, self.numRows):
                rect = pygame.Rect(self.xticks[x], self.yticks[y], WIDTH / self.numCols, HEIGHT / self.numRows)
                pygame.draw.rect(surface, colorFunction(self.Matrix[x][y], 1), rect)

# *************************

# rows, cols
gameMap = Grid(20, 20)

# *** GAME LOOP ***
while (running):
    # wipe away anything from the previous frame
    screen.fill("black")

    # *** RENDER THE GAME HERE ***
    gameMap.drawRectangles(screen)
    #gameMap.drawLines(screen, "white", 3)

    # *** END RENDERING ***

    # pygame.QUIT means the user closed the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
# *****************

pygame.quit()