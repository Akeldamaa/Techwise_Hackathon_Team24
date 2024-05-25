from config import *
import pygame
from pygame.locals import *
import time
import random
from boid import Boid

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.running = True
        pygame.display.set_caption("Boids")
        self.surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.surface.fill(WHITE)
        self.boids = [Boid(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)) for _ in range(50)]

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False

            self.surface.fill(WHITE)  # Clear screen before drawing

            for boid in self.boids:
                boid.update()
                boid.draw(self.surface)

            pygame.display.flip()
            time.sleep(SLEEP_TIME)
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
