import sqlite3
from pathlib import Path 

P = Path(__file__).parent
data_F = P.parent/"data"
db_path = data_F / "database.db"

con = sqlite3.connect(db_path)
c = con.cursor()
c.execute("PRAGMA foreign_keys = ON")


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
            lvl INTEGER,
            bullet_resistance INTEGER)
            ''')

c.execute ('''CREATE TABLE IF NOT EXISTS armor_recipes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            armor_id INTEGER,
            item_name text,
            quantity INTEGER,
            FOREIGN KEY (armor_id) REFERENCES armor(id) ON DELETE CASCADE)
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
            c.execute("DELETE FROM loot WHERE location_id = ?", (delete_location_id))
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
        print ("'add location' to add new location \n 'add loot' to add new loot \n 'locations list' to see list of locations \n 'loot list' to see list of loot \n 'armor list' to see list of armor \n 'add armor' to add new armor \n 'delete armor' to delete armor")

    elif "add armor" == user_input:
        print ("enter armor name")
        armor_name = input()
        print ("enter armor class")
        armor_class = input()
        print ("enter armor price")
        armor_price = input()
        print ("enter armor rarity")
        armor_rarity = input()
        print("enter armor lvl")
        armor_lvl = input()
        print("enter armor bullet resistance")
        armor_bullet_r = input()
        c.execute(
            "INSERT INTO armor (name, class, price, rarity, lvl, bullet_resistance) VALUES (?,?,?,?,?,?)",
            (armor_name, armor_class, armor_price, armor_rarity, armor_lvl, armor_bullet_r)
            )

    elif "add armor recipe" == user_input:
        print ("enter armor id to add recipe")
        armor_r_id = input()
        while True:
            print ("enter item name")
            item_name = input()
            print ("enter item quantity")
            item_quantity = input()
            c.execute(
                "INSERT INTO armor_recipes (armor_id, item_name, quantity) VALUES (?, ?, ?)",
                (armor_r_id, item_name, int(item_quantity))
                )
            print("item added, enter 'c' to continue or 'e' to exit")
            user_choise = input().lower().strip()
            if user_choise == "e":
                con.commit()
                break

    elif "armor list" in user_input:
        for armor_list in c.execute ("SELECT * FROM armor ORDER BY id"):
            print (f"name: {armor_list[0]}\nid: {armor_list[1]}\nclass: {armor_list[2]}\nprice: {armor_list[3]}\nrarity: {armor_list[4]}\narmor lvl: {armor_list[5]}\nparmor bullet resistance: {armor_list[6]} ")

    elif "edit armor" == user_input:
        print("enter armor id")
        edit_armor_id = input()

        c.execute("SELECT * FROM armor WHERE id = ?", (edit_armor_id,))
        armor = c.fetchone()
        
        if armor:
            print(f"Editing armor: {armor[0]} (ID: {armor[1]})")
            print("What do you want to change? (name, class, price, rarity, lvl, bullet resistance)")
            field = input().lower().strip()
            
            if field == "name":
                new_armor_name = input("Enter new name: ")
                c.execute("UPDATE armor SET name = ? WHERE id = ?", (new_armor_name, edit_armor_id))
            
            elif field == "class":
                new_armor_class = input("Enter new class name: ")
                c.execute("UPDATE armor SET class = ? WHERE id = ?", (new_armor_class, edit_armor_id))
            
            elif field == "price":
                new_armor_price = input("Enter new price: ")
                c.execute("UPDATE armor SET price = ? WHERE id = ?", (new_armor_price, edit_armor_id))

            elif field == "rarity":
                new_armor_rarity = input("Enter new rarity: ")
                c.execute("UPDATE armor SET rarity = ? WHERE id = ?", (new_armor_rarity, edit_armor_id))

            elif field == "lvl":
                new_armor_lvl = input("Enter new armor lvl: ")
                c.execute("UPDATE armor SET lvl = ? WHERE id = ?", (new_armor_lvl, edit_armor_id))
            
            elif field == "bullet resistance":
                new_armor_r = input("Enter new armor bullet resistance: ")
                c.execute("UPDATE armor SET bullet_resistance = ? WHERE id = ?", (new_armor_r, edit_armor_id))
            
            con.commit()

    elif "armor res list" == user_input:
        for armor_res_list in c.execute("SELECT * FROM armor_recipes ORDER BY armor_id"):
            print (f"id: {armor_res_list[0]}\narmor_id: {armor_res_list[1]}\nitem_name: {armor_res_list[2]}\nquantity: {armor_res_list[3]}\n")


    con.commit()
con.close()
