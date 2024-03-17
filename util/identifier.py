class Identifier:
    """
    wordcraft.util.Identifier
    """

    namespace: str
    path: str

    def __init__(self, namespace, path):
        self.namespace = namespace
        self.path = path

    def __str__(self):
        return self.namespace + ":" + self.path

    def __repr__(self):
        return self.namespace + ":" + self.path

    def serialize(self):
        return self.namespace + ":" + self.path
