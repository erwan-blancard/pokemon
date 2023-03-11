import pygame

import text


class SubMenu:

    def __init__(self, value: str, title: str):
        self._value = str(value)
        self._title = title
        self._validated = False
        self._show_warning_text = False

    def render(self, screen: pygame.Surface):
        # overlay
        rect_over = pygame.Surface((400, 240))
        rect_over.set_alpha(160)
        rect_over.fill((40, 40, 40))
        screen.blit(rect_over, (0, 0))

        text.draw_aligned_text(self._title, screen.get_width()/2, 12, screen, pygame.font.Font("res/pkmndpb.ttf", 32), color=(255, 255, 255))
        text.draw_centered_text(self._value, screen.get_width()/2, screen.get_height()/2, screen, pygame.font.Font("res/pkmndpb.ttf", 32), color=(255, 255, 255))
        if self._show_warning_text:
            text.draw_aligned_text("La valeur ne doit pas être vide !", screen.get_width()/2, 160, screen, pygame.font.Font("res/pkmndpb.ttf", 20), color=(255, 255, 255))

    def has_validated(self):
        return self._validated

    def get_value(self):
        return self._value

    def input(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if len(self._value) > 0:
                    self._validated = True
                else:
                    self._show_warning_text = True
            elif event.key == pygame.K_BACKSPACE:
                self._value = self._value[:-1]
            else:
                key = pygame.key.name(event.key)
                if key in "abcdefghijklmnopqrstuvwxyz":
                    if len(self._value) <= 20:
                        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                            self._value += key.upper()
                        else:
                            self._value += key
                elif key == "space":
                    if len(self._value) <= 20:
                        self._value += " "
                elif key in ["[0]", "[1]", "[2]", "[3]", "[4]", "[5]", "[6]", "[7]", "[8]", "[9]"]:
                    if len(self._value) <= 20:
                        self._value += key[1:2]
