from pokemon_types.pokemon_type import *
from pokemon_types.normal import Normal
from pokemon_types.fight import Fight
from pokemon_types.fire import Fire
from pokemon_types.ice import Ice
from pokemon_types.water import Water
from pokemon_types.bug import Bug
from pokemon_types.dark import Dark
from pokemon_types.dragon import Dragon
from pokemon_types.electric import Electric
from pokemon_types.steel import Steel
from pokemon_types.ghost import Ghost
from pokemon_types.fairy import Fairy
from pokemon_types.flying import Flying
from pokemon_types.grass import Grass
from pokemon_types.ground import Ground
from pokemon_types.rock import Rock
from pokemon_types.psy import Psy
from pokemon_types.poison import Poison
from pokemon_types.invalid_type import Invalid

from pokemon_attacks.attack import *


# stores pokémons
POKEMONS = []


def get_type_by_id(ID):
    if ID == NORMAL:
        return Normal()
    elif ID == FIRE:
        return Fire()
    elif ID == WATER:
        return Water()
    elif ID == ICE:
        return Ice()
    elif ID == BUG:
        return Bug()
    elif ID == DRAGON:
        return Dragon()
    elif ID == DARK:
        return Dark()
    elif ID == ELECTR:
        return Electric()
    elif ID == FAIRY:
        return Fairy()
    elif ID == FIGHT:
        return Fight()
    elif ID == FLYING:
        return Flying()
    elif ID == GHOST:
        return Ghost()
    elif ID == GRASS:
        return Grass()
    elif ID == GROUND:
        return Ground()
    elif ID == POISON:
        return Poison()
    elif ID == PSY:
        return Psy()
    elif ID == ROCK:
        return Rock()
    elif ID == STEEL:
        return Steel()
    elif ID > 17:
        return Invalid()
    return Type()


def get_attack_by_type_and_name(name, att_type: Type):

    return Attack("???", "???", Invalid(), 0, 0)


class Pokemon:

    def __init__(self, name, strenght, level, hp=100, defense=0,
                 types: tuple[int, int] = (NORMAL, -1),
                 attacks: tuple[str, str] = ("invalid", "invalid")):

        self.__name = name
        self.__strenght = strenght
        self.__level = level
        self.__hp = hp
        self.__defense = defense
        self.__types = (get_type_by_id(types[0]), get_type_by_id(types[1]))
        self.__attacks = (get_attack_by_type_and_name(attacks[0], self.__types[0]), get_attack_by_type_and_name(attacks[1], self.__types[1]))

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

    def get_attack_damage(self, type_index: int, types_opponent: tuple[int, int]):
        if 0 <= type_index < len(self.__types):
            return self.__strenght * self.__types[type_index].get_attack_multiplier(types_opponent)
        else:
            return self.__strenght * self.__types[0].get_attack_multiplier(types_opponent)

    def damage(self, amount):
        damage = amount - self.__defense
        if damage < 1:
            damage = 1
        if self.__hp - damage < 0:
            self.__hp = 0
        else:
            self.__hp -= damage
