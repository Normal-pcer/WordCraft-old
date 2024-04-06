class Main:
    @staticmethod
    def main():
        import pygame
        from client import GameRenderer
        from world import World, SaveDir
        from entity import Player
        from util import Debug, Vector2
        from time import perf_counter

        pygame.init()
        game_window = pygame.display.set_mode((1024, 720), pygame.RESIZABLE)
        running_save = World("New World", SaveDir("saves/New World"))
        local_player = Player()
        game_renderer = GameRenderer(running_save, game_window, local_player)
        game_renderer.lastTenFrameTime = perf_counter()

        pygame.key.stop_text_input()
        local_player.playerEntity.position = Vector2(0, 6)
        running_save.init(local_player)

        try:
            while True:
                running_save.tick()
                response = game_renderer.frame()
                if response.type == GameRenderer.Response.ResponseType.quit:
                    running_save.save_all_chunks()
                    break
        except Exception as exception:
            import traceback
            Debug.Log.error("Uncaught Exception: " + repr(exception))
            Debug.Log.error(traceback.format_exc())


if __name__ == '__main__':
    Main.main()
