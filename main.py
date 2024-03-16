class Main:
    @staticmethod
    def main():
        import pygame
        from client import GameRenderer
        from world import World, SaveDir
        from util import Debug

        pygame.init()
        game_window = pygame.display.set_mode((1024, 720), pygame.RESIZABLE)
        running_save = World("New World", SaveDir("saves/New World"))
        game_renderer = GameRenderer(running_save, game_window)
        try:
            Debug.Log.info(str(running_save.get_blocks(-5, 7, -3, 9)))
            while True:
                response = game_renderer.frame()
                if response.type == GameRenderer.Response.ResponseType.quit:
                    break
        except Exception as exception:
            import traceback
            Debug.Log.error("Uncaught Exception: " + repr(exception))
            Debug.Log.error(traceback.format_exc())


if __name__ == '__main__':
    Main.main()
