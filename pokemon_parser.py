import os
import json

import pokemon
from pokemon import *

FILE_POKEMONS = "pokemon.json"
FILE_POKEDEX = "pokédex.json"

"""
JSON Structure "pokemon.json":
    [
        {
            "name": str,
            "strength": int,
            "hp": int,
            "defense": int,
            "type_ID_1": int,
            "type_ID_2": int,
            "attack_type_1": int,
            "attack_name_1": str,
            "attack_type_2": int,
            "attack_name_2": str
        },
        etc
    ]
JSON Structure "pokédex.json":
    [
        {
            "name": str,
            "count": int
        }
    ]
"""


def create_file(FILE=FILE_POKEMONS):
    try:
        file = open(FILE, "w")
        json.dump([], file, indent=4)
        file.close()
    except IOError as e:
        print(e)


def open_file(FILE=FILE_POKEMONS, access_type="r"):
    if os.path.exists(FILE):
        try:
            return open(FILE, access_type)
        except IOError as e:
            print(e)
            return None
    else:
        create_file()


def get_JSON(file):
    try:
        return json.load(file)
    except Exception as e:
        print(e)
        return list()


def write_to_file(json_dict: dict, FILE=FILE_POKEMONS):
    over_file = open_file(FILE, "w")
    json.dump(json_dict, over_file, indent=4)
    over_file.close()


def load_pokemons():
    file = open_file()
    if file is not None:
        json_dict = get_JSON(file)
        if json_dict is not None:
            if type(json_dict) == list:
                for pkmn in json_dict:
                    try:
                        pkmn_in = Pokemon(name=pkmn["name"],
                                          strength=pkmn["strength"],
                                          level=1, hp=pkmn["hp"],
                                          defense=pkmn["defense"],
                                          types=(pkmn["type_ID_1"], pkmn["type_ID_2"]),
                                          type_attacks=(pkmn["attack_type_1"], pkmn["attack_type_2"]),
                                          attacks=(pkmn["attack_name_1"], pkmn["attack_name_2"])
                                          )
                        POKEMONS.append(pkmn_in)
                    except Exception as e:
                        print("Cannot create pokemon:", str(e))
    if file is not None:
        file.close()


def pokemon_exists(pokemon_name: str):
    file = open_file()
    if file is not None:
        json_dict = get_JSON(file)
        if json_dict is not None:
            if type(json_dict) == list:
                try:
                    for pkmn in json_dict:
                        if pkmn["name"].lower() == pokemon_name.lower():
                            file.close()
                            return True
                except Exception as e:
                    print("Error in pokemon_exists():", e)
    if file is not None:
        file.close()
    return False


def pokemon_in_pokedex(pokemon_name: str):
    file = open_file(FILE=FILE_POKEDEX)
    if file is not None:
        json_dict = get_JSON(file)
        if json_dict is not None:
            if type(json_dict) == list:
                try:
                    for pkmn in json_dict:
                        if pkmn["name"].lower() == pokemon_name.lower():
                            file.close()
                            return True
                except Exception as e:
                    print("Error in pokemon_in_pokedex():", e)
                    file.close()
                    return False
    if file is not None:
        file.close()
    return False


def get_pokemon_encounter_count(pokemon_name: str):
    file = open_file(FILE=FILE_POKEDEX)
    if file is not None:
        json_dict = get_JSON(file)
        if json_dict is not None:
            if type(json_dict) == list:
                try:
                    for pkmn in json_dict:
                        if pkmn["name"].lower() == pokemon_name.lower():
                            file.close()
                            return pkmn["count"]
                except Exception as e:
                    print("Error in pokemon_in_pokedex():", e)
                    file.close()
                    return -1
    if file is not None:
        file.close()
    return -1


# returns False if the pokémon couldn't be added and True if it was added to "pokemon.json"
def add_pokemon(name: str, strength: int, hp: int, defense: int, type_ID_1: int, type_ID_2: int, attack_type_1: int, attack_name_1: str, attack_type_2: int, attack_name_2: str):
    file = open_file()
    json_dict = get_JSON(file)
    if file is not None:
        file.close()
    if type(json_dict) == list:
        if not pokemon_exists(name):
            try:
                json_dict.append(
                    {"name": name,
                     "strength": strength,
                     "hp": hp,
                     "defense": defense,
                     "type_ID_1": type_ID_1,
                     "type_ID_2": type_ID_2,
                     "attack_type_1": attack_type_1,
                     "attack_name_1": attack_name_1,
                     "attack_type_2": attack_type_2,
                     "attack_name_2": attack_name_2}
                )
                write_to_file(json_dict)
                return True
            except:
                return False
        else:
            return False
    else:
        return False


# returns False if the pokémon couldn't be added and True if it was added to "pokédex.json"
def add_to_pokedex(name: str):
    file = open_file(FILE=FILE_POKEDEX)
    json_dict = get_JSON(file)
    if file is not None:
        file.close()
    if type(json_dict) == list:
        if pokemon_exists(name):
            if pokemon_in_pokedex(name):
                try:
                    for pkmn in json_dict:
                        if pkmn["name"] == name:
                            pkmn["count"] = pkmn["count"] + 1
                            write_to_file(json_dict, FILE=FILE_POKEDEX)
                            return True
                except Exception as e:
                    print("Could not increase count of pokémon in pokédex:", e)
                    return False
            else:
                try:
                    json_dict.append({"name": name, "count": 1})
                    write_to_file(json_dict, FILE=FILE_POKEDEX)
                    return True
                except Exception as e:
                    print("Could not add pokémon to pokédex:", e)
                    return False
        else:
            print("Pokémon doesn't exists:", name)
            return False
    else:
        create_file(FILE=FILE_POKEDEX)
        add_to_pokedex(name)
