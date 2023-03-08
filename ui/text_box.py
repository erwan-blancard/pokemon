import pygame

import text


class TextBox:

    def __init__(self, message: str, x, y, lenght, font: pygame.font.Font = text.font()):
        self.message = message
        self.x = x
        self.y = y
        self.__lenght = lenght
        self.__font = font
        self.__lines = []
        self.parse_lines()

    def change_font(self, font: pygame.font.Font):
        self.__font = font
        self.parse_lines()

    def parse_lines(self):
        words = self.message.split()
        lines: list[str] = [""]
        current_line = 0
        for word in words:
            if len(lines[current_line]) != 0 and self.__font.size(lines[current_line])[0] + self.__font.size(word)[0] > self.__lenght:
                current_line += 1
                lines.append("")
            if len(lines[current_line]) != 0:
                lines[current_line] += " "
            lines[current_line] += word

        self.__lines = lines

    def render(self, screen: pygame.Surface):
        char_height = self.__font.size("0")[1]
        for i in range(len(self.__lines)):
            text.draw_text(self.__lines[i], self.x, self.y + char_height*i, screen, self.__font)
