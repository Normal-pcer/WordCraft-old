class SaveDir:
    """
    wordcraft.world.SaveDir
    """
    root: str

    def __init__(self, root):
        self.root = root

    def read_file_content(self, file_name: str):
        """
        Read a file in save dir
        """
        import os
        import zlib

        complete_path = os.path.join(self.root, file_name)
        try:
            with open(complete_path, "rb") as f:
                file_content: bytes = zlib.decompress(f.read())
                return file_content
        except FileNotFoundError | zlib.error:
            return None


class World:
    """
    wordcraft.world.World
    """
    from typing import List
    from world.chunk import Chunk

    loadedChunks: List[Chunk]
    path: SaveDir
    name: str

    def __init__(self, name: str, path: SaveDir):
        self.name = name
        self.path = path
        self.loadedChunks = list()

    def load_chunk(self, chunk_id: int, default: Chunk = ...) -> Chunk:
        """
        Load a chunk by given chunk id.
        It will return default if not exist.
        """
        result_chunk = self.Chunk(chunk_id)
        # file_content = self.path.read_file_content(result_chunk.get_storage_name())
        return default if default is not ... else self.Chunk.empty(chunk_id)  # to be done

    def get_blocks(self, left: int, right: int, bottom: int, top: int, allow_load=True):
        # Calculate chunk id required
        min_id = left // 16
        max_id = right // 16

        required_chunks = [self.Chunk.empty(0)] * (max_id - min_id + 1)
        for i in range(min_id, max_id + 1):  # Make sure all chunks are loaded
            index = -1
            for j in range(len(self.loadedChunks)):
                element = self.loadedChunks[j]
                if element.chunkId == i:
                    index = j
                    required_chunks[i] = self.loadedChunks[j]
                    break
            if index == -1:  # Not loaded
                required_chunks[i] = self.load_chunk(i) if allow_load else self.Chunk.empty(i)
        catted_grid = [[self.Chunk.empty_block() for j in range(right - left + 1)]
                       for i in range(top - bottom + 1)]
        for i in required_chunks:
            result = i.grid[bottom:top + 1]
            if i.chunkId == min_id:
                result = result[left % 16:]
            if i.chunkId == max_id:
                result = result[:right % 16 + 1]
            for j in range(len(result)):
                catted_grid[j] += result[j]

        return catted_grid
