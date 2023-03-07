from pokemon_types.pokemon_type import *


class Dark(Type):

    def __init__(self):
        super().__init__()
        self._name = "dark"
        self._type = DARK
        self._types_super_effective = [PSY, GHOST]
        self._types_not_effective = [FIGHT, DARK, FAIRY]
        self._types_no_effect = []
