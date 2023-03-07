import pokemon
import pokemon_parser

# pokemon_parser.add_pokemon("Pikachu", 8, 28, 0, 0, -1)
pokemon_parser.load_pokemons()
print(pokemon.POKEMONS)

pokemon_parser.add_to_pokedex("Pikachu")
pokemon_parser.add_to_pokedex("Pichu")
"""import pygame
import game_state
import pokemon_parser
from menu import MenuState
from in_game import InGameState


pygame.init()
if not pygame.font.get_init():
    pygame.font.init()

screen = pygame.display.set_mode((576, 760))    # 400x240
pygame.display.set_caption("Pokémon | LaPlateforme Edition")
pygame.display.set_icon(pygame.image.load("res/icon.png"))

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

    screen.fill((30, 30, 30))

    state.render(screen)

    pygame.display.flip()
"""