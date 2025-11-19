import pygame as pg
from vec2 import Vec2
from boid import Boid
import random

# instances
clock = pg.time.Clock()

# vectors
WIDTH = 800
HEIGHT = 600
Position = Vec2(WIDTH/2, HEIGHT/2)
Velocity = Vec2(100, 50)

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.flip()


def main(position, screen):
    max_speed = 150
    max_force = 50

    Boids = []
    for i in range(40):
        vx = random.uniform(-50, 50)
        vy = random.uniform(-50, 50)
        velocity = Vec2(vx, vy)
        Boids.append(Boid(position, velocity))

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        dt = clock.tick(60) / 1000

        screen.fill((0, 0, 0))  # clear screen

        # boid loop
        for i, boid in enumerate(Boids):
            neighbors = boid.GetNeighbors(Boids)

            AvgVel = boid.GetAverageVel(neighbors)
            AlignmentForce = boid.Allignment(AvgVel)

            AvgPos = boid.GetAveragePos(neighbors)
            CohesionForce = boid.Cohesion(AvgPos)

            SeparationForce = boid.Separation(neighbors)

            steering = AlignmentForce + CohesionForce + SeparationForce

            if steering.length() > max_force:
                steering = steering.normalize() * max_force

            print(f"steering length: {steering.length()}")
            boid.Velocity += steering

            if boid.Velocity.length() > max_speed:
                boid.Velocity = boid.Velocity.normalize() * max_speed

            boid.Update(dt)
            boid.Wrap(HEIGHT, WIDTH)
            boid.Draw(screen)

            if i == 0:
                for neighbor in neighbors:
                    pg.draw.circle(
                        screen,
                        (0, 100, 255),   #
                        (int(boid.Position.x), int(boid.Position.y)),
                        boid.PerRadius,
                        1
                    )
                    pg.draw.line(
                        screen,
                        (0, 255, 0),  # green
                        (int(boid.Position.x), int(boid.Position.y)),
                        (int(neighbor.Position.x), int(neighbor.Position.y))
                    )

        pg.display.flip()


main(Position, screen)
