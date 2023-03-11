import pokemon
from pokemon_maker.sub_menu import *
from ui.button_icon import ButtonIcon
from ui.button_label import ButtonLabel


def render_overlay(screen):
    # overlay
    rect_over = pygame.Surface((400, 240))
    rect_over.set_alpha(160)
    rect_over.fill((40, 40, 40))
    screen.blit(rect_over, (0, 0))


class SubMenuTypes(SubMenu):

    def __init__(self, types: list[int], title="Changer les types:"):
        super().__init__("", title)
        self.__types = types

        self.__selected_button = 0
        self.__buttons_t = [
            ButtonLabel("", 100, 104, 32, 16, lambda: self.__open_menu_T1()),
            ButtonLabel("", 400-132, 104, 32, 16, lambda: self.__open_menu_T2())
        ]
        self.__buttons_t1 = [[], []]
        self.__buttons_t2 = [[], []]
        for i in range(20):
            icon = pokemon.get_type_by_id(i-1).get_type_image()
            if i-1 == -1:
                icon = pokemon.get_type_by_id(i-1).get_none_image()
            button = ButtonIcon(84 + (i//10)*34, 40+(i%10)*16, 32, 16, icon, command=lambda type_in=i-1: self.__close_menus(type_in))

            if i < 10:
                self.__buttons_t1[0].append(button)
            else:
                self.__buttons_t1[1].append(button)
        for i in range(20):
            icon = pokemon.get_type_by_id(i - 1).get_type_image()
            if i - 1 == -1:
                icon = pokemon.get_type_by_id(i - 1).get_none_image()
            button = ButtonIcon(400-132-16 + (i//10)*34, 40 + (i%10) * 16, 32, 16, icon, command=lambda type_in=i-1: self.__close_menus(type_in))

            if i < 10:
                self.__buttons_t2[0].append(button)
            else:
                self.__buttons_t2[1].append(button)

        self.__col = 0

        self.__menu_1 = False
        self.__menu_2 = False

    def get_value(self):
        return self.__types

    def __open_menu_T1(self):
        self.__menu_1 = True
        self.__selected_button = 0

    def __open_menu_T2(self):
        self.__menu_2 = True
        self.__selected_button = 0

    def __close_menus(self, selected_type):
        if self.__menu_1:
            self.__types[0] = selected_type
        elif self.__menu_2:
            self.__types[1] = selected_type
        self.__selected_button = 0
        self.__col = 0
        self.__menu_1 = False
        self.__menu_2 = False

    def is_type_menu_opened(self):
        return self.__menu_1 or self.__menu_2

    def is_left_menu_opened(self):
        return self.__menu_1

    def is_right_menu_opened(self):
        return self.__menu_2

    def render(self, screen: pygame.Surface, no_cursor=False):
        render_overlay(screen)

        text.draw_aligned_text(self._title, screen.get_width() / 2, 12, screen, pygame.font.Font("res/pkmndpb.ttf", 24), color=(255, 255, 255))

        if not (self.__menu_1 or self.__menu_2):
            type_img_1 = None
            if pokemon.get_type_by_id(self.__types[0]).get_type() != -1:
                type_img_1 = pokemon.get_type_by_id(self.__types[0]).get_type_image()
            else:
                type_img_1 = pokemon.get_type_by_id(self.__types[0]).get_none_image()
            type_img_2 = None
            if pokemon.get_type_by_id(self.__types[1]).get_type() != -1:
                type_img_2 = pokemon.get_type_by_id(self.__types[1]).get_type_image()
            else:
                type_img_2 = pokemon.get_type_by_id(self.__types[1]).get_none_image()

            # types
            screen.blit(type_img_1, (100, 104))
            screen.blit(type_img_2, (400-132, 104))

            i = 0
            while i < len(self.__buttons_t):
                self.__buttons_t[i].render(screen)
                if not no_cursor and i == self.__selected_button:
                    self.__buttons_t[i].render_cursor(screen, False, 2)
                i += 1

        if self.__menu_1:
            for j in range(len(self.__buttons_t1)):
                i = 0
                while i < len(self.__buttons_t1[j]):
                    self.__buttons_t1[j][i].render(screen)
                    if not no_cursor and i == self.__selected_button and j == self.__col:
                        self.__buttons_t1[j][i].render_cursor(screen, j == 1, 1)
                    i += 1
        if self.__menu_2:
            for j in range(len(self.__buttons_t2)):
                i = 0
                while i < len(self.__buttons_t2[j]):
                    self.__buttons_t2[j][i].render(screen)
                    if not no_cursor and i == self.__selected_button and j == self.__col:
                        self.__buttons_t2[j][i].render_cursor(screen, j == 1, 1)
                    i += 1

    def input(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if not (self.__menu_1 or self.__menu_2):
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    if self.__selected_button == 0:
                        self.__selected_button = 1
                    else:
                        self.__selected_button = 0
                elif event.key == pygame.K_RETURN:
                    self.__buttons_t[self.__selected_button].execute()
            # mini menu input
            else:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    if self.__col >= 1:
                        self.__col = 0
                    else:
                        self.__col = 1
                elif event.key == pygame.K_UP:
                    if self.__menu_1:
                        self.move_cursor_up(self.__buttons_t1[self.__col])
                    elif self.__menu_2:
                        self.move_cursor_up(self.__buttons_t2[self.__col])
                elif event.key == pygame.K_DOWN:
                    if self.__menu_1:
                        self.move_cursor_down(self.__buttons_t1[self.__col])
                    elif self.__menu_2:
                        self.move_cursor_down(self.__buttons_t2[self.__col])
                elif event.key == pygame.K_RETURN:
                    if self.__menu_1:
                        self.__buttons_t1[self.__col][self.__selected_button].execute()
                    elif self.__menu_2:
                        self.__buttons_t2[self.__col][self.__selected_button].execute()

    def move_cursor_up(self, buttons):
        if self.__selected_button - 1 >= 0:
            self.__selected_button -= 1
        else:
            self.__selected_button = len(buttons)-1

    def move_cursor_down(self, buttons):
        if self.__selected_button + 1 < len(buttons):
            self.__selected_button += 1
        else:
            self.__selected_button = 0
