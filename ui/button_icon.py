from ui.button_base import *


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
