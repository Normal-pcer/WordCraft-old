from block import Block
from util import Identifier
from typing import List

emptyBlock: Block = Block(Identifier("wordcraft", "air"))
emptyGrid: List[List[Block]]


class Chunk:
    """
    wordcraft.world.Chunk
    """

    topEdge: int = 320
    bottomEdge: int = 0
    chunkId: int
    """
    X (left edge) = chunkId*16
    """
    grid: List[List[Block]]

    @staticmethod
    def empty_block():
        return emptyBlock

    @staticmethod
    def empty_grid():
        return emptyGrid

    def __init__(self, chunk_id: int):
        self.chunkId = chunk_id

    def get_storage_name(self):
        return 'chunk_' + str(self.chunkId) + '.dat'

    @classmethod
    def empty(cls, chunk_id):
        """
        Generate an empty chunk (filled by wordcraft:air)
        Args:
            chunk_id: ID of the new chunk

        Returns:
            An empty chunk object

        """
        cls.grid = cls.empty_grid()
        cls.chunkId = chunk_id
        return cls

    def serialize(self):
        """
        Serialize self to a list.
        Returns:
            A list which stored data of self.
        """
        return self.grid


emptyGrid = [[emptyBlock for _ in range(16)] for _ in range(Chunk.bottomEdge, Chunk.topEdge + 1)]
