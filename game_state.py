import pygame
from ui.button_base import *
from ui.button_label import *
from ui.button_icon import *

# Holds the current state ID of the game
state = 0
update_pending = False

MENU = 0
INGAME = 1
POKEDEX = 2
POKEMON_MAKER = 3


def set_state(newstate):
    global state
    global update_pending
    state = newstate
    update_pending = True


# base class for states with basic button support
class GameState:
    def __init__(self):
        self.buttons: list[BaseButton] = []
        self.selected_button = 0
        self.render_cursor_right = False

    def move_cursor_down(self):
        if self.selected_button + 1 < len(self.buttons):
            self.selected_button += 1
        else:
            self.selected_button = 0

    def move_cursor_up(self):
        if self.selected_button - 1 >= 0:
            self.selected_button -= 1
        else:
            self.selected_button = len(self.buttons)-1

    def render_overlay(self, screen: pygame.Surface):
        rect_over = pygame.Surface((400, 240))
        rect_over.set_alpha(160)
        rect_over.fill((40, 40, 40))
        screen.blit(rect_over, (0, 0))

    def update(self):
        pass

    def render(self, screen: pygame.Surface):
        i = 0
        while i < len(self.buttons):
            self.buttons[i].render(screen)
            if i == self.selected_button:
                self.buttons[i].render_cursor(screen, self.render_cursor_right, 4)
            i += 1

    def input(self, event: pygame.event.Event):
        # for button in self.buttons:
        #     button.mouse_input(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if 0 <= self.selected_button < len(self.buttons):
                    self.buttons[self.selected_button].execute()
            elif event.key == pygame.K_UP:
                self.move_cursor_up()
            elif event.key == pygame.K_DOWN:
                self.move_cursor_down()
