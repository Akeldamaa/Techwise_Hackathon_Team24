import pygame
from pygame.locals import *
import random
import time

# Constants and colors
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
NUM_BOIDS = 50
MAX_SPEED = 4
MAX_FORCE = 0.1
SLEEP_TIME = 0.08
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BOID_RADIUS = 10

class Boid:
    def __init__(self):
        self.position = pygame.Vector2(random.uniform(0, WINDOW_WIDTH), random.uniform(0, WINDOW_HEIGHT))
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.velocity.scale_to_length(MAX_SPEED)
        self.acceleration = pygame.Vector2(0, 0)
        
    def update(self):
        self.position += self.velocity
        self.velocity += self.acceleration
        if self.velocity.length() > MAX_SPEED:
            self.velocity.scale_to_length(MAX_SPEED)
        self.acceleration = pygame.Vector2(0, 0)
        self.edges()
    
    def apply_force(self, force):
        self.acceleration += force
    
    def edges(self):
        if self.position.x > WINDOW_WIDTH:
            self.position.x = 1
        elif self.position.x < 0:
            self.position.x = WINDOW_WIDTH
        if self.position.y > WINDOW_HEIGHT:
            self.position.y = 1
        elif self.position.y < 0:
            self.position.y = WINDOW_HEIGHT
            
    def flock(self, boids):
        alignment = self.align(boids)
        cohesion = self.cohere(boids)
        separation = self.separate(boids)
        
        self.apply_force(alignment)
        self.apply_force(cohesion)
        self.apply_force(separation)
    
    def align(self, boids):
        perception_radius = 50
        steering = pygame.Vector2(0, 0)
        total = 0
        for boid in boids:
            if boid != self and self.position.distance_to(boid.position) < perception_radius:
                steering += boid.velocity
                total += 1
        if total > 0:
            steering /= total
            steering.scale_to_length(MAX_SPEED)
            steering -= self.velocity
            if steering.length() > MAX_FORCE:
                steering.scale_to_length(MAX_FORCE)
        return steering
    
    def cohere(self, boids):
        perception_radius = 50
        steering = pygame.Vector2(0, 0)
        total = 0
        for boid in boids:
            if boid != self and self.position.distance_to(boid.position) < perception_radius:
                steering += boid.position
                total += 1
        if total > 0:
            steering /= total
            steering -= self.position
            steering.scale_to_length(MAX_SPEED)
            steering -= self.velocity
            if steering.length() > MAX_FORCE:
                steering.scale_to_length(MAX_FORCE)
        return steering
    
    def separate(self, boids):
        perception_radius = 30
        desired_separation = 25
        steering = pygame.Vector2(0, 0)
        total = 0
        for boid in boids:
            distance = self.position.distance_to(boid.position)
            if boid != self and distance < perception_radius:
                diff = self.position - boid.position
                diff /= distance
                diff /= (distance / desired_separation)  # Scale separation force based on distance
                steering += diff
                total += 1
        if total > 0:
            steering /= total
            steering.scale_to_length(MAX_SPEED)
            steering -= self.velocity
            if steering.length() > MAX_FORCE:
                steering.scale_to_length(MAX_FORCE)
        return steering

    def draw(self, surface):
        # Calculate the points of the triangle based on boid's position and orientation
        points = [(self.position.x, self.position.y - BOID_RADIUS),
                  (self.position.x + BOID_RADIUS * 0.8, self.position.y + BOID_RADIUS * 0.6),
                  (self.position.x - BOID_RADIUS * 0.8, self.position.y + BOID_RADIUS * 0.6)]
        pygame.draw.polygon(surface, BLACK, points)

class Game:
    def __init__(self):
        pygame.init()
        self.running = True
        pygame.display.set_caption("Boids")
        self.surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.surface.fill(WHITE)
        self.boids = [Boid() for _ in range(NUM_BOIDS)]  # Create boids and add them to the list

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False

            self.surface.fill(WHITE)  # Clear the screen
            for boid in self.boids:
                boid.flock(self.boids)  # Apply flocking behavior
                boid.update()           # Update boid position
                boid.draw(self.surface) # Draw boid on the surface

            pygame.display.flip()
            clock.tick(60)  # Cap the frame rate

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()