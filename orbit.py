# File: game.py
# Programmer: Connor Fricke (cd.fricke23@gmail.com)
# Last Revision:
#   28-FEB-2024 ---> defined commonly used vectors, object class, initialized project
#   29-FEB-2024 ---> defined gravity as inverse square law, assessed TODO list
# TODO:
#   - Do force calculation from object array to prepare for N-body sim
#   - Allow for movement of sun
#   - Create and randomize locations / velocities of N-bodies
#   - Correct behavior of gravity for very small r
#   - Add some GUI stuff

import pygame
HEIGHT = 720
WIDTH = 720
#pygame initialization boilerplate
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

# necessary misc variables to keep track of
running = True  # for game loop
dt = 0          # for framerate independent physics
GRAV = 50.0     # gravitational constant, increasing this increases "strength" of gravity
inFront = True  # to decide which object to draw "on top"
frame = 0       # to keep track of frame number

# ***** VECTORS AND REFERENCE POINTS *****
# NOTE: in PyGame, the origin is the top left corner of the screen
xhat = pygame.Vector2(1.0, 0.0)     # DIRECTION: RIGHT
yhat = pygame.Vector2(0.0, 1.0)     # DIRECTION: DOWN
zero = pygame.Vector2(0.0, 0.0)     # ZERO VECTOR
center = pygame.Vector2(WIDTH / 2.0, HEIGHT / 2.0)  # DEFINED CENTER OF THE SCREEN

# ***** CLASS DEFINITION *****
class Object:
    """This is the base object of my game. It is drawn in game as a circle"""
    def __init__(self, radius, mass, color):
        # constants
        self.RADIUS = radius
        self.MASS = mass
        self.COLOR = color
        # variables
        self.position = center          # set position at middle of screen
        self.velocity = zero            # set velocity to zero
        self.acceleration = zero        # set acceleration to zero
        self.force = zero               # this is the force that the current object "feels"

    # call draw() to automatically draw the circle with it's current attributes
    def draw(self):
        pygame.draw.circle(surface=screen, color=self.COLOR, center=self.position, radius=self.RADIUS)

    def update(self, deltaTime):
        # update acceleration, velocity, and position
        self.acceleration = self.force / self.MASS
        self.velocity += self.acceleration
        self.position += self.velocity * deltaTime
    
    #def getForce(self, objectArray):
    #    for obj in objectArray:
    #        radialVec = obj.position - self.position
    #        self.force += radialVec

# ***** INITIAL CONDITIONS *****
STARTVEL = (50*xhat) + (50*yhat)
STARTPOS = center + (50*xhat) - (50*yhat) 

# orbitor object
orbitor = Object(mass=5.0, color="blue", radius=5.0)
orbitor.position = STARTPOS
orbitor.velocity = STARTVEL

# sun object, default position and velocity (centered, zero)
sun = Object(mass=100.0, color="yellow",radius=20.0)

# ***** GAME LOOP *****
while running:
    # pygame.QUIT means the user closed the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # wipe away anything from the previous frame
    screen.fill("black")

    # *** RENDER THE GAME HERE ***
    if (inFront):
        sun.draw()
        orbitor.draw()
    else:   
        orbitor.draw()
        sun.draw()

    # force points from circle position to the center
    rVec = (orbitor.position - sun.position)
    distanceTo = rVec.magnitude()
    rhat = rVec / distanceTo

    if (distanceTo > sun.RADIUS):
        orbitor.force = -((GRAV * sun.MASS * orbitor.MASS) / (distanceTo * distanceTo)) * rhat

    # update acceleration, velocity, and position
    VxBefore = orbitor.velocity.x
    orbitor.update(dt)
    VxAfter = orbitor.velocity.x

    # IF NECESSARY, reverse direction at edges
    #if ( (orbitor.position.y - orbitor.RADIUS) < 0 or (orbitor.position.y + orbitor.RADIUS) > screen.get_height()):
    #    orbitor.velocity.y *= -1   # reverse velocity y component
    #if ( (orbitor.position.x - orbitor.RADIUS) < 0 or (orbitor.position.x + orbitor.RADIUS) > screen.get_width()):
    #    orbitor.velocity.x *= -1   # reverse velocity x component

    # flip() display to send work to the screen
    pygame.display.flip()

    # limit to 60 fps
    dt = clock.tick(60) / 1000
    frame += 1

    # trigger the flipping of "inFront" when the x component of velocity changes sign
    if (VxBefore * VxAfter < 0):
        inFront = not inFront

pygame.quit()