import pygame

import text
from pokemon import Pokemon

HP_BOX_LAYOUT: pygame.Surface = None
HP_BAR_COLORS: pygame.Surface = None

# x, y, width, height
_BAR_DIMS = (35*2, 13*2, 48*2, 3*2)


def _check_images():
    global HP_BOX_LAYOUT
    global HP_BAR_COLORS
    if HP_BOX_LAYOUT is None:
        hp_box_img = pygame.image.load("res/hp_box.png")
        HP_BOX_LAYOUT = pygame.Surface((88, 29), pygame.SRCALPHA)
        HP_BOX_LAYOUT.blit(hp_box_img, (0, 0))
        HP_BOX_LAYOUT = pygame.transform.scale(HP_BOX_LAYOUT, (HP_BOX_LAYOUT.get_width()*2, HP_BOX_LAYOUT.get_height()*2))
        # pygame.image.save(HP_BOX_LAYOUT, "test/layout.png")
    if HP_BAR_COLORS is None:
        hp_box_img = pygame.image.load("res/hp_box.png")
        HP_BAR_COLORS = pygame.Surface((3, 3))
        HP_BAR_COLORS.blit(hp_box_img, (0, -29))
        # pygame.image.save(HP_BAR_COLORS, "test/colors.png")


class HpBox:

    def __init__(self, pkmn: Pokemon, x: int, y: int):
        _check_images()
        self.x = x
        self.y = y
        self.__pkmn = pkmn

    def get_bar(self):
        # green
        index = 0
        # red
        if self.__pkmn.get_current_hp() / self.__pkmn.get_hp() <= 1/3:
            index = 2
        # orange
        elif self.__pkmn.get_current_hp() / self.__pkmn.get_hp() <= 2/3:
            index = 1
        bar = pygame.Surface((1, 3))
        bar.blit(HP_BAR_COLORS, (-index, 0))
        bar = pygame.transform.scale(bar, (int(round(_BAR_DIMS[2]*(self.__pkmn.get_current_hp() / self.__pkmn.get_hp()))), _BAR_DIMS[3]))
        return bar

    def render(self, screen: pygame.Surface):
        screen.blit(HP_BOX_LAYOUT, (self.x, self.y))
        text.draw_text(self.__pkmn.get_name(), self.x + 8, self.y + 6, screen)
        # types
        if self.__pkmn.get_types()[1].get_type() == -1:
            screen.blit(self.__pkmn.get_types()[0].get_type_image(), (
                self.x + HP_BOX_LAYOUT.get_width() - 8 - self.__pkmn.get_types()[0].get_type_image().get_width(), self.y + 6))
        else:
            screen.blit(self.__pkmn.get_types()[0].get_type_image(), (
                self.x + HP_BOX_LAYOUT.get_width() - 8 - 38 - self.__pkmn.get_types()[0].get_type_image().get_width(),
                self.y + 6))
            screen.blit(self.__pkmn.get_types()[1].get_type_image(), (
                self.x + HP_BOX_LAYOUT.get_width() - 8 - self.__pkmn.get_types()[1].get_type_image().get_width(),
                self.y + 6))
        str_curr_hp = str(self.__pkmn.get_current_hp())
        for c in range(len(str(self.__pkmn.get_current_hp())), 3):
            str_curr_hp = " " + str_curr_hp
        str_hp = str(self.__pkmn.get_hp())
        for c in range(len(str(self.__pkmn.get_hp())), 3):
            str_hp = " " + str_hp
        text.draw_text(str_curr_hp+"/"+str_hp, self.x + 64*2, self.y + 18*2, screen)
        text.draw_text("LV: "+str(self.__pkmn.get_level()), self.x + 8, self.y + 18*2, screen)
        bar = self.get_bar()
        screen.blit(bar, (self.x + _BAR_DIMS[0], self.y + _BAR_DIMS[1]))
