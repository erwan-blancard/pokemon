import pygame
import text

CURSOR = pygame.image.load("res/cursor.png")


class BaseButton:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def render(self, screen: pygame.Surface):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height), width=1)
        pass

    def render_cursor(self, screen: pygame.Surface, right=False, offset=0):
        if right:
            screen.blit(pygame.transform.flip(CURSOR, flip_x=True, flip_y=False), (self.x + self.width + offset, self.y + (self.height / 2 - CURSOR.get_height() / 2)))
        else:
            screen.blit(CURSOR, (self.x - CURSOR.get_width() - offset, self.y + (self.height / 2 - CURSOR.get_height() / 2)))

    def execute(self):
        pass


class ButtonLabel(BaseButton):

    def __init__(self, label, x, y, width, height, command=None, center_text=True):
        super().__init__(x, y, width, height)
        self.label = label
        self.font = text.get_font(height)
        self.command = command
        self.center_text = center_text

    def render(self, screen: pygame.Surface):
        if self.center_text:
            text.draw_centered_text(self.label, self.x+(self.width/2), self.y+(self.height/2), screen, self.font)
        else:
            text.draw_text(self.label, self.x, self.y + (self.height - self.font.size(self.label)[1])/2, screen, self.font)
        super().render(screen)

    def execute(self):
        if self.command is not None:
            self.command()


class ButtonIcon(BaseButton):

    def __init__(self, x, y, width, height, icon, command=None):
        super().__init__(x, y, width, height)
        self.command = command
        icon = pygame.transform.scale(icon, (self.width, self.height))
        self.icon = icon

    def render(self, screen):
        screen.blit(self.icon, (self.x, self.y))
        super().render(screen)

    def execute(self):
        if self.command is not None:
            self.command()


class TrueFalseButton(BaseButton):

    def __init__(self, x, y, width, height, false_icon: pygame.Surface, true_icon: pygame.Surface, activated=False, false_command=None, true_command=None):
        super().__init__(x, y, width, height)
        self.activated = activated
        self.true_command = true_command
        self.false_command = false_command
        false_icon = pygame.transform.scale(false_icon, (self.width, self.height))
        true_icon = pygame.transform.scale(true_icon, (self.width, self.height))
        self.icons = [false_icon, true_icon]

    def render(self, screen: pygame.Surface):
        img_index = 0
        if self.activated:
            img_index = 1
        screen.blit(self.icons[img_index], (self.x, self.y))
        super().render(screen)

    def execute(self):
        if self.activated:
            self.activated = False
            self.exec_false_command()
        else:
            self.activated = True
            self.exec_true_command()

    def exec_false_command(self):
        if self.false_command is not None:
            self.false_command()

    def exec_true_command(self):
        if self.true_command is not None:
            self.true_command()
