import sqlite3
import json
from pathlib import Path
from Raid import start_raid
from inventory import show_inventory
from save import load_game
from save import save_game
from Merchants.fence import fence_merchant
from Merchants.Gear_Merchant import buy_Armor

P = Path(__file__).parent
data_F = P.parent/"data"
if not data_F.exists():
    data_F.mkdir(parents=True, exist_ok=True)
db_path = data_F / "database.db"
save_path = data_F / "save.json"
if not save_path.exists():
    initial_save = {
    "player": {
        "location": 1,
        "inventory": [],
        "money": 0,
        "owned_armor": []
    }
    }
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(initial_save, f, indent=4, ensure_ascii=False)

con = sqlite3.connect(db_path)
c = con.cursor()
c.execute("PRAGMA foreign_keys = ON")


inventory, money, owned_armor, current_location = load_game(save_path)

current_location = 1
debug_mode = True

actions = ["start raid", "inventory", "fence", "armor merchant"]

while True:

    print ("Choose command\n")
    for i, command in enumerate (actions):
        print (f"[{i + 1}] {command}")



    user_input = input().lower().strip()

    if user_input.isdigit():
        choise = int(user_input) - 1
        if 0 <= choise < len(actions):
            selected_action = actions[choise]
            
            if choise == 0:
                inventory = start_raid(inventory, current_location, debug_mode, c, save_path, money)

            elif choise == 1:
                show_inventory(inventory, c, money, owned_armor)

            elif choise == 2:
                inventory, earned_money = fence_merchant(c, inventory)
                money += earned_money
                save_game(save_path, inventory, money, current_location)

            elif choise == 3:
                inventory, money, owned_armor = buy_Armor(c, inventory, money, owned_armor)
                save_game(save_path, inventory, money, owned_armor, current_location)

    