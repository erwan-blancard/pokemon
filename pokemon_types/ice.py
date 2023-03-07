from pokemon_types.pokemon_type import *


class Ice(Type):

    def __init__(self):
        super().__init__()
        self._name = "ice"
        self._type = ICE
        self._types_super_effective = [GRASS, GROUND, FLYING, DRAGON]
        self._types_not_effective = [FIRE, WATER, ICE, STEEL]
        self._types_no_effect = []
