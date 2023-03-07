import pygame
import game_state
import pokemon
import pokemon_parser
from menu import MenuState
from in_game import InGameState


pygame.init()
if not pygame.font.get_init():
    pygame.font.init()

# load pokémon list in package pokemon
pokemon_parser.load_pokemons()

screen = pygame.display.set_mode((400*2, 240*2))    # 400x240
pygame.display.set_caption("Pokémon  |  LaPlateforme Edition")
pygame.display.set_icon(pygame.image.load("res/icon.png"))

# main surface where everything should be drawed
# the surface will be upscaled to match the window's size
game_surface = pygame.Surface((400, 240))

game_state.state = 0
state = MenuState()

running = True

while running:

    # Update state
    if game_state.update_pending:
        if game_state.state == game_state.MENU:
            state = MenuState()
        elif game_state.state == game_state.INGAME:
            state = InGameState()
        else:
            print("Invalid state id:", game_state.state)
        game_state.update_pending = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        state.input(event)

    state.update()

    game_surface.fill((240, 255, 240))

    state.render(game_surface)

    screen.blit(pygame.transform.scale(game_surface, (screen.get_width(), screen.get_height())), (0, 0))

    pygame.display.flip()
