from pokemon_types.pokemon_type import *


class Normal(Type):

    def __init__(self):
        super().__init__()
        self._type = NORMAL
        self._types_super_effective = []
        self._types_not_effective = [ROCK, STEEL]
        self._types_no_effect = [GHOST]
