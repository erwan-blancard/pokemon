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
        # pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height), width=1)
        pass

    def render_cursor(self, screen: pygame.Surface, right=False, offset=0):
        if right:
            screen.blit(pygame.transform.flip(CURSOR, flip_x=True, flip_y=False), (self.x + self.width + offset, self.y + (self.height / 2 - CURSOR.get_height() / 2)))
        else:
            screen.blit(CURSOR, (self.x - CURSOR.get_width() - offset, self.y + (self.height / 2 - CURSOR.get_height() / 2)))

    def execute(self):
        pass
