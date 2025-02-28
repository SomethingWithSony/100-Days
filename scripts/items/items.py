from scripts.utils import load_image

import pygame

class Item:
    def __init__(self, name, player, quantity=1, stackable=True, is_dropped=True, pos=(0,0) ):
        self.name = name
        self.quantity = quantity
        self.stackable = stackable  # Whether the item can stack in the inventory
        
        self.is_dropped = is_dropped
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        
        self.image = load_image("items/" + name + ".png")
        
        self.player = player
        
    # # Render?
    # def render(self):
    #   # if not in inventory render 
    #   pass
    
    # def update(self):
    #   if self.check_colision(self.player, self.item):
    #     # Show press to pickup to player
    #     pass
      
    # def check_collision(player, item):
    #   player_rect = pygame.Rect(player.pos_x, player.pos_y, player.width, player.height) 
    #   item_rect = pygame.Rect(item.pos_x, item.pos_y, item.image.get_width(), item.image.get_height())
    #   return player_rect.colliderect(item_rect)
    
    # Update?
      # Check if coliding with the player?    
      
     

    def __repr__(self):
        return f"{self.name} (x{self.quantity})" if self.stackable else self.name
      
class Weapon(Item):
    def __init__(self, name, damage, range, attack_speed):
        super().__init__(name, quantity=1, stackable=False)  # Weapons are not stackable
        self.damage = damage
        self.range = range
        self.attack_speed = attack_speed

    def attack(self, target):
        target.take_damage(self.damage)
        
class Consumable(Item):
    def __init__(self, name, quantity=1, health_restore=0, hunger_restore=0):
        super().__init__(name, quantity, stackable=True)
        self.health_restore = health_restore
        self.hunger_restore = hunger_restore

    def use(self, player):
        player.health += self.health_restore
        player.hunger += self.hunger_restore
        self.quantity -= 1
        if self.quantity <= 0:
            player.inventory.remove(self)
            
class Resource(Item):
    def __init__(self, name, quantity=1):
        super().__init__(name, quantity, stackable=True)
 
        
