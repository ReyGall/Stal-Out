import sqlite3
from pathlib import Path
from Raid import start_raid
from inventory import show_inventory
from save import load_game
from save import save_game
from Merchants.fence import fence_merchant

P = Path(__file__).parent
data_F = P.parent/"data"
db_path = data_F / "database.db"
save_path = data_F / "save.json"

con = sqlite3.connect(db_path)
c = con.cursor()



inventory, money = load_game(save_path,)


current_location = 1
debug_mode = True



while True:
    print ("Enter command")
    user_input = input().strip().lower()

    if "start raid" in user_input:
        inventory = start_raid(inventory, current_location, debug_mode, c, save_path)

    elif "inventory" in user_input:
        show_inventory(inventory, c, money)

    elif "fence" in user_input:
        inventory, earned_money = fence_merchant(c, inventory)
        money += earned_money
        save_game(save_path, inventory, money)
        
