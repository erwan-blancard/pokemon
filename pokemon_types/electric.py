from pokemon_types.pokemon_type import *


class Electric(Type):

    def __init__(self):
        super().__init__()
        self._name = "electric"
        self._type = ELECTR
        self._types_super_effective = [WATER, FLYING]
        self._types_not_effective = [ELECTR, GRASS, DRAGON]
        self._types_no_effect = [GROUND]
