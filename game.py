# File: game.py
# Programmer: Connor Fricke (cd.fricke23@gmail.com)
# Last Revision:
#   28-Feb-2024 ---> defined commonly used vectors, object class, initialized project
# TODO:
#   - Find a good way to implement flipping of inFront boolean

import pygame

#pygame initialization boilerplate
pygame.init()
screen = pygame.display.set_mode((720,720))
clock = pygame.time.Clock()
running = True
dt = 0

# ***** VECTORS AND REFERENCE POINTS *****
# NOTE: in PyGame, the origin is the top left corner of the screen
xhat = pygame.Vector2(1.0, 0.0)
yhat = pygame.Vector2(0.0, 1.0)
zeroVec = pygame.Vector2(0.0, 0.0)
up_right = (xhat - yhat) / (2 ** 0.5)
down_right = (xhat + yhat) / (2 ** 0.5)
center = pygame.Vector2(screen.get_width() / 2.0, screen.get_height() / 2.0)
origin = zeroVec

# ***** CLASS DEFINITION *****
class Object:
    """This is the base object of my game. It is drawn in game as a circle"""
    def __init__(self):
        # constants
        self.RADIUS = 20.0
        self.COLOR = "blue"
        self.MASS = 1.0
        # variables
        self.position = center          # set position at middle of screen
        self.velocity = zeroVec         # set velocity to zero
        self.acceleration = zeroVec     # set acceleration to zero
    
    def __init__(self, radius, mass, color):
        # constants
        self.RADIUS = radius
        self.MASS = mass
        self.COLOR = color
        # variables
        self.position = center          # set position at middle of screen
        self.velocity = zeroVec         # set velocity to zero
        self.acceleration = zeroVec     # set acceleration to zero

    # call draw() to automatically draw the circle with it's current attributes
    def draw(self):
        pygame.draw.circle(surface=screen, color=self.COLOR, center=self.position, radius=self.RADIUS)

STARTPOS = center - 50*(yhat) + 50*(xhat)
orbitor = Object(mass=100.0, color="blue", radius=10.0)
orbitor.position = STARTPOS

sun = Object(mass=100.0, color="yellow",radius=20.0)

inFront = True  # to decide which object to draw "on top"
accumulatedTime = 0.0   # to record the amount of time passed

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
    force = (sun.position - orbitor.position)

    # update acceleration, velocity, and position
    orbitor.acceleration = force / orbitor.MASS
    orbitor.velocity += orbitor.acceleration
    orbitor.position += orbitor.velocity * dt

    # reverse direction at edges
    if ( (orbitor.position.y - orbitor.RADIUS) < 0 or (orbitor.position.y + orbitor.RADIUS) > screen.get_height()):
        orbitor.velocity.y *= -1   # reverse velocity y component
    if ( (orbitor.position.x - orbitor.RADIUS) < 0 or (orbitor.position.x + orbitor.RADIUS) > screen.get_width()):
        orbitor.velocity.x *= -1   # reverse velocity x component

    # flip() display to send work to the screen
    pygame.display.flip()

    # limit to 60 fps
    dt = clock.tick(60) / 1000
    accumulatedTime += dt

    # trigger the flipping of "inFront"
    if ((orbitor.velocity).magnitude() < 0.5):
        print("Flipping!")
        inFront = not inFront

pygame.quit()