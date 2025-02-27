import pygame
import math
from scripts import settings
from scripts.items import Weapon, Consumable, Resource

from scripts.data_loader import ITEM_DATA

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

def create_item(item_type, item_name, quantity=1, pos=(0, 0)):
    # Get item data from the JSON file
    item_info = ITEM_DATA[item_type][item_name]
    
    # Create the appropriate item object
    if item_type == "Weapons":
        return Weapon(
            name=item_name,
            damage=item_info["Damage"],
            range=item_info["Range"],
            attack_speed=1.0,  # You can add this to the JSON file if needed
            quantity=quantity,
            pos=pos
        )
    elif item_type == "Consumables":
        return Consumable(
            name=item_name,
            quantity=quantity,
            health_restore=item_info["HealthRestore"],
            hunger_restore=item_info["HungerRestore"],
            pos=pos
        )
    elif item_type == "Resources":
        return Resource(
            name=item_name,
            quantity=quantity,
            pos=pos
        )
    else:
        raise ValueError(f"Unknown item type: {item_type}")
    
#knife = create_item("Weapons", "Knife", quantity=1, pos=(100, 100))


def check_collision(player, item):
    player_rect = pygame.Rect(player.pos_x, player.pos_y, player.width, player.height)
    item_rect = pygame.Rect(item.pos_x, item.pos_y, item.image.get_width(), item.image.get_height())
    return player_rect.colliderect(item_rect)