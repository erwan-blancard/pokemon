import time

import pygame
from game_state import GameState
from pokedex import PokedexState
from pokemon import *
from combat import Combat
from ui.button import *


class InGameState(GameState):

    def __init__(self):
        super().__init__()
        self.__in_battle = False
        self.__combat: Combat = None

        self.__start_battle(POKEMONS[0].copy(), POKEMONS[6].copy())

    def __start_battle(self, pkmn_player, pkmn_opponent):
        self.__in_battle = True
        self.__combat = Combat(pkmn_player, pkmn_opponent)

    def update(self):
        super().update()
        if self.__in_battle:
            self.__combat.update()

    def render(self, screen: pygame.Surface):
        super().render(screen)
        if self.__in_battle:
            self.__combat.render(screen)

    def input(self, event: pygame.event.Event):
        super().input(event)
        if self.__in_battle:
            self.__combat.input(event)
