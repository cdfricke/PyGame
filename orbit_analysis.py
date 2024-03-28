# File: orbit_analysis.py
# Programmer: Connor Fricke (cd.fricke23@gmail.com)
# Last Revision:
#   27-MARCH-2024 --> created
#
# Python script for simulation of a Keplerian orbit.
# TODO:
#   - add GUI stuff to show some real-time data
#   - add plotting of data
#   - use real values (real gravitational constant, more realistic masses and separations)

# *** INITIALIZE ***
import pygame
# my classes
from trail import *
from arrow import *

# libraries for analysis
import matplotlib.pyplot as plt
import numpy as np

times = []
velocities = []

WIDTH = 720
HEIGHT = 720
pygame.init()
screen = pygame.display.set_mode((WIDTH+1, HEIGHT+1))
clock = pygame.time.Clock()
running = True
dt = 0
frame = 0
simulationTime = 0
# ******************

# *** CONSTANTS ***
GRAV = 6.674E-11 # N m^2 kg^-2
SUN_MASS = 6.5e15 # kg
RATE = 3

# *** COMMON VECTORS AND LOCATIONS ***

center = pygame.Vector2(WIDTH / 2, HEIGHT / 2)
zero = pygame.Vector2(0, 0)
origin = zero
xhat = pygame.Vector2(1, 0)
yhat = pygame.Vector2(0, 1)

# ************************************

# *** CLASS DEFINITIONS ***
# NOTE THAT THESE CLASS DEFINITIONS RELY ON SOME OF THE DEFINED VARIABLES ABOVE

class Object:
    """This is the base object of the simulation. It is drawn in the window as a circle"""
    def __init__(self, radius, mass):
        # constants
        self.RADIUS = radius
        self.MASS = mass
        # variables
        self.position = center          # set position at middle of screen
        self.velocity = origin            # set velocity to zero
        self.acceleration = zero        # set acceleration to zero

    # call draw() to automatically draw the circle with it's current attributes
    def draw(self, surface, color):
        pygame.draw.circle(surface=surface, color=color, center=self.position, radius=self.RADIUS)

    def update(self, deltaTime):
        # update acceleration, velocity, and position
        # v_f = v_0 + at
        self.velocity += self.acceleration * deltaTime
        # x_f = x_0 + vt
        self.position += self.velocity * deltaTime
        
# *************************

# ***** INITIAL CONDITIONS *****
        
# sun object, default position and velocity
sun = Object(mass=SUN_MASS, radius=20.0)
# orbitor1 object, non-default position and velocity
orbitor1 = Object(mass=5.0, radius=10.0)
orbitor1.position = center + 250*xhat
orbitor1.velocity = 31*yhat

# *** ARROWS, GRIDS, AND TRAILS ***
orbitorTrail1 = Trail(1200)
orbitorTrail1.addPoint(orbitor1.position.copy())

accelArrow = Arrow(orbitor1.position, orbitor1.position - xhat)

# ***** GAME LOOP *****
while running:
    # pygame.QUIT means the user closed the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # wipe away anything from the previous frame
    screen.fill("black")

    # add current position of the orbitor1 to the Trail object array every frame
    currentPosition1 = orbitor1.position.copy()
    orbitorTrail1.addPoint(currentPosition1)

    # CALCULATE FORCES
    # force points from circle position to the center
    radius = (orbitor1.position - sun.position)
    rhat = radius / radius.magnitude()
    # a = GM/r^2 (in the negative radial direction)
    orbitor1.acceleration = -((GRAV * sun.MASS) / (radius.magnitude() * radius.magnitude())) * rhat

    # once we have the acceleration, we can decide how to draw the acceleration arrow
    accelArrow.update(orbitor1.position, orbitor1.position + orbitor1.acceleration*1.5)

    # update acceleration, velocity, and position of each orbitor (NOT the sun... assuming Keplerian Limit M >> m)
    orbitor1.update(RATE*dt)

    # ***** RENDER THE GAME HERE *****
    # TRAIL
    orbitorTrail1.aadraw(screen, "white", 1)
    # ORBITOR / SUN
    orbitor1.draw(screen, "blue")
    sun.draw(screen, "yellow")
    # ARROW
    accelArrow.draw(screen, "white", 3)

    # flip() display to send work to the screen
    pygame.display.flip()

    # limit to 50 fps (dt ~ 0.02)
    dt = clock.tick(100) / 1000
    # track a couple things for use
    simulationTime += dt
    frame += 1
    print(simulationTime)
    # add data to our times and velocities arrays to plot after the sim runs
    times.append(simulationTime)
    velocities.append(-orbitor1.velocity.y)

pygame.quit()

fig, ax = plt.subplots()
ax.set_ylabel("$V_y$ (px $\\rm s^{-1}$)")
ax.set_xlabel("Time (s)")
ax.set_title("$V_y$ vs. time")

ax.plot(times, velocities)

plt.show()