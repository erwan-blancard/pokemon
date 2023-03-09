import pygame

import game_state
import text
import ui.hp_box
from pokedex import PokedexState
from ui.button import *
from pokemon import *
from ui.hp_box import HpBox

FIGHT_SCENE = pygame.image.load("res/scene.png")
SCENE_FRAME = pygame.transform.scale(pygame.image.load("res/scene_frame.png"), (208, 40))


def render_overlay(screen: pygame.Surface):
    rect_over = pygame.Surface((400, 240))
    rect_over.set_alpha(100)
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

        # intro animation
        self.__intro_finished = False
        self.__pkmn_player_x = 400
        self.__pkmn_opponent_x = 0

        # states
        self.__selected_button = 0

        self.__buttons_choose_action = [
            ButtonLabel("ATTAQ.", 2+6, 4, 28, 16, command=lambda: self.set_attacks_menu()),
            ButtonLabel("POKÉDEX", 2+38, 4, 50, 16, command=lambda: self.__open_pokedex()),
            ButtonLabel("FUIR", 2+90, 4, 28, 16, command=lambda: game_state.set_state(game_state.MENU))
        ]
        """Button list for action selection"""

        self.__in_choose_attacks = False
        self.__buttons_choose_attack = [
            ButtonLabel(self.__pkmn_player.get_attacks()[0].get_name(), 8, 4, 32, 16, command=lambda: print("Attq 1")),
            ButtonLabel(self.__pkmn_player.get_attacks()[1].get_name(), 8+40, 4, 32, 16, command=lambda: print("Attq 2"))
        ]

    def goto_previous_menu(self):
        if self.__in_choose_attacks:
            self.__selected_button = 0
            self.__in_choose_attacks = False
        elif self.is_pokedex_open() and not self.__pokedex_menu.in_info_menu:
            self.__selected_button = 0
            self.__close_pokedex()

    def set_attacks_menu(self):
        self.__selected_button = 0
        self.__in_choose_attacks = True

    def __open_pokedex(self):
        self.__pokedex_menu = PokedexState(quit_state=-1, title_color=(255, 255, 255))

    def __close_pokedex(self):
        self.__pokedex_menu = None

    def is_pokedex_open(self):
        return self.__pokedex_menu is not None

    def update(self):
        if not self.__intro_finished:
            if self.__pkmn_opponent_x >= 400:
                self.__pkmn_player_x = 0
                self.__pkmn_opponent_x = 400
                self.__intro_finished = True
            else:
                self.__pkmn_player_x -= 1
                self.__pkmn_opponent_x += 1
        else:
            if self.is_pokedex_open():
                self.__pokedex_menu.update()

    def render(self, screen: pygame.Surface):
        screen.blit(FIGHT_SCENE, (0, 0))
        screen.blit(self.__pkmn_opponent_cached_img, (self.__pkmn_opponent_x - self.__pkmn_opponent_cached_img.get_width(), 0))
        screen.blit(self.__pkmn_player_cached_img, (self.__pkmn_player_x, 100))
        if self.__intro_finished:
            screen.blit(SCENE_FRAME, (2, 0))
            self.__player_hp_box.render(screen)
            self.__opponent_hp_box.render(screen)

            if self.__in_choose_attacks:
                for button in self.__buttons_choose_attack:
                    button.render(screen)
            elif self.is_pokedex_open():
                render_overlay(screen)
                self.__pokedex_menu.render(screen)
            else:
                for button in self.__buttons_choose_action:
                    button.render(screen)

    def input(self, event: pygame.event.Event):
        if self.__intro_finished:
            # pokédex inputs
            if self.is_pokedex_open():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.goto_previous_menu()
                if self.is_pokedex_open():
                    self.__pokedex_menu.input(event)
            else:
                # get the currently used button list
                button_list = self.__buttons_choose_action
                if self.__in_choose_attacks:
                    button_list = self.__buttons_choose_attack
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.goto_previous_menu()
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
