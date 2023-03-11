import pokemon
from pokemon_maker.sub_menu import *
from pokemon_maker.sub_menu_types import SubMenuTypes
from ui.text_box import TextBox


class SubMenuAttacks(SubMenu):

    def __init__(self, attack_types: list, attack_names: list):
        super().__init__("", "Changer les attaques:")
        self.__attack_types = attack_types
        self.__attack_names = attack_names

        self.__types_menu = SubMenuTypes(self.__attack_types, title="")
        self.__types_menu_focus = False
        self.__attack_name_right_focus = False

    def render(self, screen: pygame.Surface):
        self.__types_menu.render(screen, no_cursor=not self.__types_menu_focus)
        text.draw_aligned_text(self._title, screen.get_width() / 2, 12, screen, pygame.font.Font("res/pkmndpb.ttf", 24), color=(255, 255, 255))
        # attack names
        for i in range(2):
            color = (155, 155, 155)
            desc = "Description indisponible."
            if pokemon.attack_exists(self.__attack_names[i], self.__attack_types[i]):
                color = (60, 255, 60)
                desc = pokemon.get_attack_by_type_and_name(self.__attack_names[i], self.__attack_types[i]).get_desc()
            if i == self.__attack_name_right_focus:
                color = (255, 255, 255)
            if (not self.__types_menu.is_left_menu_opened() and i == 0) or (not self.__types_menu.is_right_menu_opened() and i == 1):
                text.draw_aligned_text(self.__attack_names[i]+"_", 100 + 16 + i * 168, 132, screen, pygame.font.Font("res/pkmndpb.ttf", 12), color=color)
            text_box = TextBox(desc, 100 + 16 + (i * 168) - 64, 132+18, 128, font=pygame.font.Font("res/pkmndpb.ttf", 12))
            text_box.render(screen, (255, 255, 255))

    def input(self, event: pygame.event.Event):
        if self.__types_menu_focus:
            self.__types_menu.input(event)

        if event.type == pygame.KEYDOWN:
            if not self.__types_menu.is_type_menu_opened():
                # switch button focus
                if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    if self.__types_menu_focus:
                        self.__types_menu_focus = False
                    else:
                        self.__types_menu_focus = True
                # switch attack focus
                elif not self.__types_menu_focus and (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                    if self.__attack_name_right_focus:
                        self.__attack_name_right_focus = False
                    else:
                        self.__attack_name_right_focus = True
                # edit attack names
                elif not self.__types_menu_focus:
                    value = self.__attack_names[self.__attack_name_right_focus]
                    if event.key == pygame.K_BACKSPACE:
                        if value == "---":
                            value = ""
                        else:
                            value = value[:-1]
                    else:
                        key = pygame.key.name(event.key)
                        if key in "abcdefghijklmnopqrstuvwxyz":
                            if len(value) <= 20:
                                if value == "---":
                                    value = ""
                                value += key.upper()
                        elif key == "space":
                            if len(value) <= 20:
                                if value == "---":
                                    value = ""
                                value += " "
                        elif key in ["[0]", "[1]", "[2]", "[3]", "[4]", "[5]", "[6]", "[7]", "[8]", "[9]"]:
                            if len(value) <= 20:
                                if value == "---":
                                    value = ""
                                value += key[1:2]
                    self.__attack_names[self.__attack_name_right_focus] = value
