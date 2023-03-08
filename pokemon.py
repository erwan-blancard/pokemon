import json

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


def get_attack_by_type_and_name(name, att_type_id: int):
    att_type: Type = get_type_by_id(att_type_id)
    try:
        file = open("pokemon_attacks/"+att_type.get_name()+".json")
        json_dict = json.load(file)
        file.close()
        for attack in json_dict:
            if attack["name"] == name:
                return Attack(attack["name"], attack["desc"], get_type_by_id(att_type.get_type()), attack["attack_strength"], attack["success_rate"])
    except Exception as e:
        print(e)
    return Attack("???", "???", Invalid(), 0, 0)


class Pokemon:

    def __init__(self, name: str, strength: int, level: int, hp=100, defense=0,
                 types: tuple[int, int] = (NORMAL, -1),
                 type_attacks: tuple[int, int] = (-1, -1),
                 attacks: tuple[str, str] = ("invalid", "invalid")):

        self.__name = name
        self.__strength = strength
        self.__level = level
        self.__hp = hp
        self.__defense = defense
        self.__types = (get_type_by_id(types[0]), get_type_by_id(types[1]))
        self.__attacks = (get_attack_by_type_and_name(attacks[0], type_attacks[0]),
                          get_attack_by_type_and_name(attacks[1], type_attacks[1]))

    def print_infos(self):
        print("Name:", self.__name, "\nStrength:", self.__strength, "\nLevel:", self.__level, "\nHP:", self.__hp,
              "\nDefense:", self.__defense, "\nTypes:", self.__types[0].get_name(), self.__types[1].get_name(),
              "\nAttacks:", self.__attacks[0].get_name(), self.__attacks[1].get_name())

    def get_name(self):
        return self.__name

    def get_strength(self):
        return self.__strength

    def get_level(self):
        return self.__level

    def get_hp(self):
        return self.__hp

    def get_defense(self):
        return self.__defense

    def get_types(self):
        return self.__types

    def get_attacks(self):
        return self.__attacks

    def get_attack_damage(self, attack_index: int, types_opponent: tuple[int, int]):
        if 0 <= attack_index < len(self.__attacks):
            return self.__attacks[attack_index].get_attack_damage(self.__strength, types_opponent)
        else:
            return self.__attacks[0].get_attack_damage(self.__strength, types_opponent)

    def damage(self, amount):
        damage = amount - self.__defense
        if damage < 1:
            damage = 1
        if self.__hp - damage < 0:
            self.__hp = 0
        else:
            self.__hp -= damage

    def __get_pokemon_image(self, path: str):
        try:
            return pygame.image.load(path.format(self.__name.lower()))
        except Exception as e:
            print(e)
        return pygame.image.load(path.format("INVALID"))

    def get_image_icon(self):
        return self.__get_pokemon_image("res/pokemons/{}_icon.png")

    def get_image_back(self):
        return self.__get_pokemon_image("res/pokemons/{}_back.png")

    def get_image_front(self):
        return self.__get_pokemon_image("res/pokemons/{}_front.png")


# stores pokémons
POKEMONS: list[Pokemon] = []


def get_pokemon_by_name(name: str):
    for pkmn in POKEMONS:
        if pkmn.get_name() == name:
            return pkmn
    return None

