class Entity:
    """
    wordcraft.entity.Entity

    实体
    """

    from util import Vector2, Identifier

    position: Vector2
    typeId: Identifier
    speed: Vector2

    def __init__(self, type_id: Identifier):
        self.typeId = type_id
        self.position = self.Vector2(0.0, 0.0)
        self.speed = self.Vector2(0.0, 0.0)
