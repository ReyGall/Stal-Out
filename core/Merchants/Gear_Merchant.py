from inventory import show_inventory

def Buy_Armor(c, inventory, money):

    print ("Hello dude, wanna buy armor? Lets see that we have\n")

    c.execute ("SELECT name, price FROM armor")
    armor_list = c.fetchall()

    for i,item in enumerate (armor_list):

        print(f"[{i + 1}]{item[0]} - {item[1]} Rubbles")

    print (" ")

    show_inventory(inventory, c, money)
    print ("choose which you want to buy by sending number\n")
    armor_id = input()

    c.execute ("SELECT name, price FROM armor WHERE id = ?", (armor_id,))
    result = c.fetchone()
    if result == None:
        print ("Yo dude I have no this armor right now, come back later")
        return inventory, money

    armor_name, armor_price = result

    if money >= armor_price:

        money -=armor_price
        inventory.append(armor_name)

        print(f"successfuly bought {armor_name}")
        return inventory, money, 
    
    else:
        print ("Yo dude you have no enough money\n")
        return inventory, money