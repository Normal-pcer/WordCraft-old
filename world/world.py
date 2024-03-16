class World:
    """
    wordcraft.world.World

    世界
    """
    from typing import List
    from chunk import Chunk

    loadedChunks: List[Chunk]
