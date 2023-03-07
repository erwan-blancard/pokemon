from pokemon_types.pokemon_type import *


class Grass(Type):

    def __init__(self):
        super().__init__()
        self._name = "grass"
        self._type = GRASS
        self._types_super_effective = [WATER, GROUND, ROCK]
        self._types_not_effective = [FIRE, GRASS, POISON, FLYING, BUG, DRAGON, STEEL]
        self._types_no_effect = []
