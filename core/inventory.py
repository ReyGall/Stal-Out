def show_inventory(inventory, c, money, owned_armor):
        
        colors = {
             
            "Picklock": "\033[37m",
            "default":"\033[37m",
            "end":"\033[0m"

            }
        
        item_count = {}
        armor_count = {}
        end_color = colors["end"]

        for item in inventory:
            if item in item_count:
                item_count[item] += 1
            else:
                item_count[item] = 1

        for armor in owned_armor:
            if armor in armor_count:
                armor_count[armor] += 1
            else:
                armor_count[armor] = 1

        print ("Your Inventory:")
        print (f"{money} Rubbles")

        print("\narmors:")

        for armor_id, count in armor_count.items():
            c.execute ("SELECT name,rarity FROM armor WHERE id = ?",(armor_id,))
            armor_db = c.fetchone()
            if armor_db is not None:
                armor_name_from_db = armor_db[0]
                armor_rarity_from_db = armor_db[1].strip()

                if armor_rarity_from_db == "Picklock":
                    armor_color = colors["Picklock"]
                else:
                    armor_color = colors["default"]

                print(f"{armor_color}{armor_name_from_db}{end_color} x{count}")
            else: 
                print("error, no armor in db")
            
        print ("\nitems:")
        for item, count in item_count.items():

            c.execute ("SELECT rarity, name FROM loot WHERE id = ?", (item,))
            item_db = c.fetchone()
            if item_db is not None:
                rarity_from_db = item_db[0].strip()
                name_from_db = item_db[1]
                if rarity_from_db == "Picklock":
                    item_color = colors["Picklock"]
                else:
                    item_color = colors["default"]

                print(f"{item_color}{name_from_db}{end_color} x{count}")
            else:
                print ("error, no item_rarity in db")
        print (" ")