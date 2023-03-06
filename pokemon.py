from pokemon_types.pokemon_type import *


class Pokemon:

    def __init__(self, name, strenght, level, hp=100, defense=0, types: tuple[int, int] = (NORMAL, -1)):

        self.__name = name
        self.__strenght = strenght
        self.__level = level
        self.__hp = hp
        self.__defense = defense
        self.__types = types

    def get_name(self):
        return self.__name

    def get_strength(self):
        return self.__strenght

    def get_level(self):
        return self.__level

    def get_hp(self):
        return self.__hp

    def get_defense(self):
        return self.__defense

    def get_types(self):
        return self.__types
