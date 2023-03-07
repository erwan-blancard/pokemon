from pokemon_types.pokemon_type import *


class Ghost(Type):

    def __init__(self):
        super().__init__()
        self._name = "ghost"
        self._type = GHOST
        self._types_super_effective = [PSY, GHOST]
        self._types_not_effective = [DARK]
        self._types_no_effect = [NORMAL]
