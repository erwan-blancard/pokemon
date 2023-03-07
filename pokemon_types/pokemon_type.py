import pygame

NORMAL = 0
FIGHT = 1
FLYING = 2
POISON = 3
GROUND = 4
ROCK = 5
BUG = 6
GHOST = 7
STEEL = 8
FAIRY = 9
FIRE = 10
WATER = 11
GRASS = 12
ELECTR = 13
PSY = 14
ICE = 15
DRAGON = 16
DARK = 17

TYPES_ATLAS = pygame.image.load("res/types.png")


class Type:

    def __init__(self):
        self._name = "???"
        self._type = -1
        self._types_super_effective = []
        self._types_not_effective = []
        self._types_no_effect = []

    def get_type(self):
        return self._type

    def get_type_image(self):
        return self._get_image()

    def get_attack_multiplier(self, types_opponent: tuple[int, int]):
        multiplier = 1.0
        for type_opp in types_opponent:
            if type_opp in self._types_no_effect:
                multiplier *= 0
            elif type_opp in self._types_super_effective:
                multiplier *= 2.0
            elif type_opp in self._types_not_effective:
                multiplier += 0.5

        return multiplier

    def _get_image(self):
        surf = pygame.Surface((32, 16), pygame.SRCALPHA)
        if 0 <= self._type <= 17:
            surf.blit(TYPES_ATLAS, ((self._type % 4) * -32, (self._type // 4) * -16))
        elif self._type > 17:
            surf.blit(TYPES_ATLAS, ((18 % 4) * -32, (18 // 4) * -16))
        return surf
