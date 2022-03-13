import json
import re


def num_formater(number):
    number = str(number)
    new_format =[number[0:3], number[3:6], number[6:],]

    return "-".join(new_format)

def num_checker(number):
    number = str(number).strip()
    if (number.isdigit() and len(number) == 10) or number == "":
        return True

    return False

def email_checker(email):
    email = email.strip()
    if email == "":
        return True
    pattern = re.compile('[a-zA-Z0-9.-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{1,3}')
    test = bool(pattern.match(email))
    
    return test


with open("contacts.json", "r") as f:
        contacts = json.load(f)

def contact_details(fname, lname, mnumber, hnumber, email, address):
    
    contacts[f"{fname.capitalize()} {lname.capitalize()}"] ={
                "Email_address": email,
                "Mobile_number": num_formater(mnumber),
                "Home_number": hnumber,
                "Home_address": address,}
    with open("contacts.json", "w") as f:
        json.dump(contacts, f)


# print('''
# Welcome to your contact list!
# The following is a list of useable commands:
# "add": Adds a contact.
# "delete": Deletes a contact.
# "list": Lists all contacts.
# "search": Searches for a contact by name.
# "q": Quits the program and saves the contact list.\n''')



# user_input = print("Type a command:")


def add_contact():

    first_name = input("First Name: ").capitalize()
    while first_name == "":
        first_name = input("First name can't be blank, please input name: ").capitalize()
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
        contact_details(first_name, last_name, mobile_number, home_number, email_address, address)
        print("Contact Added!")
    else:
        for contact in contacts:
            if first_name in contact and last_name in contact:
                print("Contact already exists.")
            else:
                contact_details(first_name, last_name, mobile_number, home_number, email_address, address) 

            # Sorting list
            contacts = dict(sorted(contacts.items()))
            print("Contact Added!")

def delete_contact(first_name, last_name):

    for contact in contacts.keys():
        if first_name in contact and last_name in contact:
            response = input("Are you sure? ").lower()
            if response == "y" or response == "yes":
                contacts.pop(contact)
                with open("contacts.json", "w") as f:
                    json.dump(contacts, f)
                print("Contact deleted!")
                break
        else:
            print("No contact with this name exists.")



def contact_list():
    for index, contact in enumerate(contacts):
        number = contacts[contact]["Mobile_number"]
        email = contacts[contact]["Email_address"]
        print(f"{index}. {contact}\n\t Mobile: {number}\n\t Email: {email}")
        
    



