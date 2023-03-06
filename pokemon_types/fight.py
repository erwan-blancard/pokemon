from pokemon_types.pokemon_type import *


class Fight(Type):

    def __init__(self):
        super().__init__()
        self._type = FIGHT
        self._types_super_effective = [NORMAL, ICE, ROCK, DARK, STEEL]
        self._types_not_effective = [POISON, FLYING, PSY, BUG, FAIRY]
        self._types_no_effect = [GHOST]
