# File. arrow.py
# Programmer: Connor Fricke (cd.fricke23@gmail.com)
# Last Revision:
#   17-MAR-2024 --> Created, v1

import pygame
import random as r

# *** INITIALIZE ***
WIDTH = 720
HEIGHT = 720
pygame.init()
screen = pygame.display.set_mode((WIDTH+1, HEIGHT+1))
clock = pygame.time.Clock()
running = True
# ******************

# *** COMMON VECTORS AND LOCATIONS ***
center = pygame.Vector2(WIDTH / 2, HEIGHT / 2)
origin = pygame.Vector2(0, 0)
xhat = pygame.Vector2(1, 0)
yhat = pygame.Vector2(0, 1)
# ************************************

# *** CLASS DEFINITIONS ***
# NOTE THAT THESE CLASS DEFINITIONS RELY ON SOME OF THE DEFINED VARIABLES ABOVE

# ARROW : class object for drawing arrows between positions on the screen.
class Arrow:
    # Arrow.__init__(tail, tip):
    # parameters:
    #   tail: location of the tail of the arrow, given by a pygame.Vector2 object.
    #   tip: location of the tip of the arrow, given by a pygame.Vector2 object.
    # *************
    # This constructor defines the only necessary parameters to describe an arrow, which is two locations in 2D space.
    # Arrow objects should be created with this constructor, and they point from the first parameter (2D Vector location) to the
    # second parameter (2D Vector location).
    # Further details for drawing the arrow are given as parameters to the draw() function.
    def __init__(self, tail, tip):
        self.tip = tip
        self.tail = tail
        self.length = (tip - tail).magnitude()
        self.direction = (tip - tail) / self.length
        self.perpendicular = pygame.Vector2(self.direction.y, -self.direction.x)

    # Arrow.draw(surface, color, thickness):
    # parameters:
    #   surface: the surface of the PyGame for the arrow to be drawn on, usually the screen.
    #   color: the color of the arrow. Should be a pygame.color object.
    #   thickness: the width, in pixels of the body of the arrow.
    # *************
    # This function is used to draw an arrow to a specified surface with particular color and thickness parameters.
    # The proportions of the head of the arrow are defined based on a scaling relation with the length of the arrow. For example,
    # the currently defined method of drawing the arrow places the tip of the left and right lines of the "arrowhead" at a location that is 98%
    # along the length of the arrow from tail to tip and a distance from the body of the arrow defined as 2% of the length of the arrow from
    # tail to tip. As long as the percentanges add up to 1 (e.g. 98% + 2%), the arrowhead will make 45 degree angles with the body of the arrow.
    def draw(self, surface, color, thickness):
        # central body
        pygame.draw.line(surface=surface, color=color, start_pos=self.tail, end_pos=self.tip, width=thickness)
        # angled tip
        leftAngled = self.tail + (0.98 * self.length * self.direction) + (0.02 * self.length * self.perpendicular)
        rightAngled = self.tail + (0.98 * self.length * self.direction) - (0.02 * self.length * self.perpendicular)
        points = [leftAngled, self.tip, rightAngled]
        pygame.draw.lines(surface=surface, color=color, closed=False, points=points, width=thickness)

    # Arrow.update(tail, tip):
    # parameters:
    #   tail: the new location of the tail of the arrow
    #   tip: the new location of the tip of the arrow
    # *************
    # This function is a simple function designed for post-initialization manipulation of arrow objects.
    # It mirrors the __init__ constructor.
    def update(self, tail, tip):
        self.tip = tip
        self.tail = tail
        self.length = (tip - tail).magnitude()
        self.direction = (tip - tail) / self.length
        self.perpendicular = pygame.Vector2(self.direction.y, -self.direction.x)

# *************************************

# create arrow object, defined as Arrow(tail, tip)
centerArrow = Arrow(origin, center)

# *** GAME LOOP ***
while (running):
    # wipe away anything from the previous frame
    screen.fill("black")

    # *** RENDER THE GAME HERE ***
    # draw arrow, but each frame update the tip of the arrow up a pixel, down a pixel, or not at all.
    # After an infinite amount of time, the avg location of the tip should be very near the center if randint() is truly random.
    centerArrow.draw(screen, "white", 5)
    centerArrow.update(origin, centerArrow.tip + r.randint(-1, 1)*yhat)
    # *** END RENDERING ***

    # pygame.QUIT means the user closed the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
# *****************

pygame.quit()