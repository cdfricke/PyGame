# File: twobody.py
# Programmer: Connor Fricke (cd.fricke23@gmail.com)
# Last Revision:
#   29-FEB-2024 --> Created, v1

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
merged = False
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
    
    def getAccel(self, accelerator):
        rVec = accelerator.position - self.position
        r = rVec.magnitude()
        aVec = ((GRAV * accelerator.MASS) / (r*r*r)) * rVec
        return aVec

    def update(self, deltaTime, accelerator):
        # update acceleration, velocity, and position
        self.acceleration = self.getAccel(accelerator)
        self.velocity += self.acceleration
        self.position += self.velocity * deltaTime
    

# ***** INITIAL CONDITIONS *****
# orbitor1 object
orbitor1 = Object(mass=150.0, color="blue", radius=5.0)
orbitor1.position = center - (50*xhat)
orbitor1.velocity = (50*yhat)

# orbitor2 object
orbitor2 = Object(mass=150.0, color="green", radius=5.0)
orbitor2.position = center + (50*xhat)
orbitor2.velocity = -(50*yhat)

# ***** GAME LOOP *****
while running:
    # pygame.QUIT means the user closed the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # wipe away anything from the previous frame
    screen.fill("black")

    # *** RENDER THE GAME HERE ***
    if ( (orbitor1.position - orbitor2.position).magnitude() < orbitor1.RADIUS ):
        merged = True
        mergedObj = Object(mass=2*orbitor1.MASS, radius=orbitor1.RADIUS*1.44, color="white")
        mergedObj.position = orbitor1.position
        mergedObj.velocity = zero
    
    if (not merged):
        orbitor1.draw()
        orbitor2.draw()
        orbitor1.update(dt, orbitor2)
        orbitor2.update(dt, orbitor1)
    else:
        mergedObj.draw()

    

    

    # IF NECESSARY, reverse direction at edges
    #if ( (orbitor1.position.y - orbitor1.RADIUS) < 0 or (orbitor1.position.y + orbitor1.RADIUS) > screen.get_height()):
    #    orbitor1.velocity.y *= -1   # reverse velocity y component
    #if ( (orbitor1.position.x - orbitor1.RADIUS) < 0 or (orbitor1.position.x + orbitor1.RADIUS) > screen.get_width()):
    #    orbitor1.velocity.x *= -1   # reverse velocity x component

    # flip() display to send work to the screen
    pygame.display.flip()

    # limit to 60 fps
    dt = clock.tick(60) / 1000
    frame += 1

pygame.quit()