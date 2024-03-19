import pygame

# ***** EXAMPLE COLOR FUNCTIONS *****
# black -> purple
def colorFunction1(x):
    # r,g,b values must be integers between 0 and 255
    r = int(float(x) * 100)
    g = 0
    b = int(float(x) * 100)
    return pygame.Color(r, g, b)

# black -> white 
def colorFunction2(x):
    # r,g,b values must be integers between 0 and 255
    r = int(float(x) * 255)
    g = int(float(x) * 255)
    b = int(float(x) * 255)
    return pygame.Color(r, g, b)

# red -> black
def colorFunction3(x):
    # r,g,b values must be integers between 0 and 255
    r = 255 - int(float(x) * 255)
    g = 0
    b = 0
    return pygame.Color(r, g, b)

# red -> blue
def colorFunction4(x):
    # r,g,b values must be integers between 0 and 255
    r = 255 - int(float(x) * 255)
    g = 0
    b = int(float(x) * 255)
    return pygame.Color(r, g, b)
# ***********************************