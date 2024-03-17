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

        def __init__(self, character: str, color: Tuple[int], font="Simsun", font_size=60):
            self.character = character
            self.color = color
            self.font = self.pygame.font.SysFont(font, font_size)

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
                                    return cls(*blocks_texture_dict[identifier.path])
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

        def to_surface(self):
            """
            Convert to a pygame.Surface object
            """
            return self.font.render(self.character, True, self.color)

    def __init__(self, game_window: pygame.Surface, running_save: World):
        from util import Position
        self.gameWindow = game_window
        self.runningSave = running_save
        self.relativePlayer = self.Player()
        self.relativePlayer.playerEntity.position = Position(0, 3)

    def frame(self):
        import math
        from util import Debug

        # Calculate grid size required
        width, height = self.gameWindow.get_size()
        half_width = (width - self.fontSize) / 2
        quarter_height = (height - self.fontSize) / 4

        player_to_left_blocks = math.ceil(half_width / self.fontSize) + 1
        player_to_right_blocks = math.ceil(half_width / self.fontSize) + 1
        player_to_bottom_blocks = math.ceil(quarter_height / self.fontSize) + 1
        player_to_top_blocks = math.ceil(quarter_height * 3 / self.fontSize) + 1

        player_feet_in_screen_x = half_width - self.fontSize / 2
        player_feet_in_screen_y = quarter_height * 3 - self.fontSize / 2

        player_feet_x = int(self.relativePlayer.playerEntity.position.x)
        player_feet_y = int(self.relativePlayer.playerEntity.position.y)

        # Get blocks in the zone
        grid = self.runningSave.get_blocks(
            player_feet_x - player_to_left_blocks, player_feet_x + player_to_right_blocks,
            player_feet_y - player_to_bottom_blocks, player_feet_y + player_to_top_blocks)
        # Debug.Log.info(str((
        #     player_feet_x - player_to_left_blocks, player_feet_x + player_to_right_blocks,
        #     player_feet_y - player_to_bottom_blocks, player_feet_y + player_to_top_blocks)))
        grid = grid[::-1]

        # Rendering block position
        screen_y = player_feet_in_screen_y - self.fontSize * player_to_top_blocks
        screen_x = player_feet_in_screen_x - self.fontSize * player_to_left_blocks

        for blocks_y in range(len(grid)):
            for blocks_x in range(len(grid[0])):
                self.gameWindow.blit(
                    self.BlockTexture.get_block_texture(grid[blocks_y][blocks_x].blockId).
                    to_surface(), (screen_x, screen_y)
                )
                screen_x += self.fontSize
            screen_x = player_feet_in_screen_x - self.fontSize * player_to_left_blocks
            screen_y += self.fontSize
