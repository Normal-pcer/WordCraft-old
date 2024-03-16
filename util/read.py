class Read:
    @staticmethod
    def read_str(filename: str, default=lambda e: "", encoding="UTF-8"):
        try:
            with open(filename, "r", encoding=encoding) as file:
                return file.read()
        except Exception as e:
            return default(e)
