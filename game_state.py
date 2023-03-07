import pygame
import ui.button as button

# Holds the current state ID of the game
state = 0
update_pending = False

MENU = 0
INGAME = 1
POKEDEX = 2
ADD_POKEMON = 3


def set_state(newstate):
    global state
    global update_pending
    state = newstate
    update_pending = True


# base class for states with basic button support
class GameState:
    def __init__(self):
        self.buttons: list[button.BaseButton] = []

    def update(self):
        pass

    def render(self, screen: pygame.Surface):
        for button in self.buttons:
            button.render(screen)

    def input(self, event: pygame.event.Event):
        for button in self.buttons:
            button.mouse_input(event)
