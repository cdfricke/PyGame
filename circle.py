import pygame

#pygame initialization boilerplate
pygame.init()
screen = pygame.display.set_mode((720,440))
clock = pygame.time.Clock()
running = True
dt = 0

circlePosition = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# start run loop
while running:
    # pygame.QUIT means the user closed the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # wipe away anything from the previous frame
    screen.fill("black")

    # *** RENDER THE GAME HERE ***
    pygame.draw.circle(surface=screen, color="green", center=circlePosition, radius=40.0)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        circlePosition.y -= 300 * dt
    if keys[pygame.K_s]:
        circlePosition.y += 300 * dt
    if keys[pygame.K_a]:
        circlePosition.x -= 300 * dt
    if keys[pygame.K_d]:
        circlePosition.x += 300 * dt

    # flip() display to send work to the screen
    pygame.display.flip()

    # limit to 60 fps
    dt = clock.tick(60) / 1000

pygame.quit()
    
