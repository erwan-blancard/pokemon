import random

from pokemon_types.pokemon_type import Type


class Attack:

    def __init__(self, name: str, desc: str, att_type: Type, attack_strenght: float, success_rate=1.0):
        self.__name = name
        self.__desc = desc
        self.__att_type = att_type
        self.__attack_strenght = attack_strenght
        self.__success_rate = success_rate

    def get_attack_damage(self, pkmn_strenght: int, types_opponent: tuple[int, int]):
        if self.__success_rate >= 1.0:
            return (self.__attack_strenght * pkmn_strenght) * self.__att_type.get_attack_multiplier(types_opponent)
        else:
            r = random.random()
            if r > self.__success_rate:
                return -1
            else:
                return (self.__attack_strenght * pkmn_strenght) * self.__att_type.get_attack_multiplier(types_opponent)
