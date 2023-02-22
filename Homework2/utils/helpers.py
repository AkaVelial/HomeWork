import json
import re


def get_all_users() -> list:
    f = open("database/userbase.json", "r")
    data = json.loads(f.read())
    f.close()
    return data


def add_new_user(user: dict):
    data = get_all_users()
    if len(data) < 1:
        user["id"] = 1
    else:
        user["id"] = len(data) + 1
    data.append(user)
    file = open("database/userbase.json", "w")
    data = json.dumps(data)
    file.write(data)
    file.close()
    print("New user added")


def validate_email(email):
    match = re.search(r'[\w.-]+@[\w.-]+', email)
    if match:
        return True
    else:
        return False


def is_email_unique(email):
    data = get_all_users()
    for el in data:
        if el["email"] == email:
            return False
    return True


def edit_user_info(id):
    data = get_all_users()
    for el in data:
        if el["id"] == id:
            print("User found,update user info.")
            el["first_name"] = input("Enter new first name: ")
            el["last_name"] = input("Enter new last name: ")
            el["email"] = input("Enter new email: ")

            while not is_email_unique(el["email"]):
                print("This email already used")
                el["email"] = input("Enter new email: ")

            while not validate_email(el["email"]):
                print("Invalid email!")
                el["email"] = input("Enter new email: ")
            print("User info update successfully")

    file = open("database/userbase.json", "w")
    data = json.dumps(data)
    file.write(data)
    file.close()
