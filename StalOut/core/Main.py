import random
import time
import sqlite3
from pathlib import Path

P = Path(__file__).parent
data_F = P.parent/"data"
db_path = data_F / "database.db"

con = sqlite3.connect(db_path)
c = con.cursor()
current_location = 1
temp_loot = []
inventory = []

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

        for i in range(int(raid_time)):
            c.execute ("SELECT * FROM loot WHERE location_id = ?", (current_location,))
            loot_list = c.fetchall()
            for item in loot_list:
                chance = item [5] / 100
                if random.random() < chance:
                    temp_loot.append(item[0])
                    print(f"You found: {item[0]}")

            player_death = random.random() < death_chance
        if player_death == False:
            print ("Raid Success")
            inventory.extend(temp_loot)
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

