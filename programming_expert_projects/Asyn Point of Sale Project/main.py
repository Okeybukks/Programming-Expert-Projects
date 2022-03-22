import asyncio
from pickletools import markobject, optimize
from samp_inventory import Inventory

inventory = Inventory()
catalogue = inventory.catalogue


def combo(cart):
    burger = {x: y for x, y in cart.items() if "Burger" in x}
    burger_sorted = dict(sorted(burger.items(), key=lambda x: x[1], reverse=True))
    sides = {x: y for x, y in cart.items() if "Fries" in x or "Salad" in x}
    sides_sorted = dict(sorted(sides.items(), key=lambda x: x[1], reverse=True))
    drinks = {x: y for x, y in cart.items() if "Coke" in x or "Ale" in x or "Milk" in x}
    drinks_sorted = dict(sorted(drinks.items(), key=lambda x: x[1], reverse=True))

    zipped = zip(burger_sorted.items(), sides_sorted.items(), drinks_sorted.items())
    combo_list = []
    for i in zipped:
        combo_list.append(dict(i))

    return combo_list


def not_combo(cart):
    combo_list = combo(cart)
    d = [item for combo in range(len(combo_list)) for item in combo_list[combo]]
    single_items = {}
    for key, value in cart.items():
        if key not in d:
            single_items[key] = value

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
        ordered.append(item_id)

    order = await order_func(inventory, ordered)
    return order


async def order_func(inventory_class, ordered):
    cart_dict = {}
    print("Placing order...")
    for item_id in ordered:
        task1 = await asyncio.gather(
            inventory_class.stock_return_value(item_id),
            inventory_class.decrement_stock(item_id),
        )
        if all(task1):
            task2 = await asyncio.create_task(inventory_class.get_item(item_id))
            print(task2)
            item_name, item_price = task2["name"], task2["price"]
            cart_dict[item_name] = item_price

    print("Here is a summary of your order:")
    print("\n")
    combo_list = combo(cart_dict)
    not_combo_list = not_combo(cart_dict)
    not_combo_price = round(sum(not_combo_list.values()), 2)
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

    for item, price in not_combo_list.items():
        print(f"${price} {item}")

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

