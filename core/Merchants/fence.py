def fence_merchant(c, inventory):

    total_earned = 0


    while True:
        if not inventory: print("Empty!"); break
        print ("Oh,look who's back! Do you want to sell me something?")

        item_counts = {}
        for item in inventory:
            item_counts[item] = item_counts.get(item, 0) + 1

        unique_items = list(item_counts.keys())

        for i, item_name in enumerate(unique_items):
            c.execute("SELECT price FROM loot WHERE name = ?", (item_name,))
            result = c.fetchone()
            if result is None:
                continue
            price = result[0] if result else 0
            count = item_counts[item_name]

            print(f"[{i + 1}] {item_name} x{count} — {price} Rubbles.")
        print ("choose what you want to sell by sending number")
        item_for_sell = input()
        if item_for_sell.isdigit():
            index = int(item_for_sell) - 1
            if 0 <= index < len(unique_items):
                name = unique_items[index]
                count = item_counts[name]
                c.execute("SELECT price FROM loot WHERE name = ?", (name,))
                price = c.fetchone()[0]
                print ("Alright dude how many you want to sell?")

                quantity_input = input()


                if quantity_input.isdigit():
                    quantity = int(quantity_input)
    
                    if quantity > count: 
                        quantity = count

                    total_earned += price * quantity

                    for i in range(quantity):
                        if name in inventory:
                            inventory.remove(name)

        print ("Thanks dude, anything else?\n(Y/N)")
        cycle = input().lower().strip()
                
        if "y" not in cycle:
            print ("See you later, my friend")
            break

    return inventory, total_earned
