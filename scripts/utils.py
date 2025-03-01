import pygame
import math
from scripts import settings

import os

BASE_IMG_PATH = 'assets/images/'

def load_image(path):
    """Load an image from the assets folder."""
    try:
        img = pygame.image.load(BASE_IMG_PATH + path).convert()
        img.set_colorkey(settings.BLACK)  # Set black as the transparent color
        return img
    except FileNotFoundError:
        print(f"Error: Image not found at {BASE_IMG_PATH + path}")
        return pygame.Surface((settings.TILE_SIZE, settings.TILE_SIZE))  # Return a placeholder surface

def normalize_vector(vector):
    """Normalize a 2D vector."""
    magnitude = math.hypot(vector[0], vector[1])
    if magnitude == 0:
        return vector
    return [vector[0] / magnitude, vector[1] / magnitude]



