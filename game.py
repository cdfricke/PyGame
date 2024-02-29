import pygame

#pygame initialization boilerplate
pygame.init()
screen = pygame.display.set_mode((720,440))
clock = pygame.time.Clock()
running = True
dt = 0

# ***** CLASS DEFINITION *****
class Circle:
    """This is the base object of my game"""
    def __init__(self):
        self.radius = 20.0
        self.position = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
        self.color = "blue"
        self.mass = 1.0

    # call draw() to automatically draw the circle with it's current attributes
    def draw(self):
        pygame.draw.circle(surface=screen, color=self.color, center=self.position, radius=self.radius)

    # radius can be a floating point value
    def setRadius(self, r):
        self.radius = r
    
    # x and y should be integers (i think)
    def setPosition(self, x, y):
        self.position = pygame.Vector2(x, y)

    # mass should be a floating point value
    def setMass(self, m):
        self.mass = m

    def setColor(self, c):
        self.color = c
    

myCircle = Circle()

# ***** GAME LOOP *****
while running:
    # pygame.QUIT means the user closed the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # wipe away anything from the previous frame
    screen.fill("black")

    # *** RENDER THE GAME HERE ***
    myCircle.draw()
    myCircle.position.x += 20

    if (myCircle.position.x > screen.get_width()):
        myCircle.position.x = 0

    # flip() display to send work to the screen
    pygame.display.flip()

    # limit to 60 fps
    dt = clock.tick(60) / 1000

pygame.quit()