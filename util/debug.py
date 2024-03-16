class Debug:
    """
    wordcraft.util.Debug
    """
    class Log:
        """
        wordcraft.util.Debug.Log
        """
        
        @staticmethod
        def info(message: str):
            import time
            log_file = open("log.txt", "a", encoding="UTF-8")
            print("[INFO]", message)
            log_file.write("[INFO at {}] {}\n".format(time.time(), message))
            log_file.close()

        @staticmethod
        def warning(message: str):
            import colorama
            import time
            log_file = open("log.txt", "a", encoding="UTF-8")
            print(colorama.Fore.YELLOW, "[Warning]", message, colorama.Style.RESET_ALL)
            log_file.write("[Warning at {}] {}\n".format(time.time(), message))
            log_file.close()

        @staticmethod
        def error(message: str):
            import colorama
            import time
            log_file = open("log.txt", "a", encoding="UTF-8")
            print(colorama.Back.RED, "[Error]", message, colorama.Style.RESET_ALL)
            log_file.write("[Error at {}] {}\n".format(time.time(), message))
            log_file.close()
