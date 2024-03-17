class Chunk:
    """
    wordcraft.world.Chunk
    """
    from typing import List
    from block import Block
    from util import Identifier

    topEdge: int = 320
    bottomEdge: int = 0
    chunkId: int
    """
    X (left edge) = chunkId*16
    """
    grid: List[List[Block]]
    emptyGrid: List[List[Block]]
    emptyBlock: Block = Block(Identifier("wordcraft", "air"))

    @classmethod
    def empty_block(cls):
        return cls.emptyBlock

    @classmethod
    def empty_grid(cls):
        return cls.emptyGrid

    def __init__(self, chunk_id: int):
        self.chunkId = chunk_id

    def get_storage_name(self):
        return 'chunk_' + str(self.chunkId) + '.dat'

    @classmethod
    def empty(cls, chunk_id):
        """
        Generate an empty chunk (filled by wordcraft:air)
        """
        cls.grid = cls.empty_grid()
        cls.chunkId = chunk_id
        return cls


Chunk.emptyGrid = [[Chunk.empty_block() for j in range(16)] for i in
                   range(Chunk.bottomEdge, Chunk.topEdge + 1)]
