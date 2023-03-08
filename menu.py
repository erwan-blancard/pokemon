import pygame

import pokemon
import text
from game_state import *
from ui.button import ButtonLabel, ButtonIcon


class MenuState(GameState):

    def __init__(self):
        super().__init__()
        self.buttons += [
            ButtonLabel("Jouer", 200-22, 128, 44, 24, command=lambda: set_state(INGAME)),
            ButtonLabel("Pokédex", 200-30, 152, 60, 24, command=lambda: set_state(POKEDEX)),
            ButtonLabel("Ajouter un Pokémon", 200-60, 176, 120, 24, command=lambda: set_state(POKEMON_MAKER))
        ]
        self.titlelogo = pygame.image.load("res/logo.png")

    def update(self):
        super().update()

    def render(self, screen: pygame.Surface):
        super().render(screen)
        screen.blit(self.titlelogo, (screen.get_width()/2 - self.titlelogo.get_width()/2, 12))
        text.draw_aligned_text("LaPlateforme Édition", screen.get_width()/2+4, 12+self.titlelogo.get_height(), screen, pygame.font.Font("res/pkmndpb.ttf", 16))
        text.draw_text("Pokémons: "+str(len(pokemon.POKEMONS)), 2, 224, screen, text.font())

    def input(self, event: pygame.event.Event):
        super().input(event)
