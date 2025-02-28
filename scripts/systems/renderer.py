import pygame
from scripts import settings

class Renderer:
    def __init__(self, screen):
        self.screen = screen

    def render_item(self, item):
        """Render an item on the screen."""
        self.screen.blit(item.image, (item.pos_x, item.pos_y))
        
    def render_player(self, player):
        """Render the player on the screen."""
        self.screen.blit(player.image, player.player_rect)
        
    def render_world(self,world):
        """Render the world."""
        for x in range(world.grid_length_x):
            for y in range(world.grid_length_y):
                square = world.world[x][y]["rect"]
                if structure := world.world[x][y]["structure"]:
                    self.screen.blit(world.structure_images[structure], square[0]) # Change this to work with structure json
                elif world.is_inside_rect(square):
                    pygame.draw.rect(self.screen, settings.WHITE, pygame.Rect(square[0][0], square[0][1], settings.TILE_SIZE, settings.TILE_SIZE), 1)
                    world.game.current_square = [x, y]