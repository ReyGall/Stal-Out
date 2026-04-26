def fence_merchant(c, inventory):

    total_earned = 0


    while True:
        if not inventory: print("Empty!"); break
        print ("Oh,look who's back! Do you want to sell me something?")

        item_counts = {}
        for item in inventory:
            item_counts[item] = item_counts.get(item, 0) + 1

        unique_ids = list(item_counts.keys())

        for i, item_id in enumerate(unique_ids):
            c.execute("SELECT name, price FROM loot WHERE id = ?", (item_id,))
            result = c.fetchone()
            if result is None:
                continue
            price = result[1] if result else 0
            display_name = result[0] if result else 0
            count = item_counts[item_id]

            print(f"[{i + 1}] {display_name} x{count} — {price} Rubbles.")
        print ("choose what you want to sell by sending number")
        item_for_sell = input()
        if item_for_sell.isdigit():
            index = int(item_for_sell) - 1
            if 0 <= index < len(unique_ids):
                id = unique_ids[index]
                count = item_counts[id]
                c.execute("SELECT name, price FROM loot WHERE id = ?", (id,))
                price = c.fetchone()[1] 
                print ("Alright dude how many you want to sell?")

                quantity_input = input()


                if quantity_input.isdigit():
                    quantity = int(quantity_input)
    
                    if quantity > count: 
                        quantity = count

                    total_earned += price * quantity

                    for i in range(quantity):
                        if id in inventory:
                            inventory.remove(id)

        print ("Thanks dude, anything else?\n(Y/N)")
        cycle = input().lower().strip()
                
        if "y" not in cycle:
            print ("See you later, my friend")
            break

    return inventory, total_earned
