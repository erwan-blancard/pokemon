import pygame
import game_state


class PokedexState(game_state.GameState):

    def __init__(self):
        super().__init__()

    def update(self):
        super().update()

    def render(self, screen: pygame.Surface):
        super().render(screen)

    def input(self, event: pygame.event.Event):
        super().input(event)
