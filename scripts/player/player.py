import pygame
from scripts.utils import load_image, normalize_vector
from scripts import settings
from scripts.items.items import Weapon
from scripts.player.build_hud import BuildHUD
from scripts.player.inventory import Inventory

class Player:
    def __init__(self, game):
        self.game = game
        self.move_speed = settings.PLAYER_SPEED
        self.movement = [0, 0]
        self.image = load_image("player.png")
        self.player_rect = self.image.get_rect(center=(self.image.get_width() // 2, self.image.get_height() // 2))
        
        self.pos_x = 0
        self.pos_y = 0
        
        self.inventory = Inventory()
        self.equipped_weapon = None
        
        self.health = 100
        self.hunger = 100
        
        self.build_hud = BuildHUD(game) 
        self.build_mode = False

        
    def equip_weapon(self, weapon):
        if isinstance(weapon, Weapon):
            self.equipped_weapon = weapon
            print(f"Equipped {weapon.name}")
        else:
            print("Cannot equip this item.")

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            print("Player has died.")
            
    

    def update(self):
        """Update player position."""
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
      