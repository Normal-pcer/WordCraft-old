class Identifier:
    """
    wordcraft.util.Identifier
    """

    namespace: str
    path: str

    def __init__(self, namespace: str, path: str):
        self.namespace = namespace
        self.path = path

    def __str__(self):
        return self.namespace + ":" + self.path

    def __repr__(self):
        return self.namespace + ":" + self.path

    def serialize(self):
        return self.namespace + ":" + self.path

    @classmethod
    def deserialize(cls, string: str):
        split_index = string.index(":")
        namespace = string[:split_index]
        path = string[split_index + 1:]
        return cls(namespace, path)
