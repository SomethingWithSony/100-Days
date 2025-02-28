import pygame
from scripts import settings
from scripts.utils import load_image

class World:
    def __init__(self, grid_length_x, grid_length_y, width, height, game):
        self.grid_length_x = grid_length_x
        self.grid_length_y = grid_length_y
        self.width = width
        self.height = height
        self.game = game
        self.world = self.generate_world()
        self.structure_images = {
            "wall": load_image("wall.png"),
        }

    def generate_world(self):
        """Generate the game world."""
        return [[self.grid_to_world(x, y) for y in range(self.grid_length_y)] for x in range(self.grid_length_x)]

    def grid_to_world(self, grid_x, grid_y):
        """Convert grid coordinates to world coordinates."""
        rect = [
            (grid_x * settings.TILE_SIZE, grid_y * settings.TILE_SIZE),
            (grid_x * settings.TILE_SIZE + settings.TILE_SIZE, grid_y * settings.TILE_SIZE),
            (grid_x * settings.TILE_SIZE + settings.TILE_SIZE, grid_y * settings.TILE_SIZE + settings.TILE_SIZE),
            (grid_x * settings.TILE_SIZE, grid_y * settings.TILE_SIZE + settings.TILE_SIZE),
        ]
        return {
            "grid": [grid_x, grid_y],
            "rect": rect,
            "structure": "",
        }

    def is_inside_rect(self, rect):
        """Check if the mouse is inside a rectangle."""
        offset = 1
        x_min = min(p[0] + offset for p in rect)
        x_max = max(p[0] - offset for p in rect)
        y_min = min(p[1] + offset for p in rect)
        y_max = max(p[1] - offset for p in rect)
        return (x_min <= self.game.mx <= x_max) and (y_min <= self.game.my <= y_max)
    
    def events(self, event):
        """Handle world-related events."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            self.world[self.game.current_square[0]][self.game.current_square[1]]["structure"] = "wall"