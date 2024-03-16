class Entity:
    """
    wordcraft.entity.Entity

    实体
    """

    from util import Position, Identifier

    position: Position
    typeId: Identifier

    def __init__(self, type_id):
        self.typeId = type_id
