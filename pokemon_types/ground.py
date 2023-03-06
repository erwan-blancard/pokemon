from pokemon_types.pokemon_type import *


class Ground(Type):

    def __init__(self):
        super().__init__()
        self._type = GROUND
        self._types_super_effective = [FIRE, ELECTR, POISON, ROCK, STEEL]
        self._types_not_effective = [GRASS, BUG]
        self._types_no_effect = [FLYING]
