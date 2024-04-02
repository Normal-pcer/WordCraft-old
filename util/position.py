class Position:
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
