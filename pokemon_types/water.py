from pokemon_types.pokemon_type import *


class Water(Type):

    def __init__(self):
        super().__init__()
        self._name = "water"
        self._type = WATER
        self._types_super_effective = [FIRE, GROUND, ROCK]
        self._types_not_effective = [WATER, GRASS, DRAGON]
        self._types_no_effect = []
