import random

from pokemon_types.pokemon_type import Type


class Attack:

    def __init__(self, name: str, desc: str, att_type: Type, attack_strength: float, success_rate=1.0):
        self.__name = name
        self.__desc = desc
        self.__att_type = att_type
        self.__attack_strength = attack_strength
        self.__success_rate = success_rate

    def get_name(self):
        return self.__name

    def get_desc(self):
        return self.__desc

    def get_attack_type(self):
        return self.__att_type

    def get_attack_strength(self):
        return self.__attack_strength

    def get_success_rate(self):
        return self.__success_rate

    # returns -1 if attack is missed
    def get_attack_damage(self, pkmn_strength: int, types_opponent: tuple[int, int]):
        r = random.random()
        if self.__success_rate >= 1.0 or r <= self.__success_rate:
            return (self.__attack_strength * pkmn_strength) * self.__att_type.get_attack_multiplier(types_opponent)
        else:
            return -1

