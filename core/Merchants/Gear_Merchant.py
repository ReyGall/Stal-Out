from inventory import show_inventory

def buy_Armor(c, inventory, money, owned_armor):

    can_afford_resources = True

    print ("Hello dude, wanna buy armor? Lets see that we have\n")

    c.execute ("SELECT name, price FROM armor")
    armor_list = c.fetchall()

    for i,item in enumerate (armor_list):

        print(f"[{i + 1}]{item[0]} - {item[1]} Rubbles")

    print (" ")

    show_inventory(inventory, c, money, owned_armor)
    print ("choose which you want to buy by sending number\n")
    choice = input()
    if choice.isdigit():
            
        armor_id = armor_list[choice -1][0]

        c.execute ("SELECT name, price FROM armor WHERE id = ?", (armor_id,))
        result = c.fetchone()

        if result == None:
            print ("Yo dude I have no this armor right now, come back later")
            return inventory, money

        c.execute ("SELECT item_name, quantity FROM armor_recipes WHERE armor_id = ?", (armor_id,))
        resourses_list = c.fetchall()

        armor_name, armor_price = result

        recipe_text = ""

        for req_name, req_qty in resourses_list:

            current_count = inventory.count(req_name)
            
            recipe_text += f"{req_name} x{req_qty}\n"
            if current_count < req_qty:
                can_afford_resources = False
            
        print(f"To buy this you need:\n{armor_price} rubbles\n{recipe_text}")

        if money >= armor_price and can_afford_resources == True:

            money -=armor_price

            for name, qty in resourses_list:
                for _ in range(qty):
                    inventory.remove(name)

            owned_armor.append(armor_name)

            print(f"successfuly bought {armor_name}")
            return inventory, money, owned_armor
        
        else:
            print ("Yo dude you have no enough money or resourses\n")
            return inventory, money