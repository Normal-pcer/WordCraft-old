class Identifier:
    """
    wordcraft.util.Identifier

    标识符
    """

    namespace: str
    path: str

    def __init__(self, namespace, path):
        self.namespace = namespace
        self.path = path