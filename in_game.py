import random
import time

import pygame

import game_state
import pokedex
import pokemon
import pokemon_parser
import text
from game_state import GameState
from pokemon import *
from combat import Combat
from ui.button_icon import ButtonIcon
from pokedex import ARROW
from ui.button_label import ButtonLabel

BUTTON_BG = pygame.image.load("res/pokédex_button_small.png")


class InGameState(GameState):

    def __init__(self):
        super().__init__()
        self.__in_battle = False
        self.__combat: Combat = None

        self.__pkmn_player: Pokemon = None
        self.__pkmn_opponent: Pokemon = None

        self.__pkmn_player_has_evolved = False
        self.__pkmn_player_reached_level_limit = False

        # create blank buttons
        for i in range(3):
            img_label = pygame.Surface((250, 48), pygame.SRCALPHA)
            img_label.blit(BUTTON_BG, (0, 0))
            text.draw_text("---", 56, 16, img_label, text.get_font(16))
            self.buttons.append(ButtonIcon(88, 24+32 + 8 + (i * 48), 250, 48, img_label))

        self.list_offset = 0
        self.set_pkmn_list_from_offset()

        self.current_button = 0
        self.game_over_buttons = [
            ButtonLabel("Rejouer", 200-32, 190, 64, 16, lambda: self.__start_battle(), font=pygame.font.Font("res/pkmndpb.ttf", 18), color=(255, 255, 255)),
            ButtonLabel("Quitter", 200-32, 212, 64, 16, lambda: game_state.set_state(game_state.MENU), font=pygame.font.Font("res/pkmndpb.ttf", 18), color=(255, 255, 255))
        ]
        self.__timer = 0

    def set_pkmn_list_from_offset(self):
        if len(POKEMONS) <= 3:
            self.list_offset = 0
        elif self.list_offset > len(POKEMONS) - 3:
            self.list_offset = len(POKEMONS) - 3
        for i in range(3):
            pkmn_i = i+self.list_offset
            img_label = pygame.Surface((250, 48), pygame.SRCALPHA)
            img_label.blit(BUTTON_BG, (0, 0))
            # if entry (pkmn_i) is a pokémon in POKEMONS
            if pkmn_i < len(POKEMONS):
                pkmn_name = POKEMONS[pkmn_i].get_name()
                # if pokémon was encountered at least once
                if pokemon_parser.pokemon_in_pokedex(pkmn_name) and pokemon_parser.get_pokemon_encounter_count(pkmn_name) > 0:
                    in_team = pokemon_parser.is_pokemon_in_team(pkmn_name)
                    # if pokémon not in team
                    pkmn_img = POKEMONS[pkmn_i].get_image_icon()
                    if not in_team:
                        pkmn_img = pokedex.colorize(pkmn_img, (0, 0, 0))
                    img_label.blit(pkmn_img, (0, 0))
                    # show types
                    if POKEMONS[pkmn_i].get_types()[1].get_type() == -1:
                        img_pkmn_type = POKEMONS[pkmn_i].get_types()[0].get_type_image()
                        img_label.blit(img_pkmn_type, (img_label.get_width() - 10 - img_pkmn_type.get_width(), img_label.get_height()/2 - img_pkmn_type.get_height()/2))
                    else:
                        for j in range(len(POKEMONS[pkmn_i].get_types())):
                            img_pkmn_type = POKEMONS[pkmn_i].get_types()[j].get_type_image()
                            img_label.blit(img_pkmn_type, (img_label.get_width() - 50 - img_pkmn_type.get_width() + j*40, img_label.get_height() / 2 - img_pkmn_type.get_height() / 2))

                    text.draw_text(POKEMONS[pkmn_i].get_name(), 56, 16, img_label, text.get_font(16))
                    if in_team:
                        self.buttons[i] = ButtonIcon(88, 24+32 + 8 + (i * 48), 250, 48, img_label,
                                                     lambda pkmn_index=pkmn_i: self.__select_pkmn(pkmn_index))
                    else:
                        self.buttons[i] = ButtonIcon(88, 24 + 32 + 8 + (i * 48), 250, 48, img_label)

                # if pokémon was not encountered
                else:
                    pkmn_img = POKEMONS[pkmn_i].get_image_icon()
                    pkmn_img = pokedex.colorize(pkmn_img, (0, 0, 0))
                    img_label.blit(pkmn_img, (0, 0))
                    text.draw_text("???", 56, 16, img_label, text.get_font(16))
                    self.buttons[i] = ButtonIcon(88, 24+32 + 8 + (i * 48), 250, 48, img_label)

            # else if entry doesn't exist
            else:
                text.draw_text("---", 56, 16, img_label, text.get_font(16))
                self.buttons[i] = ButtonIcon(88, 24+32 + 8 + (i * 48), 250, 48, img_label)

    def __select_pkmn(self, pkmn_index: int):
        self.__pkmn_player = POKEMONS[pkmn_index]
        self.__start_battle()

    def __start_battle(self):
        if self.__pkmn_player is not None:
            if self.__pkmn_player_has_evolved:
                self.__pkmn_player = pokemon.get_pokemon_by_name(self.__pkmn_player.get_evolution_name())
            self.__timer = 0
            self.__pkmn_player_has_evolved = False
            self.__pkmn_player_reached_level_limit = False
            self.__pkmn_opponent = POKEMONS[random.randint(0, len(POKEMONS) - 1)]
            self.__in_battle = True
            opponent_level = self.__pkmn_player.get_level() + random.randint(-3, 3)
            if opponent_level < 1:
                opponent_level = 1
            if opponent_level > pokemon.MAX_LEVEL:
                opponent_level = MAX_LEVEL
            self.__combat = Combat(self.__pkmn_player.copy(), self.__pkmn_opponent.copy_with_set_level(opponent_level))

    def __add_level_to_player(self):
        i = 0
        while i < len(POKEMONS):
            if POKEMONS[i].get_name() == self.__pkmn_player.get_name():
                if POKEMONS[i].add_level():
                    pokemon_parser.set_team_level_of_pokemon(self.__pkmn_player.get_name(), self.__pkmn_player.get_level())
                    # manage pkmn evolution
                    if POKEMONS[i].can_evolve() and POKEMONS[i].get_evolution_level() == POKEMONS[i].get_level() and pokemon_parser.pokemon_exists(POKEMONS[i].get_evolution_name()):
                        # no evolution if pokémon evolution is in team
                        if not pokemon_parser.is_pokemon_in_team(POKEMONS[i].get_evolution_name()):
                            pkmn_evolution = pokemon.get_pokemon_by_name(POKEMONS[i].get_evolution_name())
                            pokemon_parser.add_to_pokedex(pkmn_evolution.get_name())
                            pokemon_parser.set_pokemon_in_team_state(pkmn_evolution.get_name(), True)
                            pkmn_evolution.set_level(POKEMONS[i].get_evolution_level())
                            pokemon_parser.set_team_level_of_pokemon(pkmn_evolution.get_name(), POKEMONS[i].get_evolution_level())
                            # remove old pkmn
                            pokemon_parser.set_pokemon_in_team_state(POKEMONS[i].get_name(), False)
                            pokemon_parser.set_team_level_of_pokemon(POKEMONS[i].get_name(), 1)
                            self.__pkmn_player_has_evolved = True
                else:
                    self.__pkmn_player_reached_level_limit = True
                break
            i += 1

    def update(self):
        super().update()
        if self.__in_battle:
            self.__combat.update()
            if self.__combat.is_phase_out_anim_finished() and self.__timer == 0:
                self.__timer = time.time()
                if self.__combat.is_opponent_dead():
                    if not pokemon_parser.is_pokemon_in_team(self.__pkmn_opponent.get_name()):
                        pokemon_parser.set_pokemon_in_team_state(self.__pkmn_opponent.get_name(), True)
                        pokemon_parser.set_team_level_of_pokemon(self.__pkmn_opponent.get_name(), self.__combat.get_opponent_level())
                    self.__add_level_to_player()

    def render(self, screen: pygame.Surface):
        if self.__in_battle:
            self.__combat.render(screen)
            if self.__combat.is_phase_out_anim_finished() and time.time() - self.__timer >= 1.6:
                self.render_overlay(screen)
                if self.__combat.is_player_dead():
                    text.draw_aligned_text("Vous avez perdu !", screen.get_width()/2, 16, screen, pygame.font.Font("res/pkmndpb.ttf", 24), color=(255, 255, 255))
                elif self.__combat.is_opponent_dead():
                    text.draw_aligned_text("Vous avez gagné !", screen.get_width() / 2, 16, screen, pygame.font.Font("res/pkmndpb.ttf", 24), color=(255, 255, 255))
                    # level + evolution
                    if self.__pkmn_player_reached_level_limit:
                        text.draw_aligned_text(self.__pkmn_player.get_name() + " :  Lvl  " + str(self.__pkmn_player.get_level()), screen.get_width() / 2, 60 + 16, screen, pygame.font.Font("res/pkmndpb.ttf", 18), color=(255, 255, 255))
                    else:
                        if self.__pkmn_player_has_evolved:
                            text.draw_aligned_text(self.__pkmn_player.get_name() + " gagne un niveau !", screen.get_width() / 2, 40+16, screen, pygame.font.Font("res/pkmndpb.ttf", 18), color=(255, 255, 255))
                            text.draw_aligned_text("Lvl  " + str(self.__pkmn_player.get_level() - 1) + "  ->  " + str(self.__pkmn_player.get_level()), screen.get_width() / 2, 60+16, screen, pygame.font.Font("res/pkmndpb.ttf", 18), color=(255, 255, 255))
                            text.draw_aligned_text(self.__pkmn_player.get_name() + " évolue en " + self.__pkmn_player.get_evolution_name() + " !", screen.get_width()/2, 88+16, screen, pygame.font.Font("res/pkmndpb.ttf", 18), color=(255, 255, 255))
                            # imgs
                            text.draw_aligned_text("->", screen.get_width()/2, 128+24, screen, pygame.font.Font("res/pkmndpb.ttf", 12), color=(255, 255, 255))
                            screen.blit(self.__pkmn_player.get_image_icon(), (screen.get_width()/2-64, 128))
                            screen.blit(pokemon.get_pokemon_by_name(self.__pkmn_player.get_evolution_name()).get_image_icon(), (screen.get_width() / 2 + 24, 128))
                        else:
                            text.draw_aligned_text(self.__pkmn_player.get_name() + " gagne un niveau !", screen.get_width()/2, 72, screen, pygame.font.Font("res/pkmndpb.ttf", 18), color=(255, 255, 255))
                            text.draw_aligned_text("Lvl  " + str(self.__pkmn_player.get_level()-1) + "  ->  " + str(self.__pkmn_player.get_level()), screen.get_width()/2, 96, screen, pygame.font.Font("res/pkmndpb.ttf", 18), color=(255, 255, 255))
                i = 0
                while i < len(self.game_over_buttons):
                    self.game_over_buttons[i].render(screen)
                    if i == self.current_button:
                        self.game_over_buttons[i].render_cursor(screen, offset=4)
                    i += 1
        else:
            text.draw_aligned_text("Jouer avec:", screen.get_width()/2, 24, screen, pygame.font.Font("res/pkmndpb.ttf", 18))
            if self.list_offset > 0:
                screen.blit(ARROW, (88 + 128 - ARROW.get_width()/2, 22+32))
            if self.list_offset < len(POKEMONS)-3:
                screen.blit(pygame.transform.flip(ARROW, flip_x=False, flip_y=True), (88 + 128 - ARROW.get_width() / 2, 26+32+8+(48*3)))
            super().render(screen)

    def input(self, event: pygame.event.Event):
        if self.__in_battle:
            self.__combat.input(event)

            if self.__combat.is_phase_out_anim_finished() and time.time() - self.__timer >= 1.6 and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if 0 <= self.current_button < len(self.game_over_buttons):
                        self.game_over_buttons[self.current_button].execute()
                elif event.key == pygame.K_UP:
                    if self.current_button - 1 >= 0:
                        self.current_button -= 1
                    else:
                        self.current_button = len(self.game_over_buttons) - 1
                elif event.key == pygame.K_DOWN:
                    if self.current_button + 1 < len(self.game_over_buttons):
                        self.current_button += 1
                    else:
                        self.current_button = 0
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state.set_state(game_state.MENU)
                elif event.key == pygame.K_RETURN:
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
