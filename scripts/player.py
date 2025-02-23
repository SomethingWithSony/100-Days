import pygame
from scripts.utils import load_image, normalize_vector
from scripts import settings
from scripts.items import Weapon
from scripts.build_hud import BuildHUD

class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def add_item(self, item):
        if len(self.items) < self.capacity:
            self.items.append(item)
        else:
            print("Inventory full!")

    def remove_item(self, item):
        self.items.remove(item)

    def use_item(self, item):
        if item in self.items:
            # Handle item usage (e.g., consume food, equip weapon)
            print(f"Used {item.name}")
            self.remove_item(item)
            
class Player:
    def __init__(self, game):
        self.game = game
        self.move_speed = settings.PLAYER_SPEED
        self.movement = [0, 0]
        self.player = load_image("player.png")
        self.player_rect = self.player.get_rect(center=(self.player.get_width() // 2, self.player.get_height() // 2))
        self.pos_x = 0
        self.pos_y = 0
        
        self.weapon = Weapon("Sword", 10, 50, 1.0)  # Temp
        self.attack_cooldown = 0
        
        self.inventory = Inventory(capacity=10)  # Temp
        
        self.build_hud = BuildHUD(game) #
        self.build_mode = False


    def render(self):
        """Render the player on the screen."""
        self.game.screen.blit(self.player, self.player_rect)

    def update(self):
        """Update player position and handle collisions."""
        self.collisions()
        self.move()

    def events(self, event):
      """Handle player input events."""
      
      if self.build_mode:
            self.build_hud.events(event)
            
      if event.type == pygame.KEYDOWN:
          if event.key == settings.MOVEMENT_KEYS["up"]:
              self.movement[1] = -1
          elif event.key == settings.MOVEMENT_KEYS["down"]:
              self.movement[1] = 1
          elif event.key == settings.MOVEMENT_KEYS["left"]:
              self.movement[0] = -1
          elif event.key == settings.MOVEMENT_KEYS["right"]:
              self.movement[0] = 1
              
          if event.key == pygame.K_b:
                self.toggle_build_mode()
        
              
      if event.type == pygame.KEYUP:
          if event.key in (settings.MOVEMENT_KEYS["up"], settings.MOVEMENT_KEYS["down"]):
              self.movement[1] = 0
          elif event.key in (settings.MOVEMENT_KEYS["left"], settings.MOVEMENT_KEYS["right"]):
              self.movement[0] = 0
              
    def collisions(self):
        """Check and resolve collisions with walls."""
        player_half_width = self.player_rect.width // 2
        player_half_height = self.player_rect.height // 2

        # Future positions
        next_x = self.pos_x + self.movement[0] * self.move_speed
        next_y = self.pos_y + self.movement[1] * self.move_speed

        # Create future rects for X and Y movement
        future_rect_x = pygame.Rect(
            next_x - player_half_width, self.pos_y - player_half_height,
            self.player_rect.width, self.player_rect.height
        )
        future_rect_y = pygame.Rect(
            self.pos_x - player_half_width, next_y - player_half_height,
            self.player_rect.width, self.player_rect.height
        )

        # Check for collisions with walls
        self.check_collision(future_rect_x, "x")
        self.check_collision(future_rect_y, "y")

    def check_collision(self, future_rect, axis):
        """Check for collisions with walls on a specific axis."""
        for x in range(self.game.world.grid_length_x):
            for y in range(self.game.world.grid_length_y):
                if self.game.world.world[x][y]["structure"] == "wall":
                    wall_rect = pygame.Rect(
                        x * settings.TILE_SIZE, y * settings.TILE_SIZE,
                        settings.TILE_SIZE, settings.TILE_SIZE
                    )
                    if future_rect.colliderect(wall_rect):
                        self.resolve_collision(axis, wall_rect)

    def resolve_collision(self, axis, wall_rect):
        """Resolve collision on a specific axis."""
        if axis == "x":
            if self.movement[0] > 0:  # Moving right
                self.pos_x = wall_rect.left - self.player_rect.width // 2
            elif self.movement[0] < 0:  # Moving left
                self.pos_x = wall_rect.right + self.player_rect.width // 2
            self.movement[0] = 0
        elif axis == "y":
            if self.movement[1] > 0:  # Moving down
                self.pos_y = wall_rect.top - self.player_rect.height // 2
            elif self.movement[1] < 0:  # Moving up
                self.pos_y = wall_rect.bottom + self.player_rect.height // 2
            self.movement[1] = 0

    def move(self):
        """Move the player based on input."""
        if self.movement[0] != 0 and self.movement[1] != 0:
            self.movement = normalize_vector(self.movement)
        self.pos_x += self.movement[0] * self.move_speed
        self.pos_y += self.movement[1] * self.move_speed
        self.player_rect.center = (self.pos_x, self.pos_y)

    def attack(self):
      if self.attack_cooldown <= 0:
          # Get mouse position
          mouse_x, mouse_y = pygame.mouse.get_pos()
          # Calculate attack direction
          direction = (mouse_x - self.pos_x, mouse_y - self.pos_y)
          # Normalize direction
          direction = normalize_vector(direction)
          # Check for enemies in range
          # for enemy in self.game.enemies:
          #     if self.weapon.range >= distance(self.pos_x, self.pos_y, enemy.pos_x, enemy.pos_y):
          #         self.weapon.attack(enemy)
          self.attack_cooldown = self.weapon.attack_speed * settings.FPS  # Cooldown in frames
      else:
          self.attack_cooldown -= 1
    
    def toggle_build_mode(self):
        self.build_mode = not self.build_mode
    # Pick up items on collision   
    # def check_item_pickup(self):
    #   for item in self.game.items:
    #       if distance(self.pos_x, self.pos_y, item.pos_x, item.pos_y) < settings.TILE_SIZE:
    #           self.inventory.add_item(item)
    #           self.game.items.remove(item)
      