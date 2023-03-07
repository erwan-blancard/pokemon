from pokemon_types.pokemon_type import *


class Poison(Type):

    def __init__(self):
        super().__init__()
        self._name = "poison"
        self._type = POISON
        self._types_super_effective = [GRASS, FAIRY]
        self._types_not_effective = [POISON, GROUND, ROCK, GHOST]
        self._types_no_effect = [STEEL]
