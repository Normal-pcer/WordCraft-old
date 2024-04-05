class GameRenderer:
    """
    wordcraft.client.GameRenderer
    Rendering world-agnostic interfaces (such as GUIs)
    """

    from world import World
    from client import WorldRenderer
    from entity import Player
    import pygame

    runningSave: World
    gameWindow: pygame.Surface
    worldRender: WorldRenderer

    fpsLimit: int = 60
    lastFrameTime: float = 0

    class Response:
        from enum import Enum

        class ResponseType(Enum):
            nothing = 0
            quit = 1

        type: ResponseType
        arguments: dict

        def __init__(self, response_type: ResponseType, args):
            self.type = response_type
            self.arguments = args

    def __init__(self, running_save: World, game_window: pygame.Surface, player: Player):
        self.runningSave = running_save
        self.gameWindow = game_window
        self.worldRender = self.WorldRenderer(game_window, running_save, player)

    def frame(self):
        from time import perf_counter
        self.gameWindow.fill((255, 255, 255))
        self.worldRender.frame()
        self.pygame.time.Clock().tick(self.fpsLimit)

        # Keyboard
        for event in self.pygame.event.get():
            if event.type == self.pygame.QUIT:
                return self.Response(self.Response.ResponseType.quit, {})
            if event.type == self.pygame.VIDEORESIZE:
                self.gameWindow = self.pygame.display.set_mode(event.size, self.pygame.RESIZABLE)
                self.worldRender.gameWindow = self.gameWindow
        pressed = self.pygame.key.get_pressed()
        if pressed[self.pygame.K_a]:
            self.worldRender.relativePlayer.playerEntity.speed.x = -5.0
        elif pressed[self.pygame.K_d]:
            self.worldRender.relativePlayer.playerEntity.speed.x = 5.0
        elif pressed[self.pygame.K_SPACE]:
            if self.runningSave.entity_on_solid(self.worldRender.relativePlayer.playerEntity):
                self.worldRender.relativePlayer.playerEntity.speed.y = 5.0

        # Data
        current_time = perf_counter()
        fps_string = "FPS: " + "{:.1f}".format(1/(current_time-self.lastFrameTime))
        font = self.pygame.font.SysFont("Microsoft YaHei", 18)
        self.gameWindow.blit(font.render(fps_string, True, (0, 0, 0)), (0, 0))

        self.lastFrameTime = current_time
        self.pygame.display.update()
        return self.Response(self.Response.ResponseType.nothing, {})
