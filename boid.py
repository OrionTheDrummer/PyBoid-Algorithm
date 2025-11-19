import pygame as pg
from vec2 import Vec2


class Boid:
    def __init__(self, pos, vel):
        self.Position = pos
        self.Velocity = vel
        self.PerRadius = 100
        self.SepRadius = 30

        self.AlignmentStrength = 0.5
        self.CohesionStrength = 0.4
        self.SeparationStrength = 1.5

    def Update(self, dt):
        self.Position += self.Velocity * dt

    def Wrap(self, height, width):
        if self.Position.x > width:
            self.Position.x = 0
        if self.Position.x < 0:
            self.Position.x = width
        if self.Position.y > height:
            self.Position.y = 0
        if self.Position.y < 0:
            self.Position.y = height

    def Draw(self, screen):
        pg.draw.circle(screen, (255, 255, 255),
                       (int(self.Position.x), int(self.Position.y)), 5)

    def GetNeighbors(self, boids):
        neighbors = []

        for boid in boids:
            distance = (boid.Position - self.Position).length()
            if boid != self and distance < self.PerRadius:
                neighbors.append(boid)
        return neighbors

    # |====ALLIGHNMENT====|

    def GetAverageVel(self, neighbors):
        sumVel = Vec2(0, 0)

        if not neighbors:
            return self.Velocity

        for neighbor in neighbors:
            sumVel += neighbor.Velocity

        avgVel = sumVel * (1.0 / len(neighbors))
        return avgVel

    def Allignment(self, AvgVel):
        if AvgVel.length() == 0:
            return Vec2(0, 0)
        NorAvgVel = AvgVel.normalize()
        steering = (NorAvgVel - self.Velocity).normalize() * \
            self.AlignmentStrength
        return steering

    # |====COHESION====|
    def GetAveragePos(self, neighbors):
        sumPos = Vec2(0, 0)

        if not neighbors:
            return self.Position

        for neighbor in neighbors:
            sumPos += neighbor.Position

        avgPos = sumPos * (1.0 / len(neighbors))
        return avgPos

    def Cohesion(self, AvgPos):
        direction = AvgPos - self.Position
        direction = direction.normalize()
        CohesionForce = direction * self.CohesionStrength
        return CohesionForce

    # |====SEPARATION====|
    def Separation(self, neighbors):
        sumVec = Vec2(0, 0)

        for neighbor in neighbors:
            diff = self.Position - neighbor.Position
            distance = diff.length()
            if distance < self.SepRadius and distance > 0:
                contribution = diff.normalize() * (1 / distance)
                sumVec += contribution

        if sumVec.length() > 0:
            sumVec = sumVec.normalize() * self.SeparationStrength

        return sumVec
