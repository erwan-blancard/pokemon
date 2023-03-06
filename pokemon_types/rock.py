from pokemon_types.pokemon_type import *


class Rock(Type):

    def __init__(self):
        super().__init__()
        self._type = ROCK
        self._types_super_effective = [FIRE, ICE, FLYING, BUG]
        self._types_not_effective = [FIGHT, GROUND, STEEL]
        self._types_no_effect = []
