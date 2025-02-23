class Item:
    def __init__(self, name, quantity=1):
        self.name = name
        self.quantity = quantity

class Weapon(Item):
    def __init__(self,name, damage, range, attack_speed):
        self.name = name
        self.damage = damage
        self.range = range
        self.attack_speed = attack_speed

    def attack(self, target):
        target.take_damage(self.damage)