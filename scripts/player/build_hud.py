import pygame
from scripts import settings

class BuildHUD:
    def __init__(self, game):
        self.game = game
        self.structures = ["wall", "door", "fence"]
        self.selected_structure = None

    def render(self):
        for i, structure in enumerate(self.structures):
            text = self.game.font.render(structure, True, settings.WHITE)
            self.game.screen.blit(text, (10, 10 + i * 20))

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.selected_structure = "wall"
            elif event.key == pygame.K_2:
                self.selected_structure = "door"
                
    def place_structure(self, x, y):
      if self.selected_structure:
          self.game.world.world[x][y]["structure"] = self.selected_structure