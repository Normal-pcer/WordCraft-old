class Vector2:
    """
    wordcraft.util.Position
    """
    x: float
    y: float

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def to_tuple(self):
        return self.x, self.y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __abs__(self) -> float:
        from math import sqrt, pow
        return sqrt(pow(self.x, 2) + pow(self.y, 2))

    def __mul__(self, other: float):
        return Vector2(self.x * other, self.y * other)

    def __str__(self):
        return "({}, {})".format(str(self.x), str(self.y))

    def __repr__(self):
        return "Vector2" + str(self)

    def to_int(self):
        return Vector2(int(self.x) * 1.0, int(self.y) * 1.0)
