import os.path
import sys

import pygame

import pokedex
import pokemon
import pokemon_parser
from game_state import *
from pokemon_maker.sub_menu import SubMenu
from pokemon_maker.sub_menu_attacks import SubMenuAttacks
from pokemon_maker.sub_menu_images import SubMenuImages
from pokemon_maker.sub_menu_types import SubMenuTypes
from pokemon_types.pokemon_type import *
from pokemon import *
from ui.text_box import TextBox

NAME = 0
IMGS = 1
HP = 2
STRENGTH = 3
DEFENSE = 4
ATTACKS = 5
TYPES = 6

# check codes
CHECK_PASSED = -1
NAME_TOO_SHORT = 0
NAME_ALREADY_EXISTS = 1
INVALID_HEALTH = 2
HEALTH_TOO_SMALL = 3
HEALTH_TOO_HIGH = 4
INVALID_STRENGTH = 5
INVALID_DEFENSE = 6
TYPE_FIRST_NONE = 7
ATTACK_FIRST_INVALID = 8


class PokemonMakerState(GameState):

    def __init__(self):
        super().__init__()
        self.__pkmn_name = ""
        self.__pkmn_hp = 35
        self.__pkmn_strength = 15
        self.__pkmn_defense = 0

        self.__pkmn_types = [0, -1]

        self.__pkmn_attack_types = [0, 0]
        self.__pkmn_attacks = ["---", "---"]

        self.__pkmn_img_icon_path = ""
        self.__pkmn_img_front_path = ""
        self.__pkmn_img_back_path = ""

        self.__pkmn_img_icon_cached = pygame.image.load("res/pokemons/INVALID_icon.png")
        self.__pkmn_img_front_cached = pygame.image.load("res/pokemons/INVALID_front.png")
        self.__pkmn_img_back_cached = pygame.image.load("res/pokemons/INVALID_back.png")

        self.__sub_menu: SubMenu = None
        self.__current_value_ID = 0

        self.buttons = [
            [
                ButtonLabel("", 72, 14-9, 56, 18, lambda: self.__set_sub_menu(self.__pkmn_name, "Changer le nom:", NAME)),
                ButtonLabel("", 24, 28, 96, 96, lambda: self.__set_image_menu()),
                ButtonLabel("", 24, 128, 96, 18, lambda: self.__set_types_menu()),
                ButtonLabel("", 8, 156, 128, 20, lambda: self.__set_sub_menu(self.__pkmn_hp, "Changer les PV:", HP)),
                ButtonLabel("", 8, 176, 128, 20, lambda: self.__set_sub_menu(self.__pkmn_strength, "Changer la puissance:", STRENGTH)),
                ButtonLabel("", 8, 196, 128, 20, lambda: self.__set_sub_menu(self.__pkmn_defense, "Changer la défense:", DEFENSE)),
                ButtonLabel("Créer", 8, 216, 128, 20, lambda: self.__create_pokemon(), font=pygame.font.Font("res/pkmndpb.ttf", 18))
            ],
            [
                ButtonLabel("", 162, 40, 222, 184, lambda: self.__set_attack_menu(ATTACKS))
            ]
        ]
        self.__right_buttons = False

        self.__warning_text = ""

    def __create_pokemon(self):
        if (r := self.__can_create_pokemon()) != CHECK_PASSED:
            if r == NAME_TOO_SHORT:
                self.__warning_text = "Nom trop court !"
            elif r == NAME_ALREADY_EXISTS:
                self.__warning_text = "Un Pokémon du même NOM existe déjà !"
            elif r == INVALID_HEALTH:
                self.__warning_text = "La valeur des PV est invalide !"
            elif r == HEALTH_TOO_SMALL:
                self.__warning_text = "Les PV sont trops petits !"
            elif r == HEALTH_TOO_HIGH:
                self.__warning_text = "Les PV sont trop élevés !"
            elif r == INVALID_STRENGTH:
                self.__warning_text = "La valeur de la PUISSANCE est invalide !"
            elif r == INVALID_DEFENSE:
                self.__warning_text = "La valeur de la DÉFENSE est invalide !"
            elif r == TYPE_FIRST_NONE:
                self.__warning_text = "Le premier TYPE du Pokémon n'est pas défini !"
            elif r == ATTACK_FIRST_INVALID:
                self.__warning_text = "La première ATTAQUE n'existe pas !"
        else:
            if pokemon_parser.add_pokemon(
                name=self.__pkmn_name, strength=self.__pkmn_strength, hp=self.__pkmn_hp, defense=self.__pkmn_defense,
                type_ID_1=self.__pkmn_types[0], type_ID_2=self.__pkmn_types[1],
                attack_type_1=self.__pkmn_attack_types[0], attack_name_1=self.__pkmn_attacks[0],
                attack_type_2=self.__pkmn_attack_types[1], attack_name_2=self.__pkmn_attacks[1]
            ):
                POKEMONS.append(Pokemon(
                    name=self.__pkmn_name, strength=self.__pkmn_strength, hp=self.__pkmn_hp, defense=self.__pkmn_defense,
                    types=(self.__pkmn_types[0], self.__pkmn_types[1]), type_attacks=(self.__pkmn_attack_types[0], self.__pkmn_attack_types[1]),
                    attacks=(self.__pkmn_attacks[0], self.__pkmn_attacks[1]), level=1
                ))
                pokemon_parser.add_to_pokedex(self.__pkmn_name)
                self.__create_images()
                set_state(MENU)
            else:
                self.__warning_text = "Le Pokémon n'a pas pu être ajouté à pokemon.json !"

    def __can_create_pokemon(self):
        """Can return:
        CHECK_PASSED = -1
        NAME_TOO_SHORT = 0
        NAME_ALREADY_EXISTS = 1
        INVALID_HEALTH = 2
        HEALTH_TOO_SMALL = 3
        HEALTH_TOO_HIGH = 4
        INVALID_STRENGTH = 5
        INVALID_DEFENSE = 6
        TYPE_FIRST_NONE = 7
        ATTACK_FIRST_INVALID = 8"""
        # check name
        if len(self.__pkmn_name) <= 2:
            return NAME_TOO_SHORT

        if pokemon_parser.pokemon_exists(self.__pkmn_name):
            return NAME_ALREADY_EXISTS

        # check hp
        try: int(self.__pkmn_hp)
        except: return INVALID_HEALTH

        if int(self.__pkmn_hp) <= 0:
            return HEALTH_TOO_SMALL
        if int(self.__pkmn_hp) > 999:
            return HEALTH_TOO_HIGH

        # check strength
        try: int(self.__pkmn_strength)
        except: return INVALID_STRENGTH

        if int(self.__pkmn_strength) <= 0:
            return INVALID_STRENGTH

        # check defense
        try: int(self.__pkmn_defense)
        except: return INVALID_DEFENSE

        # check types
        if self.__pkmn_types[0] == -1:
            return TYPE_FIRST_NONE
        if not pokemon_parser.attack_exists(self.__pkmn_attacks[0], self.__pkmn_attack_types[0]):
            return ATTACK_FIRST_INVALID

        return CHECK_PASSED

    def __create_images(self):
        paths = [self.__pkmn_img_icon_path, self.__pkmn_img_front_path, self.__pkmn_img_back_path]
        i = 0
        while i < len(paths):
            if os.path.exists(paths[i]):
                try:
                    img = pygame.image.load(paths[i])
                    if i == 0:
                        img = pygame.transform.scale(img, (48, 48))
                        pygame.image.save(img, "res/pokemons/"+self.__pkmn_name.lower()+"_icon.png")
                    elif i == 1:
                        img = pygame.transform.scale(img, (96, 96))
                        pygame.image.save(img, "res/pokemons/" + self.__pkmn_name.lower() + "_front.png")
                    elif i == 2:
                        img = pygame.transform.scale(img, (96, 96))
                        pygame.image.save(img, "res/pokemons/" + self.__pkmn_name.lower() + "_back.png")
                except Exception as e:
                    print("Error saving images from n°", i, ":", e)
            i += 1

    def __set_sub_menu(self, value, title, value_ID):
        self.__current_value_ID = value_ID
        self.__sub_menu = SubMenu(value, title)

    def __set_types_menu(self):
        self.__current_value_ID = TYPES
        self.__sub_menu = SubMenuTypes(self.__pkmn_types)

    def __set_image_menu(self):
        self.__current_value_ID = IMGS
        self.__sub_menu = SubMenuImages([self.__pkmn_img_icon_path, self.__pkmn_img_front_path, self.__pkmn_img_back_path])

    def __set_attack_menu(self, value_ID):
        self.__current_value_ID = value_ID
        self.__sub_menu = SubMenuAttacks(self.__pkmn_attack_types, self.__pkmn_attacks)

    def __reload_images(self):
        try:
            self.__pkmn_img_icon_cached = pygame.transform.scale(pygame.image.load(self.__pkmn_img_icon_path), (48, 48))
        except: pass
        try:
            self.__pkmn_img_front_cached = pygame.transform.scale(pygame.image.load(self.__pkmn_img_front_path), (96, 96))
        except: pass
        try:
            self.__pkmn_img_back_cached = pygame.transform.scale(pygame.image.load(self.__pkmn_img_back_path), (96, 96))
        except: pass

    def update(self):
        super().update()
        if self.__sub_menu is not None:
            if self.__sub_menu.has_validated():
                if self.__current_value_ID == NAME:
                    self.__pkmn_name = self.__sub_menu.get_value()
                elif self.__current_value_ID == IMGS:
                    if type(self.__sub_menu) == SubMenuImages:
                        self.__pkmn_img_icon_path = self.__sub_menu.get_value()[0]
                        self.__pkmn_img_front_path = self.__sub_menu.get_value()[1]
                        self.__pkmn_img_back_path = self.__sub_menu.get_value()[2]
                        self.__reload_images()
                elif self.__current_value_ID == HP:
                    try:
                        self.__pkmn_hp = int(self.__sub_menu.get_value())
                    except Exception as e:
                        print(e)
                elif self.__current_value_ID == STRENGTH:
                    try:
                        self.__pkmn_strength = int(self.__sub_menu.get_value())
                    except Exception as e:
                        print(e)
                elif self.__current_value_ID == DEFENSE:
                    try:
                        self.__pkmn_defense = int(self.__sub_menu.get_value())
                    except Exception as e:
                        print(e)
                elif self.__current_value_ID == ATTACKS:
                    print(self.__sub_menu.get_value())
                self.__sub_menu = None

    def render(self, screen: pygame.Surface):
        screen.blit(pokedex.FRAME, (0, 0))
        name = self.__pkmn_name
        if len(name) == 0:
            name = "<Nom>"
        text.draw_centered_text(name, 72, 14, screen, pygame.font.Font("res/pkmndpb.ttf", 18))
        # stats
        text.draw_centered_text("PV: " + str(self.__pkmn_hp), 8 + 64, 166, screen)
        text.draw_centered_text("Puissance: " + str(self.__pkmn_strength), 8 + 64, 186, screen)
        text.draw_centered_text("Défense: " + str(self.__pkmn_defense), 8 + 64, 206, screen)
        # types
        type_1 = pokemon.get_type_by_id(self.__pkmn_types[0])
        type_2 = pokemon.get_type_by_id(self.__pkmn_types[1])
        if type_1.get_type() != -1:
            screen.blit(type_1.get_type_image(), (24, 124 + 13 - type_1.get_type_image().get_height() / 2))
        else:
            screen.blit(type_1.get_none_image(), (24, 124 + 13 - type_1.get_none_image().get_height() / 2))
        if type_2.get_type() != -1:
             screen.blit(type_2.get_type_image(), (24 + 96 - type_2.get_type_image().get_width(), 124 + 13 - type_2.get_type_image().get_height() / 2))
        else:
            screen.blit(type_2.get_none_image(), (24 + 96 - type_2.get_none_image().get_width(), 124 + 13 - type_2.get_none_image().get_height() / 2))
        # img pokemon
        screen.blit(self.__pkmn_img_front_cached, (24, 28))

        # attacks descs
        text.draw_centered_text("ATTAQUES:", 162 + 111, 6 + 17, screen, pygame.font.Font("res/pkmndpb.ttf", 18))
        pos_offset = 96
        for i in range(len(self.__pkmn_attacks)):
            attack: Attack = pokemon_parser.get_attack_by_type_and_name(self.__pkmn_attacks[i], self.__pkmn_attack_types[i])
            att_img = attack.get_attack_type().get_type_image()
            text.draw_text(attack.get_name(), 172, 42 + i * pos_offset, screen)
            screen.blit(att_img, (300 + 40, 42 + i * pos_offset))
            # desc
            att_desc_box = TextBox(attack.get_desc(), 166, 60 + i * pos_offset, 217, line_limit=3)
            att_desc_box.render(screen)
            # attacks stats
            power = round(attack.get_attack_strength() * 100)
            rate = round(attack.get_success_rate() * 100)
            if power <= 0:
                power = "N/A"
            if rate <= 0:
                rate = "N/A"
            text.draw_text("PUISSANCE : " + str(power), 166, 110 + i * pos_offset, screen)
            text.draw_text("PRECISION : " + str(rate), 166 + 128, 110 + i * pos_offset, screen)

        i = 0
        while i < len(self.buttons[0]):
            self.buttons[0][i].render(screen)
            if not self.__right_buttons and i == self.selected_button:
                self.buttons[0][i].render_cursor(screen, True, 4)
            i += 1
        j = 0
        while j < len(self.buttons[1]):
            self.buttons[1][j].render(screen)
            if self.__right_buttons and j == self.selected_button:
                self.buttons[1][j].render_cursor(screen)
            j += 1

        if len(self.__warning_text) > 0:
            text.draw_aligned_text(self.__warning_text, screen.get_width()/2, 200, screen, pygame.font.Font("res/pkmndpb.ttf", 18), color=(255, 90, 90), shadow_color=(255, 0, 0), shadow_offset=1)

        if self.__sub_menu is not None:
            self.__sub_menu.render(screen)

    def input(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            self.__warning_text = ""
            if self.__sub_menu is not None:
                self.__sub_menu.input(event)
                if event.key == pygame.K_ESCAPE:
                    self.__sub_menu = None
            else:
                if event.key == pygame.K_ESCAPE:
                    set_state(MENU)
                else:
                    button_list = self.buttons[0]
                    if self.__right_buttons:
                        button_list = self.buttons[1]

                    if event.key == pygame.K_RETURN:
                        if 0 <= self.selected_button < len(button_list):
                            button_list[self.selected_button].execute()
                    elif event.key == pygame.K_UP:
                        if self.selected_button - 1 >= 0:
                            self.selected_button -= 1
                        else:
                            self.selected_button = len(button_list) - 1
                    elif event.key == pygame.K_DOWN:
                        if self.selected_button + 1 < len(button_list):
                            self.selected_button += 1
                        else:
                            self.selected_button = 0
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        if self.__right_buttons:
                            self.selected_button = 2
                            self.__right_buttons = False
                        else:
                            self.__right_buttons = True
                            self.selected_button = 0

"""pokemon_parser.add_pokemon("Pikachu", 13, 35, 0, ELECTR, -1, NORMAL, "CHARGE", ELECTR, "ECLAIR")

pokemon_parser.add_pokemon("Bulbizarre", 15, 45, 0, GRASS, POISON, NORMAL, "CHARGE", GRASS, "BALLE GRAINE")
pokemon_parser.add_pokemon("Herbizarre", 18, 60, 3, GRASS, POISON, NORMAL, "CHARGE", GRASS, "FOUET LIANES")
pokemon_parser.add_pokemon("Florizarre", 21, 80, 8, GRASS, POISON, GRASS, "FOUET LIANES", POISON, "GAZ TOXIC")

pokemon_parser.add_pokemon("Salamèche", 14, 39, 0, FIRE, -1, NORMAL, "GRIFFE", FIRE, "FLAMMECHE")
pokemon_parser.add_pokemon("Reptincel", 17, 58, 4, FIRE, -1, NORMAL, "GRIFFE", FIRE, "CROCS FEU")
pokemon_parser.add_pokemon("Dracaufeu", 22, 78, 7, FIRE, FLYING, DRAGON, "DRACOGRIFFE", FIRE, "INCENDIE")

pokemon_parser.add_pokemon("Magicarpe", 8, 20, 2, WATER, -1, NORMAL, "CHARGE", NORMAL, "CHARGE")
pokemon_parser.add_pokemon("Pichu", 11, 24, 0, ELECTR, -1, NORMAL, "CHARGE", ELECTR, "ECLAIR")

pokemon_parser.load_pokemons()

for pkmn in pokemon.POKEMONS:
    pkmn.print_infos()
    print()
"""