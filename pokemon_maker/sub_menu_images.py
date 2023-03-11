import pygame.image

import game_state
from pokemon_maker.sub_menu import *
from ui.button_icon import ButtonIcon
import tkinter.filedialog

from ui.button_label import ButtonLabel


class SubMenuImages(SubMenu):

    def __init__(self, paths: list[str, str, str]):
        super().__init__("", "Changer les images:")
        self._validated = False
        self._paths = paths
        self._cached_images = [
            pygame.image.load("res/pokemons/INVALID_icon.png"),
            pygame.image.load("res/pokemons/INVALID_front.png"),
            pygame.image.load("res/pokemons/INVALID_back.png")
        ]
        for i in range(3):
            try:
                size = 96
                if i == 0:
                    size = 48
                img = pygame.transform.scale(pygame.image.load(self._paths[i]), (size, size))
                self._cached_images[i] = img
            except:
                pass

        self.__buttons = [
            ButtonLabel("", 32, 120-24, 48, 48, lambda: self.__open_file_window(0)),
            ButtonLabel("", 32+96+16, 120 - 48, 96, 96, lambda: self.__open_file_window(1)),
            ButtonLabel("", 32+96+16+96+16, 120 - 48, 96, 96, lambda: self.__open_file_window(2))
        ]
        self.__confirm_button = ButtonLabel("Valider", 200-40, 200, 80, 32, lambda: self.__set_validated(), font=pygame.font.Font("res/pkmndpb.ttf", 24), color=(255, 255, 255))
        self.__selected_button = 0
        self.__focus_confirm_button = False

    def get_value(self):
        return self._paths

    def __set_validated(self):
        self._validated = True

    def has_validated(self):
        return self._validated

    def __open_file_window(self, img_index):
        path = tkinter.filedialog.askopenfilename()
        try:
            size = 96
            if img_index == 0:
                size = 48
            img = pygame.transform.scale(pygame.image.load(path), (size, size))
            self._cached_images[img_index] = img
            self._paths[img_index] = path
        except Exception as e:
            print(e)

    def render(self, screen: pygame.Surface):
        # overlay
        rect_over = pygame.Surface((400, 240))
        rect_over.set_alpha(160)
        rect_over.fill((40, 40, 40))
        screen.blit(rect_over, (0, 0))

        text.draw_aligned_text(self._title, screen.get_width() / 2, 12, screen, pygame.font.Font("res/pkmndpb.ttf", 32), color=(255, 255, 255))

        # imgs
        for i in range(len(self._cached_images)):
            screen.blit(self._cached_images[i], (32 + i*(96+16), 120-self._cached_images[i].get_height()/2))

        i = 0
        while i < len(self.__buttons):
            self.__buttons[i].render(screen)
            if not self.__focus_confirm_button and i == self.__selected_button:
                self.__buttons[i].render_cursor(screen, offset=4)
            i += 1
        self.__confirm_button.render(screen)
        if self.__focus_confirm_button:
            self.__confirm_button.render_cursor(screen, offset=4)

    def input(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                if self.__focus_confirm_button:
                    self.__focus_confirm_button = False
                else:
                    self.__focus_confirm_button = True
            elif self.__focus_confirm_button:
                if event.key == pygame.K_RETURN:
                    self.__confirm_button.execute()
            else:
                if event.key == pygame.K_RETURN:
                    if 0 <= self.__selected_button < len(self.__buttons):
                        self.__buttons[self.__selected_button].execute()
                elif event.key == pygame.K_LEFT:
                    self.move_cursor_left()
                elif event.key == pygame.K_RIGHT:
                    self.move_cursor_right()

    def move_cursor_left(self):
        if self.__selected_button - 1 >= 0:
            self.__selected_button -= 1
        else:
            self.__selected_button = len(self.__buttons)-1

    def move_cursor_right(self):
        if self.__selected_button + 1 < len(self.__buttons):
            self.__selected_button += 1
        else:
            self.__selected_button = 0
