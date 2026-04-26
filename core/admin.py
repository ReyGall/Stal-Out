import sqlite3
from pathlib import Path 
import os

P = Path(__file__).parent
data_F = P.parent/"data"
db_path = data_F / "database.db"

if not os.path.exists(data_F):
    os.makedirs(data_F)

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
            item_id INTEGER,
            FOREIGN KEY (armor_id) REFERENCES armor(id) ON DELETE CASCADE)
            ''')

while True:
    print ("\nenter command, enter help for command list")
    user_input = input().lower().strip()

    if "add location" in user_input:
        location_name = input("enter location name: ")
        location_death_chance = input("enter death chance: ")
        armor_lvl = input("enter min armor lvl: ")
        c.execute ("INSERT INTO locations (name,death_chance, armor_lvl) VALUES (?,?,?)",
                  (location_name, location_death_chance, armor_lvl))

    elif "edit location" in user_input:
        edit_loc_id = input("enter location id: ")
        c.execute("SELECT * FROM locations WHERE id = ?", (edit_loc_id,))
        loc = c.fetchone()
        if loc:
            print(f"Editing: {loc[0]} (ID: {loc[1]})")
            field = input("What to change? (name, death, armor): ").lower().strip()
            new_val = input("Enter new value: ")
            if field == "name":
                c.execute("UPDATE locations SET name = ? WHERE id = ?", (new_val, edit_loc_id))
            elif field == "death":
                c.execute("UPDATE locations SET death_chance = ? WHERE id = ?", (new_val, edit_loc_id))
            elif field == "armor":
                c.execute("UPDATE locations SET armor_lvl = ? WHERE id = ?", (new_val, edit_loc_id))

    elif "delete location" in user_input:
        delete_location_id = input("enter location id: ")
        if delete_location_id == "1":
            print("Action denied: Cannot delete starting location (ID 1)")
        else:
            if input(f"Are you sure you want to delete location {delete_location_id}? y/n: ") == "y":
                c.execute("DELETE FROM locations WHERE id = ?", (delete_location_id,))
                c.execute("DELETE FROM loot WHERE location_id = ?", (delete_location_id,))
                print("Location and its loot deleted")

    elif "add loot" in user_input:
        loot_name = input("add loot name: ")
        location_id = input("enter location id: ")
        loot_price = input("enter loot price: ")
        loot_rarity = input("enter loot rarity: ")
        loot_chance = input("loot chance: ")
        c.execute("INSERT INTO loot (name, location_id, price, rarity, chance) VALUES (?,?,?,?,?)",
                  (loot_name, location_id, loot_price, loot_rarity, loot_chance))
        
    elif "edit loot" in user_input:
        edit_loot_id = input("enter loot id: ")
        c.execute("SELECT * FROM loot WHERE id = ?", (edit_loot_id,))
        loot_item = c.fetchone()
        if loot_item:
            field = input("Change? (name, location, price, rarity, chance): ").lower().strip()
            new_val = input("Enter new value: ")
            mapping = {"name": "name", "location": "location_id", "price": "price", "rarity": "rarity", "chance": "chance"}
            if field in mapping:
                c.execute(f"UPDATE loot SET {mapping[field]} = ? WHERE id = ?", (new_val, edit_loot_id))

    elif "delete loot" in user_input:
        delete_loot_id = input("enter loot id: ")
        if input("are you sure? y/n: ") == "y":
            c.execute("DELETE FROM loot WHERE id = ?", (delete_loot_id,))

    elif "locations list" in user_input:
        for row in c.execute("SELECT * FROM locations ORDER BY id"):
            print(f"ID: {row[1]} | Name: {row[0]} | Death: {row[2]}% | Armor Lvl: {row[3]}")

    elif "loot list" in user_input:
        for row in c.execute("SELECT * FROM loot ORDER BY id"):
            print(f"ID: {row[1]} | Name: {row[0]} | Loc_ID: {row[2]} | Price: {row[3]} | Rarity: {row[4]} | Chance: {row[5]}%")

    elif "help" in user_input:
        print ("Commands: add location, edit location, delete location, locations list\n"
               "          add loot, edit loot, delete loot, loot list\n"
               "          add armor, edit armor, delete armor, armor list\n"
               "          add armor recipe, armor res list, delete armor res")

    elif "add armor" == user_input:
        name = input("name: "); cls = input("class: "); prc = input("price: ")
        rar = input("rarity: "); lvl = input("lvl: "); res = input("bullet resistance: ")
        c.execute("INSERT INTO armor (name, class, price, rarity, lvl, bullet_resistance) VALUES (?,?,?,?,?,?)",
                  (name, cls, prc, rar, lvl, res))

    elif "delete armor" == user_input:
        del_id = input("enter armor id to delete: ")
        if input("Are you sure? (This deletes recipes too) y/n: ") == "y":
            c.execute("DELETE FROM armor WHERE id = ?", (del_id,))

    elif "add armor recipe" == user_input:
        armor_r_id = input("enter armor id: ")
        while True:
            item_id = input("enter item ID from loot table: ")
            c.execute("SELECT name FROM loot WHERE id = ?", (item_id,))
            item_row = c.fetchone()
            if not item_row:
                print("Error: This item ID does not exist in loot table!")
                continue
            qty = input(f"enter quantity for {item_row[0]}: ")
            c.execute("INSERT INTO armor_recipes (armor_id, item_name, quantity, item_id) VALUES (?, ?, ?, ?)",
                      (armor_r_id, item_row[0], int(qty), int(item_id)))
            if input("enter 'c' to continue or 'e' to exit: ").lower() == "e":
                break

    elif "armor list" in user_input:
        for r in c.execute("SELECT * FROM armor ORDER BY id"):
            print(f"ID: {r[1]} | Name: {r[0]} | Class: {r[2]} | Price: {r[3]} | Lvl: {r[5]}")

    elif "edit armor" == user_input:
        edit_id = input("enter armor id: ")
        c.execute("SELECT * FROM armor WHERE id = ?", (edit_id,))
        if c.fetchone():
            field = input("Change? (name, class, price, rarity, lvl, resistance): ").lower().strip()
            new_v = input("New value: ")
            fields = {"name":"name", "class":"class", "price":"price", "rarity":"rarity", "lvl":"lvl", "resistance":"bullet_resistance"}
            if field in fields:
                c.execute(f"UPDATE armor SET {fields[field]} = ? WHERE id = ?", (new_v, edit_id))

    elif "armor res list" == user_input:
        for r in c.execute("SELECT * FROM armor_recipes ORDER BY armor_id"):
            print(f"ArmorID: {r[1]} | Item: {r[2]} (ID: {r[4]}) | Qty: {r[3]}")

    elif "delete armor res" == user_input:
        print("1. Delete ALL resources for an armor")
        print("2. Delete SPECIFIC resource by its ID")
        sub_choice = input("Select mode (1 or 2): ")

        if sub_choice == "1":
            arm_id = input("Enter armor ID to clear its recipe: ")
            if input(f"Delete ALL resources for armor {arm_id}? y/n: ") == "y":
                c.execute("DELETE FROM armor_recipes WHERE armor_id = ?", (arm_id,))
                print("Recipe cleared.")

        elif sub_choice == "2":
            res_id = input("Enter the unique Resource ID (from 'armor res list'): ")
            c.execute("DELETE FROM armor_recipes WHERE id = ?", (res_id,))
            print(f"Resource {res_id} removed from recipe.")

    con.commit()
con.close()