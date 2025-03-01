from scripts.utils import load_image
from   scripts.systems.data_loader import ITEM_DATA

class Item:
    def __init__(self,player, name,  quantity=1, stackable=True, is_in_inventory=False, pos=(0,0)):
        self.player = player
        
        self.name = name
        self.quantity = quantity
        self.stackable = stackable  # Whether the item can stack in the inventory
        
        self.is_in_inventory = is_in_inventory
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        
        # self.image = load_image("items/" + name + ".png")
        self.image = load_image("wall.png")

    def __repr__(self):
        return f"{self.name} (x{self.quantity})" if self.stackable else self.name
      
class Weapon(Item):
    def __init__(self,player, name, damage, range, attack_speed, quantity=1, pos=(0, 0)):
        super().__init__(player, name, quantity=quantity, stackable=False, pos=pos)  # Weapons are not stackable
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
 
        
# Auc Functions
def create_item(player, item_type, item_name, quantity=1, pos=(0, 0)):
    # Get item data from the JSON file
    item_info = ITEM_DATA[item_type][item_name]
    
    # Create the appropriate item object
    if item_type == "Weapons":
        return Weapon(
            player=player,
            name=item_name,
            damage=item_info["Damage"],
            range=item_info["Range"],
            attack_speed=1.0,  # Put in json file
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
    


