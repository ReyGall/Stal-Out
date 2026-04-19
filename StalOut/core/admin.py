import sqlite3
from pathlib import Path 

P = Path(__file__).parent
data_F = P.parent/"data"
db_path = data_F / "database.db"

con = sqlite3.connect(db_path)
c = con.cursor()


c.execute ('''CREATE TABLE IF NOT EXISTS locations(
            name text,
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            death_chance INTEGER,
            armor_lvl INTEGER)
            ''')

c.execute ('''CREATE TABLE IF NOT EXISTS loot(
            name text,
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location_id INTEGER,
            price INTEGER,
            rarity text,
            chance INTEGER)
            ''')

c.execute ('''CREATE TABLE IF NOT EXISTS armor(
            name text,
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class text,
            price INTEGER,
            rarity text,
            lvl INTEGER)
            ''')

while True:

    print ("enter command, enter help for command list")

    user_input = input().lower().strip()

    if "add location" in user_input:
        print("enter location name")
        location_name = input()
        print("enter death chance")
        location_death_chance = input()
        print("enter min armor lvl")
        armor_lvl = input()

        c.execute (
            "INSERT INTO locations (name,death_chance, armor_lvl) VALUES (?,?,?)",
            (location_name, location_death_chance, armor_lvl)
            )

    elif "edit location" in user_input:
        print ("enter location id")
        edit_loc_id = input()

        c.execute("SELECT * FROM locations WHERE id = ?", (edit_loc_id,))
        loc = c.fetchone()
        
        if loc:
            print(f"Editing location: {loc[0]} (ID: {loc[1]})")
            print("What do you want to change? (name, death, armor)")
            field = input().lower().strip()
            
            if field == "name":
                new_val = input("Enter new name: ")
                c.execute("UPDATE locations SET name = ? WHERE id = ?", (new_val, edit_loc_id))
            
            elif field == "death":
                new_val = input("Enter new death chance: ")
                c.execute("UPDATE locations SET death_chance = ? WHERE id = ?", (new_val, edit_loc_id))
            
            elif field == "armor":
                new_val = input("Enter new armor level: ")
                c.execute("UPDATE locations SET armor_lvl = ? WHERE id = ?", (new_val, edit_loc_id))

    elif "delete location" in user_input:
        print ("enter location id")
        delete_location_id = input()
        print("are you sure? y/n")
        loot_accept = input()
        if loot_accept == "y":
            c.execute("DELETE FROM locations WHERE id = ?",
            (delete_location_id,))
        else:
            print("delete cancelled")

    elif "add loot" in user_input:
        print ("add loot name")
        loot_name = input()
        print ("enter location id")
        location_id = input()
        print ("enter loot price")
        loot_price = input()
        print ("enter loot rarity")
        loot_rarity = input()
        print("loot chance")
        loot_chance = input()
        c.execute(
            "INSERT INTO loot (name, location_id, price, rarity, chance) VALUES (?,?,?,?,?)",
            (loot_name,location_id, loot_price, loot_rarity, loot_chance)
            )
        
    elif "edit loot" in user_input:
        print("enter loot id")
        edit_loot_id = input()

        c.execute("SELECT * FROM loot WHERE id = ?", (edit_loot_id,))
        loot_item = c.fetchone()
        
        if loot_item:
            print(f"Editing loot: {loot_item[0]} (ID: {loot_item[1]})")
            print("What do you want to change? (name, location, price, rarity, chance)")
            field = input().lower().strip()
            
            if field == "name":
                new_val = input("Enter new name: ")
                c.execute("UPDATE loot SET name = ? WHERE id = ?", (new_val, edit_loot_id))
            
            elif field == "location":
                new_val = input("Enter new location ID: ")
                c.execute("UPDATE loot SET location_id = ? WHERE id = ?", (new_val, edit_loot_id))
            
            elif field == "price":
                new_val = input("Enter new price: ")
                c.execute("UPDATE loot SET price = ? WHERE id = ?", (new_val, edit_loot_id))

            elif field == "rarity":
                new_val = input("Enter new rarity: ")
                c.execute("UPDATE loot SET rarity = ? WHERE id = ?", (new_val, edit_loot_id))

            elif field == "chance":
                new_val = input("Enter new drop chance (1-100): ")
                c.execute("UPDATE loot SET chance = ? WHERE id = ?", (new_val, edit_loot_id))
            
            con.commit()

    elif "delete loot" in user_input:
        print ("enter loot id")
        delete_loot_id = input()
        print("are you sure? y/n")
        loot_accept = input()
        if loot_accept == "y":
            c.execute("DELETE FROM loot WHERE id = ?",
            (delete_loot_id,))
        else:
            print("delete cancelled")

    elif "locations list" in user_input:
        for location_list in c.execute ("SELECT * FROM locations ORDER BY id"):
            print (f"name: {location_list[0]}\nid: {location_list[1]}\ndeath chance: {location_list[2]}\nmin armor lvl: {location_list[3]} ")


    elif "loot list" in user_input:
        for loot_list in c.execute ("SELECT * FROM loot ORDER BY id"):
            print (f"name: {loot_list[0]}\n id: {loot_list[1]}\n location_id: {loot_list[2]}\n price: {loot_list[3]}\n rarity: {loot_list[4]}\n chance: {loot_list[5]}")

    elif "help" in user_input:
        print ("'add location' to add new location \n 'add loot' to add new loot \n 'locations list' to see list of locations \n 'loot list' to see list of loot")

    con.commit()
con.close()