class Block:
    """
    wordcraft.block.Block

    方块
    """
    from util import Identifier

    blockId: Identifier

    def __init__(self, block_id: Identifier):
        self.blockId = block_id
