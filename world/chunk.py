class Chunk:
    """
    wordcraft.world.Chunk
    """
    from typing import List
    from block import Block

    topEdge: int = 320
    bottomEdge: int = -64
    chunkId: int
    """
    X (left edge) = chunkId*16
    """
    grid: List[List[Block]]

    def __init__(self):
        pass

    def get_storage_name(self):
        return 'chunk_'+str(self.chunkId)+'.dat'