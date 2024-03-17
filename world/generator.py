class Generator:
    """
    wordcraft.world.Generator
    """
    from enum import Enum

    class GeneratorType(Enum):
        flat = 0
        normal = 1

    seed: int
    generatorType: GeneratorType

    def __init__(self, gen_type: GeneratorType, seed=-1):
        self.seed = seed
        self.generatorType = gen_type

    def generate_chunk(self, chunk_id: int):
        from world.chunk import Chunk
        from block import Block
        from util import Identifier

        if self.generatorType is self.GeneratorType.flat:
            result_chunk = Chunk(chunk_id)
            template = [("wordcraft", "bedrock")] * 1 + \
                       [("wordcraft", "stone")] * 2 + \
                       [("wordcraft", "grass_block")] * 1

            grid = list()
            for i in template:
                grid.append([Block(Identifier(*i)) for _ in range(16)])
            grid = grid + [[result_chunk.empty_block() for _ in range(16)]
                           for _ in range(result_chunk.topEdge - result_chunk.bottomEdge - len(template) + 1)]
            result_chunk.grid = grid
            return result_chunk

        else:
            return Chunk.empty(chunk_id)
