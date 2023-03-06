from pokemon_types.pokemon_type import *


class Flying(Type):

    def __init__(self):
        super().__init__()
        self._type = FLYING
        self._types_super_effective = [GRASS, FIGHT, BUG]
        self._types_not_effective = [ELECTR, ROCK, STEEL]
        self._types_no_effect = []
