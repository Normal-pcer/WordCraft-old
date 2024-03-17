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
        :param file_name: Compressed file to be read
        :return: Uncompressed data of the file or None
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

    def write_file_content(self, file_name: str, data: bytes):
        """
        Write to a file in save dir
        :param file_name: File to be written
        :param data: Uncompressed data
        """
        import os
        import zlib

        complete_path = os.path.join(self.root, file_name)

        with open(complete_path, "wb") as f:
            file_content = zlib.compress(data)
            f.write(file_content)


class World:
    """
    wordcraft.world.World
    """
    from typing import List
    from world.chunk import Chunk
    from world.generator import Generator
    from block import Block

    loadedChunks: List[Chunk]
    path: SaveDir
    name: str
    generator: Generator

    def __init__(self, name: str, path: SaveDir):
        self.name = name
        self.path = path
        self.loadedChunks = list()
        self.generator = self.Generator(self.Generator.GeneratorType.flat)

    def load_chunk(self, chunk_id: int, default: Chunk = ...) -> Chunk:
        """Load a chunk from file

        Args:
            chunk_id: ID of file to be read
            default: Will be returned while file not exists. Defaults to Ellipsis.

        Returns:
            Target chunk object
        """
        result_chunk = default if default is not ... \
            else self.generator.generate_chunk(chunk_id)
        # file_content = self.path.read_file_content(result_chunk.get_storage_name())
        self.loadedChunks.append(result_chunk)
        return result_chunk  # to be done

    def save_chunk(self, chunk: Chunk):
        """
        Save a chunk to a file in save dir.
        Args:
            chunk: The chunk to be saved.

        Returns:
            None.
        """
        import json
        file = chunk.get_storage_name()
        content_str = json.dumps(chunk, default=lambda obj: obj.serialize())
        content = bytes(content_str, encoding="UTF-8")
        self.path.write_file_content(file, content)

    def save_all_chunks(self):
        """
        Save all loaded chunks.
        Returns:
            None.
        """
        for i in self.loadedChunks:
            self.save_chunk(i)

    def get_blocks(self, left: int, right: int, bottom: int,
                   top: int, allow_load=True) -> List[List[Block]]:
        if bottom < self.Chunk.bottomEdge:
            return ([[self.Chunk.empty_block() for _ in range(right - left + 1)] for _ in
                     range(self.Chunk.bottomEdge - bottom)] +
                    self.get_blocks(left, right, self.Chunk.bottomEdge, top, allow_load))
        if top > self.Chunk.topEdge:
            return self.get_blocks(left, right, bottom, self.Chunk.topEdge) + [
                [self.Chunk.empty_block() for _ in range(right - left + 1)] for _ in
                range(top - self.Chunk.topEdge)]
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
                required_chunks[i] = self.load_chunk(
                    i) if allow_load else self.Chunk.empty(i)
        catted_grid = [[] for _ in range(top - bottom + 1)]
        for i in required_chunks:
            result = i.grid[bottom:top + 1]
            for j in range(len(result)):
                row = result[j]
                if i.chunkId == min_id:
                    row = row[left % 16:]
                if i.chunkId == max_id:
                    row = row[:right % 16 + 1]
                catted_grid[j] += row

        return catted_grid
