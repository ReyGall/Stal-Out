import random
import time
import json
import sqlite3
from pathlib import Path

P = Path(__file__).parent
data_F = P.parent/"data"
db_path = data_F / "database.db"
save_path = data_F / "save.json"

con = sqlite3.connect(db_path)
c = con.cursor()

def load_game():
     
            global inventory

            with open(save_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                inventory = data["player"]["inventory"]

load_game()

def save_game():
            
            global inventory

            data = {
                "player": {
                    "location": 1,
                    "inventory": inventory
                }
            }
            with open(save_path, "w") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)



current_location = 1
debug_mode = False



while True:
    print ("Enter command")
    user_input = input().strip().lower()

    if "start raid" in user_input:
        print("enter raid time in minutes from 1 to 360")
        raid_time = input()
        print("Raid Started")
        temp_loot = []
        raid_time_int = int(raid_time)
        c.execute ("SELECT death_chance FROM locations WHERE id = ?", (current_location,))
        death_chance_inc = c.fetchone() 
        death_chance = death_chance_inc [0] * 0.01

        for i in range(raid_time_int):
            if not debug_mode:
                for second in range(60, 0, -10):
                    print(f"Time left: {second}s...")
                    time.sleep(10)

            c.execute ("SELECT * FROM loot WHERE location_id = ?", (current_location,))
            loot_list = c.fetchall()
            for item in loot_list:
                chance = item [5] / 100
                if random.random() < chance:
                    temp_loot.append(item[0])
                    print(f"You found: {item[0]}")

            player_alive = random.random() > death_chance
        if player_alive == True:
            print ("Raid Success")
            inventory.extend(temp_loot)
            temp_loot = []
            save_game()

        else:
            print("You Died")
            temp_loot = []
        
    item_count = {}

    for item in inventory:
        if item in item_count:
            item_count[item]+= 1
        else:
            item_count[item] = 1

    if "inventory" in user_input:
        for item, count in item_count.items():
            print(f"{item} x{count}")

