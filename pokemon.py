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

MAX_LEVEL = 99

# added stats values per level
HP_BONUS_LEVEL = 1.3
STRENGTH_BONUS_LEVEL = 0.5
DEFENSE_BONUS_LEVEL = 0.3


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
        if type(att_type) != Type and type(att_type) != Invalid:
            file = open("pokemon_attacks/"+att_type.get_name()+".json")
            json_dict = json.load(file)
            file.close()
            for attack in json_dict:
                if attack["name"] == name:
                    return Attack(attack["name"], attack["desc"], get_type_by_id(att_type.get_type()), attack["attack_strength"], attack["success_rate"])
        elif type(att_type) == Invalid:
            return Attack("???", "???", Invalid(), 0, 0)
    except Exception as e:
        print(e)
    return Attack("---", "---", Type(), -1, -1)


def attack_exists(name, att_type_id: int):
    att_type: Type = get_type_by_id(att_type_id)
    try:
        if type(att_type) != Type and type(att_type) != Invalid:
            file = open("pokemon_attacks/"+att_type.get_name()+".json")
            json_dict = json.load(file)
            file.close()
            for attack in json_dict:
                if attack["name"] == name:
                    test_attack = Attack(attack["name"], attack["desc"], get_type_by_id(att_type.get_type()), attack["attack_strength"], attack["success_rate"])
                    return True
        else:
            return False
    except Exception as e:
        print(e)
    return False


class Pokemon:

    def __init__(self, name: str, strength: int, level: int, hp=100, defense=0,
                 types: tuple[int, int] = (NORMAL, -1),
                 type_attacks: tuple[int, int] = (-1, -1),
                 attacks: tuple[str, str] = ("invalid", "invalid"),
                 evolution: str = "", evolution_level: int = 0):

        self.__name = name
        self.__strength = strength
        self.__level = level
        self.__hp = hp
        self.__current_hp = hp + self.__get_level_bonus_amount(HP_BONUS_LEVEL)
        self.__defense = defense
        self.__types = (get_type_by_id(types[0]), get_type_by_id(types[1]))
        self.__attacks = (get_attack_by_type_and_name(attacks[0], type_attacks[0]),
                          get_attack_by_type_and_name(attacks[1], type_attacks[1]))
        self.__evolution = evolution
        self.__evolution_level = evolution_level

    def print_infos(self):
        print("Name:", self.__name, "\nBase Strength:", self.__strength, "\nLevel:", self.__level, "\nBase HP:", self.__hp,
              "\nBase Defense:", self.__defense, "\nTypes:", self.__types[0].get_name(), self.__types[1].get_name(),
              "\nAttacks:", self.__attacks[0].get_name(), self.__attacks[1].get_name())

    def get_name(self):
        return self.__name

    def get_base_strength(self):
        return self.__strength

    def get_strength(self):
        return self.__strength + self.__get_level_bonus_amount(STRENGTH_BONUS_LEVEL)

    def get_level(self):
        return self.__level

    def add_level(self):
        """
        Adds 1 level to the Pokémon.
        Returns False if adding a level makes it go past the MAX_LEVEL, and True if the level was added.
        """
        if self.__level + 1 > MAX_LEVEL:
            return False
        else:
            self.__level += 1
            self.__current_hp = self.get_hp()
            return True

    def set_level(self, level):
        """
        Sets the level of the Pokémon.
        Returns False if the level is greater than the MAX_LEVEL, and True if the level was set.
        """
        if level > MAX_LEVEL or level < 1:
            return False
        else:
            self.__level = level
            self.__current_hp = self.get_hp()
            return True

    def __get_level_bonus_amount(self, bonus):
        return (self.__level - 1)*round(bonus)

    def can_evolve(self):
        return self.__evolution_level > 0

    def get_evolution_name(self):
        return self.__evolution

    def get_evolution_level(self):
        return self.__evolution_level

    def get_base_hp(self):
        return self.__hp

    def get_hp(self):
        return self.__hp + self.__get_level_bonus_amount(HP_BONUS_LEVEL)

    def get_current_hp(self):
        return self.__current_hp

    def get_base_defense(self):
        return self.__defense

    def get_defense(self):
        return self.__defense + self.__get_level_bonus_amount(DEFENSE_BONUS_LEVEL)

    def get_types(self):
        return self.__types

    def get_types_type(self):
        return self.__types[0].get_type(), self.__types[1].get_type()

    def get_attacks(self):
        return self.__attacks

    def get_attack_damage(self, attack_index: int, types_opponent: tuple[int, int]):
        if 0 <= attack_index < len(self.__attacks):
            return self.__attacks[attack_index].get_attack_damage(self.get_strength(), types_opponent)
        else:
            return self.__attacks[0].get_attack_damage(self.get_strength(), types_opponent)

    def damage(self, amount):
        damage = amount - self.get_defense()
        if damage < 1:
            damage = 1
        if amount <= 0:
            damage = 0
        if self.__current_hp - damage < 0:
            self.__current_hp = 0
        else:
            self.__current_hp -= damage

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

    def copy(self):
        """returns a copy of the Pokémon as a new instance of the Pokemon class."""
        return Pokemon(self.get_name(), self.get_base_strength(), self.get_level(), self.get_base_hp(), self.get_base_defense(),
                       (self.get_types()[0].get_type(), self.get_types()[1].get_type()),
                       (self.get_attacks()[0].get_attack_type().get_type(), self.get_attacks()[1].get_attack_type().get_type()),
                       (self.get_attacks()[0].get_name(), self.get_attacks()[1].get_name()))

    def copy_with_set_level(self, level: int):
        """returns a copy of the Pokémon as a new instance of the Pokemon class."""
        return Pokemon(self.get_name(), self.get_base_strength(), level, self.get_base_hp(), self.get_base_defense(),
                       (self.get_types()[0].get_type(), self.get_types()[1].get_type()),
                       (self.get_attacks()[0].get_attack_type().get_type(), self.get_attacks()[1].get_attack_type().get_type()),
                       (self.get_attacks()[0].get_name(), self.get_attacks()[1].get_name()))


# stores pokémons
POKEMONS: list[Pokemon] = []


def get_pokemon_by_name(name: str):
    for pkmn in POKEMONS:
        if pkmn.get_name() == name:
            return pkmn
    return None
