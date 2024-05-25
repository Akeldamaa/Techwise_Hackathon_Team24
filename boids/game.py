import pygame
from pygame.locals import *
from config import *
import boid as boid

# Finished hackathon 9:57 PM

class Game:
    def __init__(self):
        pygame.init()
        self.running = True
        pygame.display.set_caption("Boids")
        self.surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        # self.surface.fill(WHITE)
        self.background_image = pygame.image.load('sky-background.jpg')
        self.surface.blit(self.background_image, (0, 0))
        self.boids = [boid.Boid() for _ in range(NUM_BOIDS)]  # Create boids and add them to the list

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False

            # Clear the screen
            self.surface.blit(self.background_image, (0, 0))
            for boid in self.boids:
                boid.flock(self.boids)  # Apply flocking behavior
                boid.update()  # Update boid position
                boid.draw(self.surface)  # Draw boid on the surface

            pygame.display.flip()
            clock.tick(60)  # Cap the frame rate

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
