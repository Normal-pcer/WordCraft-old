class SaveDir:
    """
    wordcraft.world.Save.SaveDir

    存档文件夹
    """
    root: str

    def __init__(self, root):
        self.root = root

    def read_file_content(self, file_name: str):
        """
        wordcraft.world.Save.readFileContent(fileName: str)

        读取压缩的文件
        """
        import os
        import zlib
        complete_path = os.path.join(self.root, file_name)

        with open(complete_path, "rb") as f:
            file_content: bytes = zlib.decompress(f.read())
            return file_content


class Save:
    from world.world import World

    """
    wordcraft.world.Save

    存档
    """
    storedWorld: World
    path: SaveDir
    name: str

    def __init__(self, name: str, path: SaveDir):
        self.name = name
        self.path = path
