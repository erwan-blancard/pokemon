import pygame

import pokemon
from pokemon import POKEMONS, Pokemon
import pokemon_parser
from pokemon_attacks.attack import Attack
from ui.button_icon import *
from game_state import *
from ui.text_box import TextBox

BUTTON_BG = pygame.image.load("res/pokédex_button.png")
FRAME = pygame.image.load("res/pokédex_frame.png")
ARROW = pygame.image.load("res/arrow.png")


def colorize(image, newColor):
    image = image.copy()
    # zero out RGB values
    image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
    # add in new RGB values
    image.fill(newColor[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)

    return image


class PokedexState(GameState):

    def __init__(self, quit_state=MENU, title_color=text.DEFAULT_COLOR):
        super().__init__()
        self.quit_state = quit_state
        self.title_color = title_color

        # create blank buttons
        for i in range(4):
            img_label = pygame.Surface((300, 48), pygame.SRCALPHA)
            img_label.blit(BUTTON_BG, (0, 0))
            text.draw_text("---", 56, 16, img_label, text.get_font(16))
            self.buttons.append(ButtonIcon(64, 24 + 8 + (i * 48), 300, 48, img_label))

        self.list_offset = 0
        self.set_pkmn_list_from_offset()
        self.info_pkmn: Pokemon = None
        self.info_pkmn_cached_img: pygame.Surface = None
        self.info_pkmn_cached_count = -1
        self.in_info_menu = False

    def set_pkmn_list_from_offset(self):
        if len(POKEMONS) <= 4:
            self.list_offset = 0
        elif self.list_offset > len(POKEMONS) - 4:
            self.list_offset = len(POKEMONS) - 4
        for i in range(4):
            pkmn_i = i+self.list_offset
            img_label = pygame.Surface((300, 48), pygame.SRCALPHA)
            img_label.blit(BUTTON_BG, (0, 0))
            # if entry (pkmn_i) is a pokémon in POKEMONS
            if pkmn_i < len(POKEMONS):
                pkmn_name = POKEMONS[pkmn_i].get_name()
                # if pokémon was encountered at least once
                if pokemon_parser.pokemon_in_pokedex(pkmn_name) and pokemon_parser.get_pokemon_encounter_count(pkmn_name) > 0:
                    img_label.blit(POKEMONS[pkmn_i].get_image_icon(), (0, 0))
                    # show types
                    if POKEMONS[pkmn_i].get_types()[1].get_type() == -1:
                        img_pkmn_type = POKEMONS[pkmn_i].get_types()[0].get_type_image()
                        img_label.blit(img_pkmn_type, (img_label.get_width() - 10 - img_pkmn_type.get_width(), img_label.get_height()/2 - img_pkmn_type.get_height()/2))
                    else:
                        for j in range(len(POKEMONS[pkmn_i].get_types())):
                            img_pkmn_type = POKEMONS[pkmn_i].get_types()[j].get_type_image()
                            img_label.blit(img_pkmn_type, (img_label.get_width() - 50 - img_pkmn_type.get_width() + j*40, img_label.get_height() / 2 - img_pkmn_type.get_height() / 2))

                    text.draw_text(POKEMONS[pkmn_i].get_name(), 56, 16, img_label, text.get_font(16))
                    self.buttons[i] = ButtonIcon(64, 24 + 8 + (i * 48), 300, 48, img_label,
                                                 lambda name=pkmn_name: self.show_info_menu_for_pokemon(name))
                # if pokémon was not encountered
                else:
                    pkmn_img = POKEMONS[pkmn_i].get_image_icon()
                    pkmn_img = colorize(pkmn_img, (0, 0, 0))
                    img_label.blit(pkmn_img, (0, 0))
                    text.draw_text("???", 56, 16, img_label, text.get_font(16))
                    self.buttons[i] = ButtonIcon(64, 24 + 8 + (i * 48), 300, 48, img_label)

            # else if entry doesn't exist
            else:
                text.draw_text("---", 56, 16, img_label, text.get_font(16))
                self.buttons[i] = ButtonIcon(64, 24 + 8 + (i * 48), 300, 48, img_label)

    def show_info_menu_for_pokemon(self, name: str):
        if pokemon_parser.pokemon_exists(name):
            self.info_pkmn = pokemon.get_pokemon_by_name(name)
            if self.info_pkmn is not None:
                self.info_pkmn_cached_img = self.info_pkmn.get_image_front()
                self.in_info_menu = True
                self.info_pkmn_cached_count = pokemon_parser.get_pokemon_encounter_count(name)

    def quit_info_menu(self):
        self.in_info_menu = False
        self.info_pkmn = None
        self.info_pkmn_cached_img = None
        self.info_pkmn_cached_count = -1

    def update(self):
        super().update()

    def render(self, screen: pygame.Surface):
        if self.in_info_menu:
            screen.blit(FRAME, (0, 0))
            text.draw_centered_text(self.info_pkmn.get_name(), 72, 14, screen, pygame.font.Font("res/pkmndpb.ttf", 18))
            # stats
            text.draw_centered_text("PV: " + str(self.info_pkmn.get_hp()), 8 + 64, 166, screen)
            text.draw_centered_text("Puissance: " + str(self.info_pkmn.get_strength()), 8 + 64, 186, screen)
            text.draw_centered_text("Défense: " + str(self.info_pkmn.get_defense()), 8 + 64, 206, screen)
            text.draw_centered_text("Rencontres: " + str(self.info_pkmn_cached_count), 8 + 64, 226, screen)
            # types
            if self.info_pkmn.get_types()[1].get_type() == -1:
                screen.blit(self.info_pkmn.get_types()[0].get_type_image(), (
                24 + 48 - self.info_pkmn.get_types()[0].get_type_image().get_width() / 2,
                124 + 13 - self.info_pkmn.get_types()[0].get_type_image().get_height() / 2))
            else:
                screen.blit(self.info_pkmn.get_types()[0].get_type_image(), (
                24, 124 + 13 - self.info_pkmn.get_types()[0].get_type_image().get_height() / 2))
                screen.blit(self.info_pkmn.get_types()[1].get_type_image(), (
                24 + 96 - self.info_pkmn.get_types()[1].get_type_image().get_width(),
                124 + 13 - self.info_pkmn.get_types()[1].get_type_image().get_height() / 2))
            # img pokemon
            screen.blit(self.info_pkmn_cached_img, (24, 28))

            # attacks descs
            text.draw_centered_text("ATTAQUES:", 162+111, 6+17, screen, pygame.font.Font("res/pkmndpb.ttf", 18), color=self.title_color)
            pos_offset = 96
            for i in range(len(self.info_pkmn.get_attacks())):
                attack: Attack = self.info_pkmn.get_attacks()[i]
                att_img = attack.get_attack_type().get_type_image()
                text.draw_text(attack.get_name(), 172, 42 + i*pos_offset, screen)
                screen.blit(att_img, (300 + 40, 42 + i*pos_offset))
                # desc
                att_desc_box = TextBox(attack.get_desc(), 166, 60 + i*pos_offset, 217, line_limit=3)
                att_desc_box.render(screen)
                # attacks stats
                power = round(attack.get_attack_strength()*100)
                rate = round(attack.get_success_rate() * 100)
                if power <= 0:
                    power = "N/A"
                if rate <= 0:
                    rate = "N/A"
                text.draw_text("PUISSANCE : "+str(power), 166, 110 + i*pos_offset, screen)
                text.draw_text("PRECISION : " + str(rate), 166+128, 110 + i * pos_offset, screen)

        else:
            if self.list_offset > 0:
                screen.blit(ARROW, (64 + 150 - ARROW.get_width()/2, 22))
            if self.list_offset < len(POKEMONS)-4:
                screen.blit(pygame.transform.flip(ARROW, flip_x=False, flip_y=True), (64 + 150 - ARROW.get_width() / 2, 26+8+(48*4)))
            text.draw_aligned_text("Pokédex", screen.get_width()/2, 4, screen, pygame.font.Font("res/pkmndpb.ttf", 16), color=self.title_color)
            super().render(screen)

    def input(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.in_info_menu:
                    self.in_info_menu = False
                elif self.quit_state >= 0:
                    set_state(self.quit_state)

            if not self.in_info_menu:
                if event.key == pygame.K_RETURN:
                    if 0 <= self.selected_button < len(self.buttons):
                        self.buttons[self.selected_button].execute()
                # scroll pokédex up
                elif event.key == pygame.K_UP:
                    if self.selected_button == 0:
                        if self.list_offset > 0:
                            self.list_offset -= 1
                            self.set_pkmn_list_from_offset()
                    else:
                        self.move_cursor_up()
                # scroll pokédex down
                elif event.key == pygame.K_DOWN:
                    if self.selected_button == len(self.buttons) - 1:
                        if self.list_offset < len(POKEMONS) - 1:
                            self.list_offset += 1
                            self.set_pkmn_list_from_offset()
                    else:
                        self.move_cursor_down()
