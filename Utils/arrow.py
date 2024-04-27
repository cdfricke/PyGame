# File: arrow.py
# Programmer: Connor Fricke (cd.fricke23@gmail.com)
# Last Revision:
#   17-MAR-2024 --> Created, v1

import pygame

# ARROW : class object for drawing arrows between positions on the screen.
class Arrow:
    
    def __init__(self, tail: pygame.Vector2, tip: pygame.Vector2):
        """
        Arrow.__init__(tail, tip):
        parameters:
          tail: location of the tail of the arrow, given by a pygame.Vector2 object.
          tip: location of the tip of the arrow, given by a pygame.Vector2 object.
        *************
        This constructor defines the only necessary parameters to describe an arrow, which is two locations in 2D space.
        Arrow objects should be created with this constructor, and they point from the first parameter (2D Vector location) to the
        second parameter (2D Vector location).
        Further details for drawing the arrow are given as parameters to the draw() function.
        """
        self.tip = tip
        self.tail = tail
    
    def draw(self, surface: pygame.Surface, color: pygame.Color, thickness: int) -> None:
        """
        Arrow.draw(surface, color, thickness):
        parameters:
          surface: the surface of the PyGame for the arrow to be drawn on, usually the screen.
          color: the color of the arrow. Should be a pygame.color object.
          thickness: the width, in pixels of the body of the arrow.
        *************
        This function is used to draw an arrow to a specified surface with particular color and thickness parameters.
        The proportions of the head of the arrow are defined based on a scaling relation with the length of the arrow. For example,
        the currently defined method of drawing the arrow places the tip of the left and right lines of the "arrowhead" at a location that is 98%
        along the length of the arrow from tail to tip and a distance from the body of the arrow defined as 2% of the length of the arrow from
        tail to tip. As long as the percentanges add up to 1 (e.g. 98% + 2%), the arrowhead will make 45 degree angles with the body of the arrow.
        """
        length = (self.tip - self.tail).magnitude()
        direction = (self.tip - self.tail) / length
        perpendicular = pygame.Vector2(direction.y, -direction.x)
        # angled tip
        leftAngled = self.tail + (0.8 * length * direction) + (0.2 * length * perpendicular)
        rightAngled = self.tail + (0.8 * length * direction) + (-0.2 * length * perpendicular)
        points = [leftAngled, self.tip, rightAngled]
        pygame.draw.lines(surface=surface, color=color, closed=False, points=points, width=thickness)
        # central body
        pygame.draw.line(surface=surface, color=color, start_pos=self.tail, end_pos=self.tip, width=thickness)

    
    def update(self, tail: pygame.Vector2, tip: pygame.Vector2) -> None:
        """
        Arrow.update(tail, tip):
        parameters:
          tail: the new location of the tail of the arrow
          tip: the new location of the tip of the arrow
        *************
        This function is a simple function designed for post-initialization manipulation of arrow objects.
        It mirrors the __init__ constructor.
        """
        self.tip = tip
        self.tail = tail