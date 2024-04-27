# File: asteroid_belt.py
# Programmer: Connor Fricke (cd.fricke23@gmail.com)
# Last Revision:
#   28-FEB-2024 ---> Created
#   22-APR-2024 ---> Revised to be a many-bodied asteroid belt simulation

# *** INITIALIZE ***
import pygame as pg
from random import uniform, gauss
from math import sin, cos, pi
WIDTH = 900
HEIGHT = 900
pg.init()
screen = pg.display.set_mode((WIDTH+1, HEIGHT+1))
clock = pg.time.Clock()
running = True
dt = 0
frame = 0
simulationTime = 0
# ******************

# CLASS FILES
from Utils.text import *
from Utils.satellite import *

# *** COMMON VECTORS AND LOCATIONS ***
center = pg.Vector2(WIDTH / 2, HEIGHT / 2)
zero = pg.Vector2(0, 0)
xhat = pg.Vector2(1, 0)
yhat = pg.Vector2(0, 1)

# *** CONSTANTS ***
GRAV = 6.674E-11 # N m^2 kg^-2
STELLAR_MASS = 6.5e31 # kg
ASTEROID_MASS = 1000 # kg
SATELLITE_DISTANCE = 300 # px
RATE = 10
NUM_ASTEROIDS = 10000  
SCALE = 1e8 # meters per px
AU = 1.496e11 # meters per AU

# *** HELPER FUNCTIONS ***

def toCartesian(radius: float, angle: float) -> pg.Vector2:
    """
    Converts a radius and angle to polar coordinates relative to a center-screen origin
    """
    return center + radius*cos(angle)*yhat - radius*sin(angle)*xhat

def getForceBetween(satellite1: Satellite, satellite2: Satellite) -> pg.Vector2:
    """
    Given two satellite objects, getForceBetween() returns a vector describing the 
    force vector ON the first parameter FROM the second parameter.
    """
    r = satellite1.position - satellite2.position
    rHat = r / r.magnitude()
    return -((GRAV * satellite1.MASS * satellite2.MASS) / (SCALE*r.magnitude() * SCALE*r.magnitude())) * rHat

def getTangent(loc1: pg.Vector2, loc2: pg.Vector2) -> pg.Vector2:
    """
    returns a normalized vector tangent to the vector described by loc1 - loc2.
    """
    vector = loc1 - loc2
    return pg.Vector2(vector.y, -vector.x) / vector.magnitude()


# ***** INITIAL CONDITIONS *****
star = Satellite(radius=20, mass=STELLAR_MASS)
star.setPosition(pos=center)
satellites = []
for i in range(NUM_ASTEROIDS):
    asteroid = Satellite(radius=1, mass=ASTEROID_MASS)
    # each asteroid gets a randomized position and velocity
    randAngle = uniform(0, 2*pi)
    randRadius = gauss(mu=SATELLITE_DISTANCE, sigma=5)
    asteroid.setPosition(toCartesian(randRadius, randAngle))
    randSpeed = gauss(mu=37, sigma=1)
    tangentVel = randSpeed * getTangent(center, asteroid.position)
    asteroid.setVelocity(vel=tangentVel)
    satellites.append(asteroid)

# TEXT
numBodies = Text()
numBodies.text("Number of Satellites: {}".format(NUM_ASTEROIDS))
solarMasses = STELLAR_MASS / 1.989e30
stellarMass = Text()
stellarMass.text("Stellar Mass: {} kg or {} solar masses.".format(STELLAR_MASS, round(solarMasses,1)))
avgRadii = Text()
avgRadii.text("Average Satellite Distance: {} AU.".format(round(SCALE*SATELLITE_DISTANCE / AU, 4)))

# ***** GAME LOOP *****
while running:
    # pg.QUIT means the user closed the window
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    # wipe away anything from the previous frame
    screen.fill("black")

    # ***** RENDER THE GAME HERE *****
    star.draw(surface=screen, color="yellow")

    numBodies.render(surface=screen, location=(5*xhat + 5*yhat))
    stellarMass.render(surface=screen, location=(5*xhat + 20*yhat))
    avgRadii.render(surface=screen, location=(5*xhat + 35*yhat))

    for asteroid in satellites:
        asteroid.draw(surface=screen, color="white")

    # calculate force on each satellite, then update
    for asteroid in satellites:
        asteroid.acceleration = getForceBetween(asteroid, star) / ASTEROID_MASS
        asteroid.update(dt * RATE)

    # flip() display to send work to the screen
    pg.display.flip()

    # limit to 100 fps (dt ~ 0.01)
    dt = clock.tick(100) / 1000
    simulationTime += dt
    if (simulationTime > 30):
        RATE = 1
    frame += 1

pg.quit()