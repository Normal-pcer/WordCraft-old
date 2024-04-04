class Entity:
    """
    wordcraft.entity.Entity

    实体
    """

    from util import Vector2, Identifier

    position: Vector2
    typeId: Identifier

    def __init__(self, type_id):
        self.typeId = type_id
        self.position = self.Vector2(0.0, 0.0)
