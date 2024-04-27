# File: orbit.py
# Programmer: Connor Fricke (cd.fricke23@gmail.com)
# Last Revision:
#   27-MARCH-2024 --> created
#
# Python script for simulation of a Keplerian orbit. Mass units are kilograms, distance units are meters (1 px = 1 m)
# TODO:
#   - add plotting of data
#   - use real values (real gravitational constant, more realistic masses and separations)
#   - create class for writing fonts and putting text to the screen

import pygame as pg

# CLASS FILES
from Utils.trail import *
from Utils.arrow import *
from Utils.text import *
from Utils.satellite import *

# *** INITIALIZE ***
times = []
velocities = []
momentums = []
WIDTH = 1000
HEIGHT = 720
pg.init()
screen = pg.display.set_mode((WIDTH+1, HEIGHT+1))
clock = pg.time.Clock()
running = True
dt = 0
frame = 0
simulationTime = 0
angularMomentum = 0
halfPeriodCounter = 0
period = 0
# ******************

# *** COMMON VECTORS AND LOCATIONS ***
center = pg.Vector2(WIDTH / 2, HEIGHT / 2)
zero = pg.Vector2(0, 0)
origin = zero
xhat = pg.Vector2(1, 0)
yhat = pg.Vector2(0, 1)

# *** CONSTANTS ***
GRAV = 6.674E-11 # N m^2 kg^-2
SUN_MASS = 6.5e15 # kg
INITIAL_POS = center + 250*xhat
RATE = 0.5

# ***** INITIAL CONDITIONS *****  
sun = Satellite(mass=SUN_MASS, radius=20.0)
sun.setPosition(center)
orbitor = Satellite(mass=5.0, radius=10.0)
orbitor.position = INITIAL_POS
orbitor.velocity = 45*yhat

# *** ARROWS + TRAILS ***
orbitorTrail1 = Trail(1575)
orbitorTrail1.addPoint(orbitor.position.copy())
accelArrow = Arrow(orbitor.position, orbitor.position - xhat)

# *** TEXT ***
periodData = Text()
periodData.set_font("consolas", 12, True, False, "white")
sunText = Text()
sunText.set_font("consolas", 12, True, False, "white")
sunText.text("Hello World!")
earthText = Text()
earthText.set_font("consolas", 12, True, False, "red")
earthText.text("Hello Sun!") 
# ******************

# ***** GAME LOOP *****
while running:
    # pg.QUIT means the user closed the window
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    # wipe away anything from the previous frame
    screen.fill("black")

    # add current position of the orbitor to the Trail Satellite array every frame
    currentPosition1 = orbitor.position.copy()
    orbitorTrail1.addPoint(currentPosition1)

    # CALCULATE FORCES
    # force points from circle position to the center
    radius = (orbitor.position - sun.position)
    rhat = radius / radius.magnitude()
    # a = GM/r^2
    orbitor.acceleration = -((GRAV * sun.MASS) / (radius.magnitude() * radius.magnitude())) * rhat

    # L = mvr
    angularMomentum = orbitor.MASS * orbitor.velocity.magnitude() * radius.magnitude()

    # once we have the acceleration, we can decide how to draw the acceleration arrow
    accelArrow.update(orbitor.position, orbitor.position + orbitor.acceleration*5)

    # update acceleration, velocity, and position of each orbitor (NOT the sun... assuming Keplerian Limit M >> m)
    vBefore = orbitor.velocity.copy()
    orbitor.update(RATE*dt)
    vAfter = orbitor.velocity.copy()
    if (vBefore.x*vAfter.x < 0):
        halfPeriodCounter += 1
        period = simulationTime * 2 / halfPeriodCounter

    # ***** RENDER THE GAME HERE *****
    orbitorTrail1.aadraw(screen, "white", 1)
    orbitor.draw(screen, "blue")
    sun.draw(screen, "yellow")
    accelArrow.draw(screen, "white", 3)

    # Render text
    periodData.text(f"Orbital Period: {round(period, 2)} seconds" + (" (Calculating...)" if period == 0 else ""))
    periodData.render(screen, 20*xhat + 20*yhat)
    sunText.render(screen, sun.position + 20*xhat - 20*yhat)
    earthText.render(screen, orbitor.position + 20*xhat - 20*yhat)

    # flip() display to send work to the screen
    pg.display.flip()

    # limit fps
    dt = clock.tick(100) / 1000

    simulationTime += dt * RATE
    frame += 1
    times.append(simulationTime)
    velocities.append(orbitor.velocity.magnitude())
    momentums.append(angularMomentum)

pg.quit()
# ******************

