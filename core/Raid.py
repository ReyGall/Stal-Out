import random
import time
from save import save_game

def start_raid(inventory, current_location, debug_mode, c, save_path, money):

    print("enter raid time in minutes from 1 to 360")
    try:
        raid_time = input()
        raid_time_int = int(raid_time)
    except ValueError:
        print("invalid number")
    print("Raid Started")
    temp_loot = []
    c.execute ("SELECT death_chance FROM locations WHERE id = ?", (current_location,))
    death_chance_inc = c.fetchone() 

    if death_chance_inc is None:
        print(f"Error: Location {current_location} not found in DB!")
        return inventory

    death_chance = death_chance_inc [0] * 0.01

    player_alive = True
    temp_loot = []

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
                temp_loot.append(item[1])
                print(f"You found: {item[0]}")

        player_alive = random.random() > death_chance
    if player_alive == True:
        print ("Raid Success")
        inventory.extend(temp_loot)
        temp_loot = []
        save_game(save_path, inventory, money)

    else:
        print("You Died")
        temp_loot = []
        

    return inventory


