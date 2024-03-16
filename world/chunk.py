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
    emptyGrid: List[List[Block]]

    @staticmethod
    def empty_block():
        from util import Identifier
        from block import Block
        return Block(Identifier("wordcraft", "air"))

    @classmethod
    def empty_grid(cls):
        return [[cls.empty_block() for j in range(16)]
                for i in range(cls.bottomEdge, cls.topEdge)]

    def __init__(self, chunk_id):
        self.chunkId = chunk_id

    def get_storage_name(self):
        return 'chunk_' + str(self.chunkId) + '.dat'

    @classmethod
    def empty(cls, chunk_id):
        """
        Generate an empty chunk (filled by wordcraft:air)
        """
        from util import Identifier
        from block import Block
        cls.emptyBlock = Block(Identifier("wordcraft", "air"))
        cls.emptyGrid = [[Block(Identifier("wordcraft", "air")) for j in range(16)]
                         for i in range(cls.bottomEdge, cls.topEdge)]
        cls.grid = cls.emptyGrid
        cls.chunkId = chunk_id
        return cls
