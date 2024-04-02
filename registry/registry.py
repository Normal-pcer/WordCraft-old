from typing import Tuple, Dict

from registry.registries import Registries
from util import Identifier

storage: Dict[str, Tuple[Registries, any]] = dict()


class Registry:
    @staticmethod
    def register(reg_id: Identifier, reg_type: Registries, reg_item: any):
        storage[str(reg_id)] = (reg_type, reg_item)
