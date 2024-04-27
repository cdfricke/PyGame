# File: gradients.py
# Programmer: Connor Fricke (cd.frick23@gmail.com)
# Latest Revision: 26-APR-2024 --> Created

import pygame as pg
from Utils.grid import *
from Utils.colors import *

# *** INITIALIZE ***
WIDTH = 720
HEIGHT = 720
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
running = True
dt = 0
frame = 0
runningTime = 0

COLOR_FUNCTION = 4
GRADIENT_TYPE = "random"

if (GRADIENT_TYPE == "horizontal"):
    myGradient = Grid(columns=WIDTH, rows=1, width=WIDTH, height=HEIGHT)
    myGradient.horizontalGradientMatrix()
elif (GRADIENT_TYPE == "vertical"):
    myGradient = Grid(columns=1, rows=HEIGHT, width=WIDTH, height=HEIGHT)
    myGradient.verticalGradientMatrix()
elif (GRADIENT_TYPE == "random"):
    myGradient = Grid(columns=int(WIDTH/10), rows=int(HEIGHT/10), width=WIDTH, height=HEIGHT)
    myGradient.randomizeMatrix()
else:
    print("Invalid gradient type selected.")
    running = False

while (running):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # wipe away anything from the previous frame
    screen.fill("black")

    if (COLOR_FUNCTION == 1):
        myGradient.drawRectangles(surface=screen, colorFunc=colorFunction1)
    elif (COLOR_FUNCTION == 2):
        myGradient.drawRectangles(surface=screen, colorFunc=colorFunction2)
    elif (COLOR_FUNCTION == 3):
        myGradient.drawRectangles(surface=screen, colorFunc=colorFunction3)
    elif (COLOR_FUNCTION == 4):
        myGradient.drawRectangles(surface=screen, colorFunc=colorFunction4)
    

    # flip() display to send work to the screen
    pg.display.flip()

    dt = clock.tick(100) / 1000

pg.quit()
