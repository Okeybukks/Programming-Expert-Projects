import json
import re

# Function to format number in the form 123-456-7890
def num_formater(number):
    number = str(number)
    new_format = [
        number[0:3],
        number[3:6],
        number[6:],
    ]

    return "-".join(new_format)


# Function to check if input number is valid
def num_checker(number):
    number = str(number).strip()
    if (number.isdigit() and len(number) == 10) or number == "":
        return True

    return False


# Function to check if input email is valid
def email_checker(email):
    email = email.strip()
    if email == "":
        return True
    pattern = re.compile("[a-zA-Z0-9.-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{1,3}")
    test = bool(pattern.match(email))

    return test


# Function to add contact details into the contact dictionary
def contact_details(fname, lname, mnumber, hnumber, email, address):
    with open("contacts.json", "r") as f:
        contacts = json.load(f)

    contacts[f"{fname.capitalize()} {lname.capitalize()}"] = {
        "Email_address": email,
        "Mobile_number": num_formater(mnumber),
        "Home_number": hnumber,
        "Home_address": address,
    }
    with open("contacts.json", "w") as f:
        json.dump(contacts, f)


# Function to add contact in dictionary into json file
def add_contact():
    with open("contacts.json", "r") as f:
        contacts = json.load(f)

    first_name = input("First Name: ").capitalize()
    while first_name == "":
        first_name = input(
            "First name can't be blank, please input name: "
        ).capitalize()
    last_name = input("Last Name: ").capitalize()
    while last_name == "":
        last_name = input("Last name can't be blank, please input name: ").capitalize()
    mobile_number = input("Mobile Phone Number: ")
    while num_checker(mobile_number) != True or mobile_number == "":
        mobile_number = input("Input valid Mobile number.: ")
    home_number = input("Home Phone Number: ")
    while num_checker(home_number) != True:
        home_number = input("Input valid Home number.: ")
    email_address = input("Email Address: ").lower()
    while email_checker(email_address) != True or email_address == "":
        email_address = input("Input valid email address.: ").lower()
    address = input("Address: ").lower()

    if len(contacts) == 0:
        contact_details(
            first_name, last_name, mobile_number, home_number, email_address, address
        )

    else:
        for contact in contacts:
            if first_name in contact and last_name in contact:
                print("Contact already exists.")
            else:
                contact_details(
                    first_name,
                    last_name,
                    mobile_number,
                    home_number,
                    email_address,
                    address,
                )

    # Sorting list
    contacts = dict(sorted(contacts.items()))
    print("Contact Added!")


# Function to delete a contact permanently from json file
def delete_contact():
    with open("contacts.json", "r") as f:
        contacts = json.load(f)

    first_name = input("First Name: ").capitalize()
    last_name = input("Last Name: ").capitalize()
    search_name = f"{first_name} {last_name}"
    print(search_name)

    if search_name in contacts:
        response = input("Are you sure you want to delete contact ?: ").lower()
        if response == "y" or response == "yes":
            contacts.pop(search_name)
            with open("contacts.json", "w") as f:
                json.dump(contacts, f)
            print("Contact deleted!")
        else:
            print("No contact with this name exists.")


# Function which prints contacts available
def contact_list():
    with open("contacts.json", "r") as f:
        contacts = json.load(f)

    for index, contact in enumerate(contacts):
        number = contacts[contact]["Mobile_number"]
        email = contacts[contact]["Email_address"]
        home_address = contacts[contact]["Home_address"]
        if home_address == "":
            print(f"{index}. {contact}\n\t Mobile: {number}\n\t Email: {email}")
        else:
            print(
                f"{index}. {contact}\n\t Mobile: {number}\n\t Email: {email}\n\t Address: {home_address}"
            )


# Function to search for a contact
def search_contact():
    with open("contacts.json", "r") as f:
        contacts = json.load(f)

    fname = input("First Name: ")
    lname = input("Last Name: ")

    contacts_found = []
    for contact in contacts.keys():
        first_name = contact.split(" ")[0].lower()
        last_name = contact.split(" ")[1].lower()
        if (fname in first_name and fname != "") or (
            lname in last_name and lname != ""
        ):
            contacts_found.append(contact)

    if len(contacts_found) != 0:
        print(f"Found {len(contacts_found)} matching contact(s).")
        for index, contact in enumerate(contacts_found):
            number = contacts[contact]["Mobile_number"]
            email = contacts[contact]["Email_address"]
            home_address = contacts[contact]["Home_address"]
            if home_address == "":
                print(f"{index + 1}. {contact}\n\t Mobile: {number}\n\t Email: {email}")
            else:
                print(
                    f"{index + 1}. {contact}\n\t Mobile: {number}\n\t Email: {email}\n\t Address: {home_address}"
                )
    else:
        print(f"Found 0 matching contact.")


print(
    """
Welcome to your contact list!
The following is a list of useable commands:
"add": Adds a contact.
"delete": Deletes a contact.
"list": Lists all contacts.
"search": Searches for a contact by name.
"q" or "quit": Quits the program and saves the contact list.\n"""
)


while True:
    print("\n")
    user_input = input("Type a command: ").lower()
    if user_input == "add":
        add_contact()
    elif user_input == "delete":
        delete_contact()
    elif user_input == "list":
        contact_list()
    elif user_input == "search":
        search_contact()
    elif user_input == "q" or user_input == "quit":
        print("Thanks for using program!")
        break
    else:
        print("Invalid input!")
