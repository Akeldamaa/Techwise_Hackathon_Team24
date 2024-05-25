import pygame
import random
from config import *

class Boid:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.acceleration = pygame.Vector2(1, 1)

    def update(self):
        self.position += self.velocity
        self.velocity += self.acceleration
        self.acceleration = pygame.Vector2(0, 0)  # Reset acceleration

        # Keep boids within screen bounds
        if self.position.x > WINDOW_WIDTH:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = WINDOW_WIDTH
        if self.position.y > WINDOW_HEIGHT:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = WINDOW_HEIGHT

    def draw(self, surface):
        pygame.draw.circle(surface, BLACK, (int(self.position.x), int(self.position.y)), BOID_RADIUS)
