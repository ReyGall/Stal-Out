import json

def load_game(save_path):

            with open(save_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                inventory = data["player"]["inventory"]
                money = data["player"]["money"]

            return inventory, money

def save_game(save_path, inventory, money):

            data = {
                "player": {
                    "location": 1,
                    "inventory": inventory,
                    "money": money
                }
            }
            with open(save_path, "w") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

