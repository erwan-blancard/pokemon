from pokemon_types.pokemon_type import *


class Fairy(Type):

    def __init__(self):
        super().__init__()
        self._name = "fairy"
        self._type = FAIRY
        self._types_super_effective = [FIGHT, DRAGON, DARK]
        self._types_not_effective = [FIRE, POISON, STEEL]
        self._types_no_effect = []
