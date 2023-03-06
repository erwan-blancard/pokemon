import pygame

import pokemon_types.rock
"""
from pokemon_types import *
import sys
sys.path.insert(0, 'pokemon_types')"""


ptype = pokemon_types.rock.Rock()
pygame.image.save(ptype.get_type_image(), "test.png")
