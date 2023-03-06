from pokemon_types.pokemon_type import *


class Steel(Type):

    def __init__(self):
        super().__init__()
        self._type = STEEL
        self._types_super_effective = [ICE, ROCK, FAIRY]
        self._types_not_effective = [FIRE, WATER, ELECTR, STEEL]
        self._types_no_effect = []
