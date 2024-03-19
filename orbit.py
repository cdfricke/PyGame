# File: orbit.py
# Programmer: Connor Fricke (cd.fricke23@gmail.com)
# Last Revision:
#   28-FEB-2024 ---> defined commonly used vectors, object class, initialized project
#   29-FEB-2024 ---> defined gravity as inverse square law, assessed TODO list
# TODO:
#   - add some GUI stuff

# *** INITIALIZE ***
import pygame
from grid import *
from colors import *
from arrow import Arrow

WIDTH = 720
HEIGHT = 720
pygame.init()
screen = pygame.display.set_mode((WIDTH+1, HEIGHT+1))
clock = pygame.time.Clock()
running = True
inFront = True
dt = 0
frame = 0
GRAV = 40.0
# ******************

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
    """This is the base object of my game. It is drawn in game as a circle"""
    def __init__(self, radius, mass):
        # constants
        self.RADIUS = radius
        self.MASS = mass
        # variables
        self.position = center          # set position at middle of screen
        self.velocity = origin            # set velocity to zero
        self.acceleration = zero        # set acceleration to zero
        self.force = zero               # this is the force that the current object "feels"

    # call draw() to automatically draw the circle with it's current attributes
    def draw(self, surface, color):
        pygame.draw.circle(surface=surface, color=color, center=self.position, radius=self.RADIUS)

    def update(self, deltaTime):
        # update acceleration, velocity, and position
        self.acceleration = self.force / self.MASS
        self.velocity += self.acceleration
        self.position += self.velocity * deltaTime

class Trail:
    def __init__(self, maxlength):
        self.pointArray = []
        self.maxlength = maxlength
        
    def draw(self, surface, color, width):
        pygame.draw.aalines(surface=surface, color=color, closed=False, points=self.pointArray, blend=1)

    def addPoint(self, point):
        self.pointArray.append(point)
        # limit trail length to N points (N should be determined based on the orbit length)
        if (len(self.pointArray) > self.maxlength):
            self.pointArray.pop(0)
        
# *************************

# ***** INITIAL CONDITIONS *****
# sun object, default position and velocity
sun = Object(mass=100.0, radius=20.0)
# orbitor1 object, non-default position and velocity
orbitor1 = Object(mass=5.0, radius=10.0)
orbitor1.position = center + 250*xhat
orbitor1.velocity = 31*yhat
# orbitor2 object, non-default position and velocity
orbitor2 = Object(mass=5.0, radius=10.0)
orbitor2.position = center + 100*xhat
orbitor2.velocity = 50*yhat
# orbitor2 object, non-default position and velocity
orbitor3 = Object(mass=5.0, radius=5.0)
orbitor3.position = center + 50*xhat
orbitor3.velocity = 70*yhat

# *** ARROWS, GRIDS, AND TRAILS ***
radialArrow = Arrow(sun.position, orbitor3.position)
gameGrid = Grid(10,10, WIDTH, HEIGHT)
orbitorTrail1 = Trail(600)
orbitorTrail1.addPoint(orbitor1.position.copy())
orbitorTrail2 = Trail(300)
orbitorTrail2.addPoint(orbitor2.position.copy())
orbitorTrail3 = Trail(100)
orbitorTrail3.addPoint(orbitor3.position.copy())

# ***** GAME LOOP *****
while running:
    # pygame.QUIT means the user closed the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # wipe away anything from the previous frame
    screen.fill("black")

    currentPosition1 = orbitor1.position.copy()
    currentPosition2 = orbitor2.position.copy()
    currentPosition3 = orbitor3.position.copy()
    # add current position of the orbitor1 to the Trail object array every 20 frames
    if (frame % 5 == 0):
        orbitorTrail1.addPoint(currentPosition1)
        orbitorTrail2.addPoint(currentPosition2)
        orbitorTrail3.addPoint(currentPosition3)
    
    # set arrow data
    radialArrow.update(sun.position, orbitor3.position)

    # ***** RENDER THE GAME HERE *****
    
    # GRID
    gameGrid.drawRectangles(screen, colorFunction1)
    gameGrid.drawLines(screen, "white", 1)

    # TRAILS
    orbitorTrail1.draw(screen, "green", 1)
    orbitorTrail2.draw(screen, "green", 1)
    orbitorTrail3.draw(screen, "green", 1)

    # ORBITORS
    orbitor1.draw(screen, "blue")
    orbitor2.draw(screen, "orange")
    orbitor3.draw(screen, "red")

    # SUN
    sun.draw(screen, "yellow")

    # ARROWS
    radialArrow.draw(screen, "white", 3)
    
    # CALCULATE FORCES
    # force points from circle position to the center
    r1 = (orbitor1.position - sun.position)
    rhat1 = r1 / r1.magnitude()
    r2 = (orbitor2.position - sun.position)
    rhat2 = r2 / r2.magnitude()
    r3 = (orbitor3.position - sun.position)
    rhat3 = r3 / r3.magnitude()
    
    orbitor1.force = -((GRAV * sun.MASS * orbitor1.MASS) / (r1.magnitude() * r1.magnitude())) * rhat1
    orbitor2.force = -((GRAV * sun.MASS * orbitor2.MASS) / (r2.magnitude() * r2.magnitude())) * rhat2
    orbitor3.force = -((GRAV * sun.MASS * orbitor3.MASS) / (r3.magnitude() * r3.magnitude())) * rhat3

    # update acceleration, velocity, and position of each orbitor (NOT the sun... assuming Keplerian Limit M >> m)
    orbitor1.update(dt)
    orbitor2.update(dt)
    orbitor3.update(dt)

    # flip() display to send work to the screen
    pygame.display.flip()

    # limit to 60 fps
    dt = clock.tick(60) / 1000
    print(int(1/dt))
    frame += 1

pygame.quit()