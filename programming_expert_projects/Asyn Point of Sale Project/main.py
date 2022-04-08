import asyncio
from samp_inventory import Inventory


inventory = Inventory()
catalogue = inventory.catalogue


def combo(cart):

    burger = [x for x in cart if "Burger" in x[0]]
    burger_sorted = sorted(burger, key=lambda x: x[1], reverse=True)
    sides = [x for x in cart if "Fries" in x[0] or "Salad" in x[0]]
    sides_sorted = sorted(sides, key=lambda x: x[1], reverse=True)
    drinks = [x for x in cart if "Coke" in x[0] or "Ale" in x[0] or "Milk" in x[0]]
    drinks_sorted = sorted(drinks, key=lambda x: x[1], reverse=True)

    zipped = zip(burger_sorted, sides_sorted, drinks_sorted)
    combo_list = []
    for i in zipped:
        combo_list.append(dict(i))

    return combo_list


def not_combo(cart):
    combo_list = combo(cart)
    combo_list = [x for y in combo_list for x in y.items()]
    for item in combo_list:
        if item in cart:
            cart.remove(item)

    single_items = cart

    return single_items


def value_checker(value):
    value = int(value)
    if value < 0:
        return False
    return True


def option_checker(answer):
    while True:
        if answer == "Yes" or answer == "No":
            break
        else:
            answer = input(f"Please input a valid value(yes/no): ")
            continue

    return answer


async def display_catalogue(catalogue):
    print("Welcome to the ProgrammingExpert Burger Bar!\nLoading catalogue...")
    await asyncio.sleep(2)

    burgers = catalogue["Burgers"]
    sides = catalogue["Sides"]
    drinks = catalogue["Drinks"]

    print("--------- Burgers -----------\n")
    for burger in burgers:
        item_id = burger["id"]
        name = burger["name"]
        price = burger["price"]
        print(f"{item_id}. {name} ${price}")

    print("\n---------- Sides ------------")
    for side in sides:
        sizes = sides[side]

        print(f"\n{side}")
        for size in sizes:
            item_id = size["id"]
            size_name = size["size"]
            price = size["price"]
            print(f"{item_id}. {size_name} ${price}")

    print("\n---------- Drinks ------------")
    for beverage in drinks:
        sizes = drinks[beverage]

        print(f"\n{beverage}")
        for size in sizes:
            item_id = size["id"]
            size_name = size["size"]
            price = size["price"]
            print(f"{item_id}. {size_name} ${price}")

    print("\n------------------------------\n")

    async def repeat_order_func():
        returned_order = await welcome_func(inventory)

        if returned_order == 0:
            make_order = input(
                "No order made, do you wish to order now(yes/no)? "
            ).capitalize()
            make_order = option_checker(make_order)
            if make_order == "Yes":
                repeat_order_bool = True
            elif make_order == "No":
                print("No problem, please come again!")
                repeat_order_bool = False
        else:
            make_order = input(
                f"Would you like to purchase this order for ${returned_order} (yes/no)? "
            ).capitalize()

            make_order = option_checker(make_order)

            if make_order == "Yes":
                print("Thank you for your order!")
                print("\n")
                repeat_order = input(
                    "Would you like to make another order (yes/no)? "
                ).capitalize()
                repeat_order = option_checker(repeat_order)

                if repeat_order == "Yes":
                    repeat_order_bool = True
                else:
                    print("Goodbye!")
                    repeat_order_bool = False

            elif make_order == "No":
                print("No problem, please come again!")
                repeat_order_bool = False
                print("\n")
        return repeat_order_bool

    while True:
        repeat_order_bool = await repeat_order_func()

        if repeat_order_bool == False:
            break


async def item_getter(inventory, item_id):
    stock, item = await asyncio.gather(
        inventory.stock_return_value(item_id),
        inventory.get_item(item_id),
    )

    if stock == 0:
        return False, item_id

    success = await inventory.decrement_stock(item_id)

    if not success:
        return False, item_id

    return True, item


async def welcome_func(inventory):
    ordered = []

    print(
        "Please enter the number of items that you would like to add to your order. Enter q to complete your order."
    )

    while True:
        item_id = input("Enter an item number: ")
        if item_id == "q":
            break
        while item_id.isdigit() == False or value_checker(item_id) == False:
            item_id = input("Enter a valid item number: ")
            if item_id == "q":
                break

        item_id = int(item_id)
        add_to_order_task = asyncio.create_task(item_getter(inventory, item_id))
        ordered.append(add_to_order_task)

    order = await order_func(ordered)

    return order


async def order_func(ordered):
    cart_dict = []
    print("Placing order...")
    for task in ordered:
        stock, item = await task

        if stock == True:
            item_id = item["id"]
            item_name, item_price = item["name"], item["price"]
            cart_dict.append((item_name, item_price))
        else:
            item_id = item
            print(
                f"Unfortunately item number {item_id} is out of stock and has been removed from your order. Sorry!"
            )
    # print(cart_dict)
    print("Here is a summary of your order:")
    print("\n")

    combo_list = combo(cart_dict)
    not_combo_list = not_combo(cart_dict)
    not_combo_price = round(sum([item[1] for item in not_combo_list]), 2)
    combo_prices = []

    if len(combo_list) == 0:
        combo_prices = [0]
    else:
        for combo_item in combo_list:
            combo_price = round(sum(combo_item.values()) * 0.85, 2)
            combo_prices.append(combo_price)

            print(f"${combo_price} Burger Combo")
            for item in combo_item.keys():
                print(f"\t{item}")

    for item in not_combo_list:
        print(f"${item[1]} {item[0]}")

    subtotal_price = round(sum(combo_prices) + not_combo_price, 2)
    tax = round(subtotal_price * 0.05, 2)
    total_price = subtotal_price + tax

    print("\n")
    print(f"Subtotal: ${subtotal_price}")
    print(f"Tax: ${tax}")
    print(f"Total: ${total_price}")

    return round(total_price, 2)


async def main():
    await display_catalogue(catalogue)


if __name__ == "__main__":
    asyncio.run(main())
