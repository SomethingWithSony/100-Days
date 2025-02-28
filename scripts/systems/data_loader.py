import json

# Load item data from JSON file
with open("json/items.json", "r") as file:
    ITEM_DATA = json.load(file)