import pygame
import game_state
import text
from game_state import GameState
from ui.button import ButtonLabel, ButtonIcon


class MenuState(GameState):

    def __init__(self):
        super().__init__()
        # window_bounds = pygame.display.get_window_size()
        # self.buttons += []
        # self.titlelogo = pygame.image.load("res/logo.png")
        # self.titlelogo = pygame.transform.scale(self.titlelogo, (136*3, 40*3))

    def update(self):
        super().update()

    def render(self, screen: pygame.Surface):
        super().render(screen)
        # screen.blit(self.titlelogo, (screen.get_width()/2 - self.titlelogo.get_width()/2, 72))

    def input(self, event: pygame.event.Event):
        super().input(event)
