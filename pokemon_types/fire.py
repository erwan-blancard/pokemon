from pokemon_types.pokemon_type import *


class Fire(Type):

    def __init__(self):
        super().__init__()
        self._type = FIRE
        self._types_super_effective = [GRASS, ICE, BUG, STEEL]
        self._types_not_effective = [FIRE, WATER, ROCK, DRAGON]
        self._types_no_effect = []
