class Player:
    """
    wordcraft.entity.Player

    玩家
    """
    from entity.playerEntity import PlayerEntity
    from util import Identifier
    playerEntity: PlayerEntity

    def __init__(self):
        self.playerEntity = self.PlayerEntity(
            self.Identifier("wordcraft", "player"))
