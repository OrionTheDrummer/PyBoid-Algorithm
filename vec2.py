import math

class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Add two vectors
    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    # Subtract two vectors
    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)

    # Multiply vector by scalar
    def __mul__(self, scalar):
        return Vec2(self.x * scalar, self.y * scalar)

    # Support scalar * vector
    __rmul__ = __mul__

    # Length of vector
    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    # Normalize vector (length 1)
    def normalize(self):
        l = self.length()
        if l == 0:
            return Vec2(0, 0)
        return Vec2(self.x / l, self.y / l)

    # Clamp vector length to max_len
    def clamp(self, max_len):
        l = self.length()
        if l > max_len:
            return self.normalize() * max_len
        return self

    # Optional: string representation for debugging
    def __repr__(self):
        return f"Vec2({self.x:.2f}, {self.y:.2f})"
