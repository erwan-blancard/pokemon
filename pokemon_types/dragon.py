from pokemon_types.pokemon_type import *


class Dragon(Type):

    def __init__(self):
        super().__init__()
        self._type = DRAGON
        self._types_super_effective = [DRAGON]
        self._types_not_effective = [STEEL]
        self._types_no_effect = [FAIRY]
