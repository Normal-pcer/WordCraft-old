class Block:
    """
    wordcraft.block.Block
    """
    from util import Identifier

    blockId: Identifier
    data: dict = {}

    def __init__(self, block_id: Identifier):
        self.blockId = block_id

    def __repr__(self):
        from client import WorldRenderer
        return WorldRenderer.BlockTexture.get_block_texture(self.blockId).character

    def serialize(self) -> dict | str:
        if self.data == {}:
            return str(self.blockId)  # No extra data
        else:
            return self.__dict__
