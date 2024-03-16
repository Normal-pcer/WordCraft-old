class Block:
    """
    wordcraft.block.Block

    方块
    """
    from util import Identifier

    blockId: Identifier

    def __init__(self, block_id: Identifier):
        self.blockId = block_id

    def __repr__(self):
        from client import WorldRenderer
        return WorldRenderer.BlockTexture.get_block_texture(self.blockId).character
