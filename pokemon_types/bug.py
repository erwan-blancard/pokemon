from pokemon_types.pokemon_type import *


class Bug(Type):

    def __init__(self):
        super().__init__()
        self._name = "bug"
        self._type = BUG
        self._types_super_effective = [GRASS, PSY, DARK]
        self._types_not_effective = [FIRE, FIGHT, POISON, FLYING, GHOST, STEEL, FAIRY]
        self._types_no_effect = []
