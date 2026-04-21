import sqlite3
from pathlib import Path
from Raid import start_raid
from inventory import show_inventory
from save import load_game
from save import save_game
from Merchants.fence import fence_merchant
from Merchants.Gear_Merchant import Buy_Armor

P = Path(__file__).parent
data_F = P.parent/"data"
db_path = data_F / "database.db"
save_path = data_F / "save.json"

con = sqlite3.connect(db_path)
c = con.cursor()
c.execute("PRAGMA foreign_keys = ON")


inventory, money = load_game(save_path,)

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
                show_inventory(inventory, c, money)

            elif choise == 2:
                inventory, earned_money = fence_merchant(c, inventory)
                money += earned_money
                save_game(save_path, inventory, money)

            elif choise == 3:
                Buy_Armor(c, inventory, money)

    