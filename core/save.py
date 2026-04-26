import json

def load_game(save_path):

            with open(save_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                inventory = data["player"]["inventory"]
                money = data["player"]["money"]
                owned_armor = data["player"]["owned_armor"]

            return inventory, money, owned_armor

def save_game(save_path, inventory, money, owned_armor):

            data = {
                "player": {
                    "location": 1,
                    "inventory": inventory,
                    "money": money,
                    "owned armor": owned_armor
                }
            }
            with open(save_path, "w") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

