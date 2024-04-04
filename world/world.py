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
        except FileNotFoundError:
            return None
        except zlib.error:
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
    from entity import Entity, Player

    loadedChunks: List[Chunk]
    path: SaveDir
    name: str
    generator: Generator
    tick: int
    lastTickTime: float = 0.0
    MAX_TPS = 20

    def __init__(self, name: str, path: SaveDir):
        self.name = name
        self.path = path
        self.loadedChunks = list()
        self.generator = self.Generator(self.Generator.GeneratorType.flat)

    def init(self, player: Player):
        from time import perf_counter
        initial_chunk = self.get_chunk(int(player.playerEntity.position.x) // 16)
        initial_chunk.entities.append(player.playerEntity)
        self.lastTickTime = perf_counter()

    def get_chunk(self, chunk_id: int, default: Chunk = ...) -> Chunk:
        for c in self.loadedChunks:
            if c.chunkId == chunk_id:
                return c

        return self.load_chunk(chunk_id, default)

    def load_chunk(self, chunk_id: int, default: Chunk = ...) -> Chunk:
        """Load a chunk from file

        Args:
            chunk_id: ID of file to be read
            default: Will be returned while file not exists. Defaults to Ellipsis.

        Returns:
            Target chunk object
        """
        result_chunk = self.Chunk.empty(chunk_id)
        file_content = self.path.read_file_content(
            result_chunk.get_storage_name())
        if file_content is not None:
            import json
            from typing import List, Dict
            from util import Identifier

            file_content_str = str(file_content, encoding="UTF-8")
            file_content_list: List[List[str | Dict[str, any]]] = (
                json.loads(file_content_str))
            for row in range(result_chunk.topEdge - result_chunk.bottomEdge + 1):
                for block in range(16):
                    block_data = file_content_list[row][block]
                    block_object: World.Block
                    if isinstance(block_data, str):
                        block_object = self.Block(Identifier.deserialize(block_data))
                    else:
                        raise Exception("Unwritten function")
                        # block_object = self.Block(Identifier(block_data["blockId"]))
                    result_chunk.grid[row][block] = block_object
        else:
            result_chunk = default if default is not ... else \
                self.generator.generate_chunk(chunk_id)
        self.loadedChunks.append(result_chunk)
        return result_chunk

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

    def get_blocks(self, left: int, right: int, bottom: int, top: int, allow_load=True) \
            -> List[List[Block]]:
        if bottom < self.Chunk.bottomEdge:
            return ([[self.Chunk.empty_block() for _ in range(right - left + 1)] for _ in
                     range(self.Chunk.bottomEdge - bottom)] + self.get_blocks(
                left, right, self.Chunk.bottomEdge, top, allow_load))
        if top > self.Chunk.topEdge:
            return self.get_blocks(left, right, bottom, self.Chunk.topEdge) + [
                [self.Chunk.empty_block() for _ in range(right - left + 1)] for _ in
                range(top - self.Chunk.topEdge)]  # Calculate chunk id required
        min_id = left // 16
        max_id = right // 16

        required_chunks = list()
        for i in range(min_id, max_id + 1):  # Make sure all chunks are loaded
            index = -1
            for j in range(len(self.loadedChunks)):
                element = self.loadedChunks[j]
                if element.chunkId == i:
                    index = j
                    required_chunks.append(self.loadedChunks[j])
                    break
            if index == -1:  # Not loaded
                required_chunks.append(self.load_chunk(
                    i) if allow_load else self.Chunk.empty(i))
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

    def tick(self):
        from time import perf_counter
        current_time = perf_counter()

        if (current_time - self.lastTickTime) < 1 / self.MAX_TPS:
            return

        for c in self.loadedChunks:
            for e in c.entities:
                # Calculate position
                e.position = e.position + e.speed * (current_time - self.lastTickTime)
                # Resistant force
                if e.speed.x > 0:
                    e.speed.x = max(0.0, e.speed.x - 5.0 * (current_time - self.lastTickTime))
                    print(e.speed.x)
                else:
                    e.speed.x = min(0.0, e.speed.x + 5.0 * (current_time - self.lastTickTime))

        self.lastTickTime = current_time

    def entity_on_solid(self, entity: Entity):
        container_chunk = self.get_chunk(int(entity.position.x) // 16)
        if entity.position.y - int(entity.position.y) < 0.1:
            if (container_chunk.grid[int(entity.position.y)][int(entity.position.x) % 16]
                    .blockId is not self.Chunk.empty_block().blockId):
                return True
        return False
