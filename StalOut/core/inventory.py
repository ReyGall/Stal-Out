def show_inventory(inventory, c, money):
        
        colors = {
             
            "Picklock": "\033[37m",
            "end":"\033[0m"

            }
        
        item_count = {}

        for item in inventory:
            if item in item_count:
                item_count[item] += 1
            else:
                item_count[item] = 1


        items = c.fetchall()

        print ("Your Inventory:")
        print (f"{money} Rubbles")

        for item, count in item_count.items():

            c.execute ("SELECT rarity FROM loot WHERE name = ?", (item,))
            item_rarity = c.fetchone()
            rarity_from_db = item_rarity[0].strip()
            if rarity_from_db == "Picklock":
                item_color = colors["Picklock"]

                
            
            end_color = colors["end"]

            print(f"{item_color}{item}{end_color} x{count}")
        print (" ")