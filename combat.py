import random
import time

import pygame

import game_state
import text
import ui.hp_box
from pokedex import PokedexState
from ui.button import *
from pokemon import *
from ui.hp_box import HpBox
from pokemon_attacks.attack import Attack
from ui.text_box import TextBox

FIGHT_SCENE = pygame.image.load("res/scene.png")
SCENE_FRAME = pygame.transform.scale(pygame.image.load("res/scene_frame.png"), (208, 40))

# TIMES FOR ANIMATIONS
INTRO_TIME = 1.0
SPEECH_INTERVAL_TIME = 0.9
DMG_INTERVAL_TIME = 0.1

# TEXTS
ATT_USE = "{} utilise {}!"
ATT_SUP_EFF = "C'est super efficace!"
ATT_NOT_EFF = "Ce n'est pas très efficace..."
ATT_NO_EFF = "...mais {} n'a aucun effet!"
ATT_MISS = "...mais {} a raté!"


def render_overlay(screen: pygame.Surface):
    rect_over = pygame.Surface((400, 240))
    rect_over.set_alpha(160)
    rect_over.fill((40, 40, 40))
    screen.blit(rect_over, (0, 0))


class Combat:

    def __init__(self, pkmn_player: Pokemon, pkmn_opponent: Pokemon):
        self.__pkmn_player = pkmn_player
        self.__pkmn_player_cached_img = pygame.transform.scale(self.__pkmn_player.get_image_back(), (96*2, 96*2))
        self.__pkmn_opponent = pkmn_opponent
        self.__pkmn_opponent_cached_img = pygame.transform.scale(self.__pkmn_opponent.get_image_front(), (96*2, 96*2))

        # pokédex menu
        self.__pokedex_menu: PokedexState = None

        # hp boxes
        self.__player_hp_box = HpBox(self.__pkmn_player, 2, 50)
        self.__opponent_hp_box = HpBox(self.__pkmn_opponent, 222, 172)

        # used for anim times
        self.__timer = 0.0

        # intro animation
        self.__intro_finished = False
        self.__pkmn_player_x = 400
        self.__pkmn_opponent_x = 0

        # states
        self.__selected_button = 0

        self.__buttons_choose_action = [
            ButtonLabel("ATTAQUER", 2+8, 6, 58, 16, command=lambda: self.__set_attacks_menu()),
            ButtonLabel("POKÉDEX", 2+8+58+24, 6, 50, 16, command=lambda: self.__open_pokedex()),
            ButtonLabel("FUIR", 2+8+58+48+50, 6, 28, 16, command=lambda: game_state.set_state(game_state.MENU))
        ]
        """Button list for action selection"""

        self.__in_choose_attacks = False
        att_1 = self.__pkmn_player.get_attacks()[0]
        att_2 = self.__pkmn_player.get_attacks()[1]
        self.__buttons_choose_attack = [
            ButtonLabel(att_1.get_name(), 14, 0, text.font().size(att_1.get_name())[0]+2, 16, command=lambda: self.__set_attack_state(0), center_text=False),
            ButtonLabel(att_2.get_name(), 14+28+text.font().size(att_1.get_name())[0]+2, 0, text.font().size(att_2.get_name())[0]+2, 16, command=lambda: self.__set_attack_state(1), center_text=False)
        ]
        """Button list for attack selection"""

        # manage attack turn anims
        self.__in_attack_state = False

        self.__player_attack_index = 0
        self.__opponent_attack_index = 0
        self.__pending_player_att_damage = 0
        self.__pending_opponent_att_damage = 0

        self.__damaging_opponent = False
        """Used when the game will try to remove HPs of the opponent"""
        self.__damaging_player = False
        """Used when the game will try to remove HPs of the player"""
        self.__opponent_damaged = False
        """Used when the game is done removing HPs of the opponent"""
        self.__player_damaged = False
        """Used when the game is done removing HPs of the player"""

        # attack miss or no effect
        self.__player_attack_error = False
        self.__opponent_attack_error = False

        self.__timer = time.time()

    def __set_attack_state(self, player_attack_index):
        # pokémons attacks
        self.__player_attack_index = player_attack_index
        self.__opponent_attack_index = random.randint(0, 1)

        # attack damages + pending damages
        self.__player_att_damage = self.__pkmn_player.get_attack_damage(self.__player_attack_index, self.__pkmn_opponent.get_types_type())
        self.__opponent_att_damage = self.__pkmn_opponent.get_attack_damage(self.__opponent_attack_index, self.__pkmn_player.get_types_type())
        self.__pending_player_att_damage = self.__player_att_damage
        self.__pending_opponent_att_damage = self.__opponent_att_damage

        self.__damaging_opponent = False
        self.__damaging_player = False
        self.__opponent_damaged = False
        self.__player_damaged = False

        self.__player_attack_error = False
        self.__opponent_attack_error = False

        self.__in_choose_attacks = False
        self.__in_attack_state = True
        self.__timer = time.time()

    def __goto_previous_menu(self):
        if self.__in_choose_attacks:
            self.__selected_button = 0
            self.__in_choose_attacks = False
        elif self.is_pokedex_open() and not self.__pokedex_menu.in_info_menu:
            self.__selected_button = 0
            self.__close_pokedex()

    def __set_attacks_menu(self):
        self.__selected_button = 0
        self.__in_choose_attacks = True

    def __open_pokedex(self):
        self.__pokedex_menu = PokedexState(quit_state=-1, title_color=(255, 255, 255))

    def __close_pokedex(self):
        self.__pokedex_menu = None

    def is_pokedex_open(self):
        return self.__pokedex_menu is not None

    def __get_current_button_list(self):
        button_list = self.__buttons_choose_action
        if self.__in_choose_attacks:
            button_list = self.__buttons_choose_attack
        return button_list

    def __update_attack_state(self):
        if self.__in_attack_state:
            time_passed = time.time() - self.__timer
            if not self.__opponent_damaged:
                if time_passed >= SPEECH_INTERVAL_TIME:
                    self.__damaging_opponent = True
                    self.__timer = time.time()
                if self.__damaging_opponent:
                    # if the player's attack missed or is lower or equal to 0
                    if self.__player_attack_error:
                        if time_passed >= SPEECH_INTERVAL_TIME:
                            self.__opponent_damaged = True
                            self.__timer = time.time()
                    # else if the player's attack don't miss or is greater than 0
                    elif not self.__player_att_damage <= 0:
                        if time_passed >= DMG_INTERVAL_TIME and self.__pending_player_att_damage > 0:
                            self.__pkmn_opponent.damage(1)
                            self.__pending_player_att_damage -= 1

                            if self.__pkmn_opponent.get_current_hp() <= 0:
                                self.__pending_player_att_damage = 0

                            self.__timer = time.time()
                        elif self.__pending_player_att_damage <= 0:
                            self.__opponent_damaged = True
                    else:
                        self.__player_attack_error = True
                        self.__timer = time.time()

            elif not self.__player_damaged:
                if time_passed >= SPEECH_INTERVAL_TIME:
                    self.__damaging_player = True
                    self.__timer = time.time()
                if self.__damaging_player:
                    # if the opponent's attack missed or is lower or equal to 0
                    if self.__opponent_attack_error:
                        if time_passed >= SPEECH_INTERVAL_TIME:
                            self.__player_damaged = True
                            self.__timer = time.time()
                    # else if the opponent's attack don't miss or is greater than 0
                    elif not self.__opponent_att_damage <= 0:
                        if time_passed >= DMG_INTERVAL_TIME and self.__pending_opponent_att_damage > 0:
                            self.__pkmn_player.damage(1)
                            self.__pending_opponent_att_damage -= 1

                            if self.__pkmn_player.get_current_hp() <= 0:
                                self.__pending_opponent_att_damage = 0

                            self.__timer = time.time()
                        elif self.__pending_opponent_att_damage <= 0:
                            self.__player_damaged = True
                    else:
                        self.__opponent_attack_error = True
                        self.__timer = time.time()

            # exit attack state
            if self.__player_damaged:
                self.__in_attack_state = False

    def update(self):
        if not self.__intro_finished:
            time_passed = time.time() - self.__timer
            if time_passed >= INTRO_TIME:
                self.__pkmn_player_x = 0
                self.__pkmn_opponent_x = 400
                self.__intro_finished = True
            else:
                self.__pkmn_player_x = 400-int(400*(time_passed/INTRO_TIME))
                self.__pkmn_opponent_x = int(400*(time_passed/INTRO_TIME))
        else:
            if self.is_pokedex_open():
                self.__pokedex_menu.update()

            # update attack state
            self.__update_attack_state()

    def render(self, screen: pygame.Surface):
        screen.blit(FIGHT_SCENE, (0, 0))
        screen.blit(self.__pkmn_opponent_cached_img, (self.__pkmn_opponent_x - self.__pkmn_opponent_cached_img.get_width(), 0))
        screen.blit(self.__pkmn_player_cached_img, (self.__pkmn_player_x, 100))
        if self.__intro_finished:
            self.__player_hp_box.render(screen)
            self.__opponent_hp_box.render(screen)

            if self.is_pokedex_open():
                render_overlay(screen)
                self.__pokedex_menu.render(screen)
            else:
                screen.blit(SCENE_FRAME, (2, 0))
                if self.__in_attack_state:
                    text_state = ""
                    if not self.__opponent_damaged:
                        player_attack: Attack = self.__pkmn_player.get_attacks()[self.__player_attack_index]
                        text_state = ATT_USE.format(self.__pkmn_player.get_name(), player_attack.get_name())
                        # get text from state
                        if self.__damaging_opponent:
                            if self.__player_attack_error:
                                if self.__player_att_damage == 0:
                                    text_state = ATT_NO_EFF.format(player_attack.get_name())
                                elif self.__player_att_damage == -1:
                                    text_state = ATT_MISS.format(player_attack.get_name())
                            else:
                                if player_attack.is_super_effective(self.__pkmn_player.get_strength(), self.__player_att_damage):
                                    text_state = ATT_SUP_EFF
                                elif player_attack.is_not_effective(self.__pkmn_player.get_strength(), self.__player_att_damage):
                                    text_state = ATT_NOT_EFF

                    elif not self.__player_damaged:
                        opponent_attack: Attack = self.__pkmn_opponent.get_attacks()[self.__opponent_attack_index]
                        text_state = ATT_USE.format(self.__pkmn_opponent.get_name(), opponent_attack.get_name())
                        # get text from state
                        if self.__damaging_player:
                            if self.__opponent_attack_error:
                                if self.__opponent_att_damage == 0:
                                    text_state = ATT_NO_EFF.format(opponent_attack.get_name())
                                elif self.__opponent_att_damage == -1:
                                    text_state = ATT_MISS.format(opponent_attack.get_name())
                            else:
                                if opponent_attack.is_super_effective(self.__pkmn_opponent.get_strength(), self.__opponent_att_damage):
                                    text_state = ATT_SUP_EFF
                                elif opponent_attack.is_not_effective(self.__pkmn_opponent.get_strength(), self.__opponent_att_damage):
                                    text_state = ATT_NOT_EFF
                    text_box = TextBox(text_state, 6*2, 0, 92*2, line_limit=2)
                    text_box.render(screen)
                else:
                    buttons = self.__get_current_button_list()
                    i = 0
                    while i < len(buttons):
                        buttons[i].render(screen)
                        # render attack type
                        if self.__in_choose_attacks:
                            type_img = self.__pkmn_player.get_attacks()[i].get_attack_type().get_type_image()
                            screen.blit(type_img, (buttons[i].x + (buttons[i].width - type_img.get_width()) / 2, buttons[i].y + buttons[i].height))
                        if i == self.__selected_button:
                            buttons[i].render_cursor(screen, right=True)
                        i += 1

    def input(self, event: pygame.event.Event):
        if self.__intro_finished:
            # pokédex inputs
            if self.is_pokedex_open():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.__goto_previous_menu()
                if self.is_pokedex_open():
                    self.__pokedex_menu.input(event)
            else:
                # get the currently used button list
                button_list = self.__get_current_button_list()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.__goto_previous_menu()
                    elif event.key == pygame.K_RETURN:
                        if 0 <= self.__selected_button < len(button_list):
                            button_list[self.__selected_button].execute()
                    elif event.key == pygame.K_LEFT:
                        self.move_cursor_left(button_list)
                    elif event.key == pygame.K_RIGHT:
                        self.move_cursor_right(button_list)

    def move_cursor_left(self, button_list):
        if self.__selected_button - 1 >= 0:
            self.__selected_button -= 1
        else:
            self.__selected_button = len(button_list)-1

    def move_cursor_right(self, button_list):
        if self.__selected_button + 1 < len(button_list):
            self.__selected_button += 1
        else:
            self.__selected_button = 0
