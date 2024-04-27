# Programmer: Connor Fricke
# File: satellite.py
# Latest Revision: 22-APR-2024 ---> Created
#
# Class file for Satellite. Primary object used in PyGame orbital simulations.

import pygame

class Satellite:
    """
    Main orbitor object in simulation.
    """
    def __init__(self, radius, mass):
        # constants
        self.RADIUS = radius
        self.MASS = mass
        # variables
        self.position = pygame.Vector2(0,0)
        self.velocity = pygame.Vector2(0,0)        
        self.acceleration = pygame.Vector2(0,0)

    # call draw() to automatically draw the circle with it's current attributes
    def draw(self, surface, color):
        """Renders Satellite object as a circle"""
        pygame.draw.circle(surface=surface, color=color, center=self.position, radius=self.RADIUS)

    def setPosition(self, pos):
        self.position = pos

    def setVelocity(self, vel):
        self.velocity = vel

    def update(self, deltaTime):
        """
        Calculates instantaneous velocity and position change based on accelaration
        """
        # v_f = v_0 + at
        self.velocity += self.acceleration * deltaTime
        # x_f = x_0 + vt
        self.position += self.velocity * deltaTime  