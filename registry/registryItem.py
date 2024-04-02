class RegistryItem:
    from registry.registries import Registries

    registryType: Registries
    value: any

    def __init__(self, registry_type: Registries, value):
        self.registryType = registry_type
        self.value = value
