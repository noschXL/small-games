#an boids simulation

import pygame
import sys
import random
from math import atan2, cos, sin, radians, degrees

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

class Boid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = random.uniform(0, 2 * 3.14159)

    def update(self, boids):
        separation_radius = 50
        alignment_radius = 100
        cohesion_radius = 100
        separation_force = 1
        alignment_force = 0.5
        cohesion_force = 0.3

        move_x, move_y = 0, 0

        for boid in boids:
            if boid == self:
                continue

            dx = boid.x - self.x
            dy = boid.y - self.y
            distance = (dx**2 + dy**2)**0.5

            # Separation
            if 0 < distance < separation_radius:
                move_x -= dx / distance * separation_force
                move_y -= dy / distance * separation_force

            # Alignment
            if 0 < distance < alignment_radius:
                move_x += cos(boid.angle) * alignment_force
                move_y += sin(boid.angle) * alignment_force

            # Cohesion
            if 0 < distance < cohesion_radius:
                move_x += dx / distance * cohesion_force
                move_y += dy / distance * cohesion_force

        # Update angle
        if move_x != 0 or move_y != 0:
            target_angle = atan2(move_y, move_x)
            angle_difference = target_angle - self.angle
            self.angle += angle_difference * 0.1

        # Move the boid
        speed = 2
        self.x += speed * cos(self.angle)
        self.y += speed * sin(self.angle)

        # Wrap around screen edges
        self.x %= width
        self.y %= height

    def draw(self):
        boid_surface = pygame.Surface((20, 30))
        boid_surface.set_colorkey((0, 0, 0))  # Set black as transparent color
        pygame.draw.polygon(boid_surface, (0, 128, 255), [(10, 0), (0, 30), (20, 30)])
        rotated_surface = pygame.transform.rotate(boid_surface, -degrees(self.angle) + 270)
        screen.blit(rotated_surface, (self.x - rotated_surface.get_width() / 2, self.y - rotated_surface.get_height() / 2))
        screen.blit(rotated_surface, (self.x - rotated_surface.get_width() / 2, self.y - rotated_surface.get_height() / 2))

# Create a list of boids
boids = [Boid(random.randint(0, width), random.randint(0, height)) for _ in range(50)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((64,66,64))

    for boid in boids:
        boid.update(boids)
        boid.draw()

    pygame.display.flip()
    clock.tick(60)
