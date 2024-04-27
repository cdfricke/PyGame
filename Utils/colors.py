# File: colors.py
# Programmer: Connor Fricke (cd.fricke23@gmail.com)
# Latest Revision: 5-MAR-2024 --> Created
#
# Simple color functions for use in associating a pygame.Color
# value with a floating point value. Useful for various color
# associations and gradients.

import pygame

# ***** EXAMPLE COLOR FUNCTIONS *****
# black -> purple
def colorFunction1(x: float) -> pygame.Color:
    # r,g,b values must be integers between 0 and 255
    r = int(float(x) * 100)
    g = 0
    b = int(float(x) * 100)
    return pygame.Color(r, g, b)

# black -> white 
def colorFunction2(x: float) -> pygame.Color:
    # r,g,b values must be integers between 0 and 255
    r = int(float(x) * 255)
    g = int(float(x) * 255)
    b = int(float(x) * 255)
    return pygame.Color(r, g, b)

# red -> black
def colorFunction3(x: float) -> pygame.Color:
    # r,g,b values must be integers between 0 and 255
    r = 255 - int(float(x) * 255)
    g = 0
    b = 0
    return pygame.Color(r, g, b)

# red -> blue
def colorFunction4(x: float) -> pygame.Color:
    # r,g,b values must be integers between 0 and 255
    r = 255 - int(float(x) * 255)
    g = int(float(x) * 255)
    b = 0
    return pygame.Color(r, g, b)