import pygame
from scripts import settings
from scripts.player import player
from scripts.world import world
from scripts.systems.physics import Physics
from scripts.systems.renderer import Renderer

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("100 Days")
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        self.clock = pygame.Clock()
        self.running = True
        
        self.status = "Game Loop" # Game status responsable of choosing wich "menu" to display
        
        # Initialize game objects
        self.world = world.World(100, 100, settings.WIDTH, settings.HEIGHT, self) # Creates world 
        self.player = player.Player(self) # Initializes the player
        self.items = []  # Array to hold items in the game world
        
        # Initialize game systems
        self.renderer = Renderer(self.screen)  # Renderer system
        self.physics = Physics()  # Physics system

        # Mouse position and ...
        self.mx, self.my = 0, 0 
        self.current_square = [0, 0] 
        


    def events(self):
        """Handle game events."""
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
      # Remember 
      # First Check Colisions then movement
      self.physics.player_collisions_with_structures(self.player)
      
      self.player.update()
      
      
      
    def renders(self):
      self.renderer.render_player(self.player)
      self.renderer.render_world(self.world)    
        
    def main_menu(self):
        """Render the main menu."""
        self.screen.fill((50, 50, 50))
        self.events()
        pygame.display.flip()
        self.clock.tick(settings.FPS)

    def game_loop(self):
        """Run the main game loop."""
        self.screen.fill(settings.BLACK)
        self.mx, self.my = pygame.mouse.get_pos()
        
        self.events()
        self.updates()
        self.renders()

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
