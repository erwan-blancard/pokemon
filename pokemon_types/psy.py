from pokemon_types.pokemon_type import *


class Psy(Type):

    def __init__(self):
        super().__init__()
        self._name = "psy"
        self._type = PSY
        self._types_super_effective = [FIGHT, POISON]
        self._types_not_effective = [PSY, STEEL]
        self._types_no_effect = [DARK]
