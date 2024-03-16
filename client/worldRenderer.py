class WorldRenderer:
    """
    wordcraft.client.WorldRenderer
    Rendering objects (blocks, entities, etc.) in the world on game window.
    """
    import pygame
    from entity import Player
    gameWindow = pygame.Surface
    relativePlayer: Player

    class BlockTexture:
        """
        wordcraft.client.WorldRenderer.BlockTexture
        """
        from typing import Tuple
        from util import Identifier

        character: str
        color: Tuple[int]

        def __init__(self, character: str, color: Tuple[int]):
            self.character = character
            self.color = color

        @classmethod
        def get_block_texture(cls, identifier: Identifier, default=("材质丢失", (0, 0, 0))):
            """
            Get a block texture object by the given identifier.
            Default: Return when unable to find the texture file, etc.
            """
            from util import Read, Debug
            # Read index of texture packs
            textures_index_file = Read.read_str("textures/index.json", default=lambda e: Debug.Log.warning(
                "Exception while reading textures index: " + repr(e)))
            if textures_index_file is not None:
                import json
                try:
                    textures_index = json.loads(textures_index_file)
                    # Read texture packs in json order
                    for texture_pack in textures_index:
                        block_json_file = Read.read_str(
                            "textures/" + texture_pack + "/" + identifier.namespace + "/blocks/blocks.json")
                        try:
                            if block_json_file is None:
                                continue
                            else:
                                blocks_texture_dict = json.loads(
                                    block_json_file)
                                if identifier.path in blocks_texture_dict:
                                    return cls(*blocks_texture_dict[identifier.path]) # 
                                else:
                                    continue
                        except json.decoder.JSONDecodeError as exception:
                            Debug.Log.warning(
                                "Exception while loading " + "textures/" + texture_pack + "/" +
                                identifier.namespace + "/blocks/blocks.json" + ":" + repr(exception))
                except json.decoder.JSONDecodeError as exception:
                    Debug.Log.warning(
                        "Exception while loading textures index: " + repr(exception))
            return cls(*default)

    def __init__(self, game_window: pygame.Surface):
        self.gameWindow = game_window

    def frame(self):
        from util import Identifier

        font = self.pygame.font.SysFont("Simsun", 60)
        texture: WorldRenderer.BlockTexture = WorldRenderer.BlockTexture.get_block_texture(Identifier(
            "wordcraft", "grass_block"))
        text = font.render(texture.character, True, texture.color)
        self.gameWindow.blit(text, (-20, 50))
