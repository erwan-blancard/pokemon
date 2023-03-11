import pygame
import game_state
import pokemon
import pokemon_parser
import text
from menu import MenuState
from in_game import InGameState
from pokedex import PokedexState
from pokemon_maker.pokemon_maker import PokemonMakerState


pygame.init()
if not pygame.font.get_init():
    pygame.font.init()


# load pokémon list in package pokemon
pokemon_parser.load_pokemons()

# sets first pokémon unlocked
if not pokemon_parser.pokemon_in_pokedex(pokemon.POKEMONS[0].get_name()):
    pokemon_parser.add_to_pokedex(pokemon.POKEMONS[0].get_name())

screen = pygame.display.set_mode((400*2, 240*2))    # 400x240
pygame.display.set_caption("Pokémon  |  LaPlateforme Édition")
pygame.display.set_icon(pygame.image.load("res/icon.png"))

# main surface where everything should be drawed
# the surface will be upscaled to match the window's size
game_surface = pygame.Surface((400, 240))

game_state.state = 0
state = MenuState()

fullscreen = False


def enable_fullscreen():
    global fullscreen
    pygame.display.set_mode(flags=pygame.FULLSCREEN)
    fullscreen = True


def disable_fullscreen():
    global screen
    global fullscreen
    screen = pygame.display.set_mode((400 * 2, 240 * 2))
    fullscreen = False


running = True

while running:

    # Update state
    if game_state.update_pending:
        if game_state.state == game_state.MENU:
            state = MenuState()
        elif game_state.state == game_state.INGAME:
            state = InGameState()
        elif game_state.state == game_state.POKEDEX:
            state = PokedexState()
        elif game_state.state == game_state.POKEMON_MAKER:
            state = PokemonMakerState()
        else:
            print("Invalid state id:", game_state.state)
        game_state.update_pending = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
            if fullscreen:
                disable_fullscreen()
            else:
                enable_fullscreen()
        state.input(event)

    state.update()

    game_surface.fill((240, 255, 240))

    state.render(game_surface)

    if game_state.state == game_state.MENU:
        current_win_mode = "Fenêtré"
        if fullscreen:
            current_win_mode = "Fullscreen"
        current_win_mode += ' (F11)'
        text.draw_text(current_win_mode, 400 - 4 - text.font().size(current_win_mode)[0], 240 - text.font().size(current_win_mode)[1], game_surface)

    screen.blit(pygame.transform.scale(game_surface, (screen.get_width(), screen.get_height())), (0, 0))

    pygame.display.flip()
