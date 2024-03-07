# File: orbit.py
# Programmer: Connor Fricke (cd.fricke23@gmail.com)
# Last Revision:
#   28-FEB-2024 ---> defined commonly used vectors, object class, initialized project
#   29-FEB-2024 ---> defined gravity as inverse square law, assessed TODO list
# TODO:
#   - Do force calculation from object array to prepare for N-body sim
#   - Allow for movement of sun
#   - Add some GUI stuff

# *** INITIALIZE ***
import pygame
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
        leftAngled = self.tail + (0.9 * self.length * self.direction) + (0.1 * self.length * self.perpendicular)
        rightAngled = self.tail + (0.9 * self.length * self.direction) - (0.1 * self.length * self.perpendicular)
        points = [leftAngled, self.tip, rightAngled]
        pygame.draw.lines(surface=surface, color=color, closed=False, points=points, width=thickness)

    # same as constructor just allows us to manipulate the arrow after the object is constructed
    def setTailToTip(self, tail, tip):
        self.tip = tip
        self.tail = tail
        self.length = (tip - tail).magnitude()
        self.direction = (tip - tail) / self.length
        self.perpendicular = pygame.Vector2(self.direction.y, -self.direction.x)

# GRID: class object for drawing a grid with a certain number of rows and columns on the screen.
class Grid:
    def __init__(self, rows, columns):
        self.numRows = rows
        self.numCols = columns
        self.xticks = list(range(0, WIDTH + 1, int(WIDTH / columns)))
        self.yticks = list(range(0, HEIGHT + 1, int(HEIGHT / rows)))
    
    def draw(self, surface, color, thickness):
        for tick in self.xticks:
            start = tick*xhat
            end = start + HEIGHT*yhat
            pygame.draw.line(surface=surface, color=color, start_pos=start, end_pos=end, width=thickness)
        for tick in self.yticks:
            start = tick*yhat
            end = start + WIDTH*xhat
            pygame.draw.line(surface=surface, color=color, start_pos=start, end_pos=end, width=thickness)


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
    def __init__(self):
        self.pointArray = []
        
    def draw(self, surface, color, width):
        pygame.draw.aalines(surface=surface, color=color, closed=False, points=self.pointArray, blend=1)

    def addPoint(self, point):
        self.pointArray.append(point)
        # limit trail length to 50 points (experimental value)
        if (len(self.pointArray) > 700):
            self.pointArray.pop(0)
        
# *************************

# ***** INITIAL CONDITIONS *****
# orbitor object, non-default position and velocity
orbitor = Object(mass=5.0, radius=10.0)
orbitor.position = center + 250*xhat
orbitor.velocity = 30*yhat
# sun object, default position and velocity
sun = Object(mass=100.0, radius=20.0)

radialArrow = Arrow(sun.position, orbitor.position)
gameGrid = Grid(20,20)
earthTrail = Trail()
earthTrail.addPoint(orbitor.position.copy())

# ***** GAME LOOP *****
while running:
    # pygame.QUIT means the user closed the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # wipe away anything from the previous frame
    screen.fill("black")

    currentPosition = orbitor.position.copy()
    # add current position of the orbitor to the Trail object array every 20 frames
    if (frame % 5 == 0):
        earthTrail.addPoint(currentPosition)

    # *** RENDER THE GAME HERE ***
    gameGrid.draw(screen, "dark grey", 1)
    earthTrail.draw(screen, "green", 1)

    if (inFront):
        sun.draw(screen, "yellow")
        orbitor.draw(screen, "blue")
    else:   
        orbitor.draw(screen, "blue")
        sun.draw(screen, "yellow")

    radialArrow.setTailToTip(sun.position, orbitor.position)
    radialArrow.draw(screen, "red", 3)
    
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