import random
import time
from save import save_game

def start_raid(inventory, current_location, debug_mode, c, save_path):

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
        save_game(save_path)

    else:
        print("You Died")
        temp_loot = []
        item_count = {}

    return inventory

