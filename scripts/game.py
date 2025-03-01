import pygame
from scripts import settings
from scripts.player import player
from scripts.world import world
from scripts.systems.physics import Physics
from scripts.systems.renderer import Renderer
from scripts.items.items import create_item

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("100 Days")
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.status = "Main Menu" # Game status responsable of choosing wich "menu" to display
        
        # Initialize game objects
        self.world = world.World(100, 100, settings.WIDTH, settings.HEIGHT, self) # Creates world 
        self.player = player.Player(self) # Initializes the player
        self.items = []  # Array to hold items in the game world
        self.items.append(create_item(self.player,"Weapons", "Knife", quantity=1, pos=(100, 100)))# Test Item 
        
        # Initialize game systems
        self.renderer = Renderer(self.screen)  # Renderer system
        self.physics = Physics()  # Physics system

        # Mouse position and ...
        self.mx, self.my = 0, 0 
        self.current_square = [0, 0] 
        
    def events(self):
        """ Should only handle game events """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            self.player.events(event)
            self.world.events(event)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:
                    self.status = "Main Menu"
                elif event.key == pygame.K_k:
                    self.status = "Game Loop"

    def updates(self):
        """ Should only update game state """
        # First, check collisions
        self.physics.player_collisions_with_structures(self.player)
        for item in self.items:
            if self.physics.check_collision_player_item(self.player, item):
                self.player.hovering_item = item
            else:
                self.player.hovering_item = None
            
        # Then, update player and other game objects
        self.player.update()
      
    def renders(self):
        """ Should only render game objects """
        self.screen.fill(settings.BLACK) # Clear the screen
        
        # Render the world, items, and player
        self.renderer.render_world(self.world) 
        for item in self.items:
            self.renderer.render_item(item)
        
        self.renderer.render_player(self.player)
            
    def main_menu(self):
        """Render the main menu."""
        self.screen.fill((50, 50, 50))
        self.events()
        pygame.display.flip()
        self.clock.tick(settings.FPS)

    def game_loop(self):
        """Run the main game loop."""
        self.mx, self.my = pygame.mouse.get_pos()
        
        # Handle events, update game state, and render
        self.events()
        self.updates()
        self.renders()

        # Update the display
        pygame.display.flip()
        self.clock.tick(settings.FPS)

    def screen_manager(self):
        """Manage game screens."""
        while self.running:
            if self.status == "Game Loop":
                self.game_loop()
            elif self.status == "Main Menu":
                self.main_menu()
        pygame.quit()
