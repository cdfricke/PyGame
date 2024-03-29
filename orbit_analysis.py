# File: orbit_analysis.py
# Programmer: Connor Fricke (cd.fricke23@gmail.com)
# Last Revision:
#   27-MARCH-2024 --> created
#
# Python script for simulation of a Keplerian orbit. Mass units are kilograms, distance units are meters (1 px = 1 m)
# TODO:
#   - add plotting of data
#   - use real values (real gravitational constant, more realistic masses and separations)
#   - create class for writing fonts and putting text to the screen

# libraries for analysis
import matplotlib.pyplot as plt
import pygame
# my classes
from trail import *
from arrow import *



# *** INITIALIZE ***
times = []
velocities = []
momentums = []
WIDTH = 1000
HEIGHT = 720
pygame.init()
screen = pygame.display.set_mode((WIDTH+1, HEIGHT+1))
clock = pygame.time.Clock()
consolas = pygame.font.SysFont(name="consolas", size=12, bold=True, italic=False)
running = True
dt = 0
frame = 0
simulationTime = 0
angularMomentum = 0
halfPeriodCounter = 0
period = 0
# ******************

# *** COMMON VECTORS AND LOCATIONS ***
center = pygame.Vector2(WIDTH / 2, HEIGHT / 2)
zero = pygame.Vector2(0, 0)
origin = zero
xhat = pygame.Vector2(1, 0)
yhat = pygame.Vector2(0, 1)
# ******************

# *** CONSTANTS ***
GRAV = 6.674E-11 # N m^2 kg^-2
SUN_MASS = 6.5e15 # kg
INITIAL_POS = center + 250*xhat
RATE = 5
# ******************

# *** OBJECT CLASS ***
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
orbitor1.position = INITIAL_POS
orbitor1.velocity = 45*yhat
# ******************

# *** ARROWS, GRIDS, AND TRAILS ***
orbitorTrail1 = Trail(1575)
orbitorTrail1.addPoint(orbitor1.position.copy())
accelArrow = Arrow(orbitor1.position, orbitor1.position - xhat)
# ******************

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

    # L = mvr
    angularMomentum = orbitor1.MASS * orbitor1.velocity.magnitude() * radius.magnitude()

    # once we have the acceleration, we can decide how to draw the acceleration arrow
    accelArrow.update(orbitor1.position, orbitor1.position + orbitor1.acceleration*5)

    # update acceleration, velocity, and position of each orbitor (NOT the sun... assuming Keplerian Limit M >> m)
    vBefore = orbitor1.velocity.copy()
    orbitor1.update(RATE*dt)
    vAfter = orbitor1.velocity.copy()
    if (vBefore.x*vAfter.x < 0):
        halfPeriodCounter += 1
        period = simulationTime * 2 / halfPeriodCounter
        print("Orbital Period:", round(period, 2), "seconds.")

    # ***** RENDER THE GAME HERE *****
    # TRAIL
    orbitorTrail1.aadraw(screen, "white", 1)
    # ORBITOR / SUN
    orbitor1.draw(screen, "blue")
    sun.draw(screen, "yellow")
    # ARROW
    accelArrow.draw(screen, "white", 1)

    # Render and display text
    sunText = consolas.render("Hello World!", True, "white") # returns a surface object
    earthText = consolas.render("Hello Sun!", True, "red")
    orbitalPeriodText = consolas.render(f"Orbital Period: {round(period, 2)} seconds", True, "white")
    # once we have our text surfaces, we must blit them to the screen
    screen.blit(sunText, sun.position + 20*xhat - 20*yhat)
    screen.blit(earthText, orbitor1.position + 20*xhat - 20*yhat)
    screen.blit(orbitalPeriodText, 20*xhat + 20*yhat)

    # flip() display to send work to the screen
    pygame.display.flip()

    # limit to 50 fps (dt ~ 0.02)
    dt = clock.tick(100) / 1000
    # track a couple things for use
    simulationTime += dt * RATE
    frame += 1
    # add data to our times and velocities arrays to plot after the sim runs
    times.append(simulationTime)
    velocities.append(orbitor1.velocity.magnitude())
    momentums.append(angularMomentum)

pygame.quit()

# *** DATA ANALYSIS ***
fig, ax = plt.subplots()
ax.set_ylabel("$v$ (px $\\rm s^{-1}$)")
ax.set_xlabel("Time (s)")
ax.set_title("Velocity vs. time")
ax.plot(times, velocities)
plt.show()
# ******************

