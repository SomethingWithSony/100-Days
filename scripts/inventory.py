from scripts.items import *

class Inventory:
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.items = []

    def add_item(self, item):
        # Check if the item is stackable and already exists in the inventory
        if item.stackable:
            for existing_item in self.items:
                if existing_item.name == item.name:
                    existing_item.quantity += item.quantity
                    return
        # If not stackable or not found, add the item
        if len(self.items) < self.capacity:
            self.items.append(item)
        else:
            print("Inventory is full!")

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)

    def use_item(self, item, player):
        if isinstance(item, Consumable):
            item.use(player)
        elif isinstance(item, Weapon):
            player.equip_weapon(item)

    def __repr__(self):
        return "\n".join(str(item) for item in self.items)