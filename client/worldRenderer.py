_cache_texture = {}


class WorldRenderer:
    """
    wordcraft.client.WorldRenderer
    Rendering objects (blocks, entities, etc.) in the world on game window.
    """
    import pygame
    from entity import Player
    from world import World
    gameWindow = pygame.Surface
    relativePlayer: Player

    runningSave: World
    fontSize = 60

    class BlockTexture:
        """
        wordcraft.client.WorldRenderer.BlockTexture
        """
        from typing import Tuple
        from util import Identifier
        import pygame

        character: str
        color: Tuple[int]
        font: pygame.font.Font

        def __init__(self, character: str, color: Tuple[int],
                     font="Microsoft YaHei", font_size=60):
            self.character = character
            self.color = color
            self.font = self.pygame.font.SysFont(font, font_size)

        @classmethod
        def get_block_texture(cls, identifier: Identifier,
                              default=("材质丢失", (0, 0, 0))):
            """
            Get a block texture object by the given identifier.
            default: Return when unable to find the texture file, etc.
            """
            if str(identifier) in _cache_texture:
                return _cache_texture[str(identifier)]
            from util import Read, Debug
            # Read index of texture packs
            textures_index_file = Read.read_str(
                "textures/index.json", default=lambda e: Debug.Log.warning(
                    "Exception while reading textures index: " + repr(e)))
            if textures_index_file is not None:
                import json
                try:
                    textures_index = json.loads(textures_index_file)
                    # Read texture packs in json order
                    for texture_pack in textures_index:
                        block_json_file = Read.read_str(
                            "textures/" + texture_pack + "/" +
                            identifier.namespace + "/blocks/blocks.json")
                        try:
                            if block_json_file is None:
                                continue
                            else:
                                blocks_texture_dict = json.loads(
                                    block_json_file)
                                if identifier.path in blocks_texture_dict:
                                    _cache_texture[str(identifier)] = (
                                        cls(*blocks_texture_dict[identifier.path]))
                                    return cls(*blocks_texture_dict[identifier.path])
                                else:
                                    continue
                        except json.decoder.JSONDecodeError as exception:
                            Debug.Log.warning(
                                "Exception while loading " + "textures/" + texture_pack
                                + "/" + identifier.namespace + "/blocks/blocks.json" + ":"
                                + repr(exception))
                except json.decoder.JSONDecodeError as exception:
                    Debug.Log.warning(
                        "Exception while loading textures index: " + repr(exception))
            return cls(*default)

        def to_surface(self):
            """
            Convert to a pygame.Surface object
            """
            return self.font.render(self.character, True, self.color)

    class EntityTexture:
        from typing import Tuple, List
        from util import Identifier, Vector2
        import pygame

        characters: List[str]
        color: Tuple[int]
        font: pygame.font.Font
        fontSize: int

        def __init__(self, characters: List[str], color: Tuple[int], font="Microsoft YaHei",
                     font_size=60):
            self.characters = characters
            self.color = color
            self.font = self.pygame.font.SysFont(font, font_size)
            self.fontSize = font_size
            ...

        @classmethod
        def get_entity_texture(cls, identifier: Identifier,
                               default=(["〇"], (0, 0, 0))):
            """
            Get an entity texture object by the given identifier.
            default: Return when unable to find the texture file, etc.
            """

            if str(identifier) in _cache_texture:
                return _cache_texture[str(identifier)]
            from util import Read, Debug
            # Read index of texture packs
            textures_index_file = Read.read_str(
                "textures/index.json", default=lambda e: Debug.Log.warning(
                    "Exception while reading textures index: " + repr(e)))
            if textures_index_file is not None:
                import json
                try:
                    textures_index = json.loads(textures_index_file)
                    # Read texture packs in json order
                    for texture_pack in textures_index:
                        block_json_file = Read.read_str(
                            "textures/" + texture_pack + "/" +
                            identifier.namespace + "/entities/entities.json")
                        try:
                            if block_json_file is None:
                                continue
                            else:
                                blocks_texture_dict = json.loads(
                                    block_json_file)
                                if identifier.path in blocks_texture_dict:
                                    _cache_texture[str(identifier)] = (
                                        cls(*blocks_texture_dict[identifier.path]))
                                    return cls(*blocks_texture_dict[identifier.path])
                                else:
                                    continue
                        except json.decoder.JSONDecodeError as exception:
                            Debug.Log.warning(
                                "Exception while loading " + "textures/" + texture_pack
                                + "/" + identifier.namespace + "/entities/entities.json" + ":"
                                + repr(exception))
                except json.decoder.JSONDecodeError as exception:
                    Debug.Log.warning(
                        "Exception while loading textures index: " + repr(exception))
            return cls(*default)

        def blit(self, window: pygame.surface.Surface, destination: Vector2) -> None:
            """
            Display this on a game window.
            destination: left top screen position
            """
            for y_block in range(len(self.characters)):
                for x_block in range(len(self.characters[y_block])):
                    element = self.characters[y_block][x_block]
                    p_x = destination.x + self.fontSize * x_block
                    p_y = destination.y + self.fontSize * y_block
                    window.blit(self.font.render(element, True, self.color),
                                (p_x, p_y))
                    ...

            # return self.font.render(self.character, True, self.color)

    def __init__(self, game_window: pygame.Surface, running_save: World,
                 player: Player):
        self.gameWindow = game_window
        self.runningSave = running_save
        self.relativePlayer = player

    def frame(self):
        import math
        from util import Vector2
        from time import perf_counter

        # Calculate grid size required
        width, height = self.gameWindow.get_size()
        half_width = (width - self.fontSize) / 2
        quarter_height = (height - self.fontSize) / 4

        player_to_left_blocks = math.ceil(half_width / self.fontSize) + 1
        player_to_right_blocks = math.ceil(half_width / self.fontSize) + 1
        player_to_bottom_blocks = math.ceil(quarter_height / self.fontSize) + 1
        player_to_top_blocks = math.ceil(
            quarter_height * 3 / self.fontSize) + 1

        player_feet_in_screen_x = half_width - self.fontSize / 2
        player_feet_in_screen_y = quarter_height * 3 - self.fontSize / 2

        player_feet_x = int(self.relativePlayer.playerEntity.position.x)
        player_feet_y = int(self.relativePlayer.playerEntity.position.y)

        # Get blocks in the zone
        grid = self.runningSave.get_blocks(
            player_feet_x - player_to_left_blocks, player_feet_x + player_to_right_blocks,
            player_feet_y - player_to_bottom_blocks, player_feet_y + player_to_top_blocks)

        grid = grid[::-1]

        # Rendering block position
        current_time = perf_counter()
        pass_time = current_time - self.runningSave.lastTickTime
        player_x = (self.relativePlayer.playerEntity.position.x +
                    self.relativePlayer.playerEntity.speed.x * pass_time)
        player_y = (self.relativePlayer.playerEntity.position.y +
                    self.relativePlayer.playerEntity.speed.y * pass_time)
        screen_y = player_feet_in_screen_y - self.fontSize * player_to_top_blocks
        screen_x = (player_feet_in_screen_x - self.fontSize * player_to_left_blocks -
                    (player_x - int(player_x)) * self.fontSize)

        for blocks_y in range(len(grid)):
            for blocks_x in range(len(grid[0])):
                self.gameWindow.blit(
                    self.BlockTexture.get_block_texture(grid[blocks_y][blocks_x].blockId).
                    to_surface(), (screen_x, screen_y)
                )
                screen_x += self.fontSize
            screen_x = (player_feet_in_screen_x - self.fontSize * player_to_left_blocks -
                        (player_x - int(player_x)) * self.fontSize)
            screen_y += self.fontSize

        player_texture = self.EntityTexture.get_entity_texture(
            self.relativePlayer.playerEntity.typeId)
        player_texture.blit(self.gameWindow,
                            Vector2(player_feet_in_screen_x, player_feet_in_screen_y))
