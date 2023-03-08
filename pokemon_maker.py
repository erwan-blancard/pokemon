from game_state import *
from pokemon_types.pokemon_type import *


class PokemonMakerState(GameState):

    def __init__(self):
        super().__init__()

    def update(self):
        super().update()

    def render(self, screen: pygame.Surface):
        super().render(screen)

    def input(self, event: pygame.event.Event):
        super().input(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                set_state(MENU)

"""pokemon_parser.add_pokemon("Pikachu", 35, 13, 0, ELECTR, -1, NORMAL, "CHARGE", ELECTR, "ECLAIR")

pokemon_parser.add_pokemon("Bulbizarre", 45, 15, 0, GRASS, POISON, NORMAL, "CHARGE", GRASS, "BALLE GRAINE")
pokemon_parser.add_pokemon("Herbizarre", 60, 18, 3, GRASS, POISON, NORMAL, "CHARGE", GRASS, "FOUET LIANES")
pokemon_parser.add_pokemon("Florizarre", 80, 21, 8, GRASS, POISON, GRASS, "FOUET LIANES", POISON, "GAZ TOXIC")

pokemon_parser.add_pokemon("Salamèche", 39, 14, 0, FIRE, -1, NORMAL, "GRIFFE", FIRE, "FLAMMECHE")
pokemon_parser.add_pokemon("Reptincel", 58, 17, 4, FIRE, -1, NORMAL, "GRIFFE", FIRE, "CROCS FEU")
pokemon_parser.add_pokemon("Dracaufeu", 78, 22, 7, FIRE, FLYING, DRAGON, "DRACOGRIFFE", FIRE, "INCENDIE")

pokemon_parser.add_pokemon("Magicarpe", 20, 8, 2, WATER, -1, NORMAL, "CHARGE", NORMAL, "CHARGE")
pokemon_parser.add_pokemon("Pichu", 24, 11, 0, ELECTR, -1, NORMAL, "CHARGE", ELECTR, "ECLAIR")

pokemon_parser.load_pokemons()

for pkmn in pokemon.POKEMONS:
    pkmn.print_infos()
    print()
"""