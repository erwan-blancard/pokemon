import pygame

import pokemon
import pokemon_parser
from game_state import *


class AskResetState(GameState):

    def __init__(self):
        super().__init__()
        self.buttons = [
            ButtonLabel("Oui", 200-16, 150, 32, 16, lambda: self.__reset()),
            ButtonLabel("Non", 200-16, 164, 32, 16, lambda: set_state(MENU))
        ]

    def __reset(self):
        pokemon_parser.create_file(pokemon_parser.FILE_POKEDEX)
        pokemon.POKEMONS.clear()
        pokemon_parser.load_pokemons()
        pokemon_parser.add_to_pokedex(pokemon.POKEMONS[0].get_name())
        set_state(MENU)

    def render(self, screen: pygame.Surface):
        super().render(screen)
        text.draw_aligned_text("Réinitialiser le jeu ?", screen.get_width()/2, 16, screen, pygame.font.Font("res/pkmndpb.ttf", 32))
        text.draw_aligned_text("Cette action est définitive !", screen.get_width()/2, 56, screen, pygame.font.Font("res/pkmndpb.ttf", 24))