from pokemon_types.pokemon_type import *


class Invalid(Type):

    def __init__(self):
        super().__init__()
        self._name = "invalid"
        self._type = 256
        self._types_super_effective = []
        self._types_not_effective = []
        self._types_no_effect = []
