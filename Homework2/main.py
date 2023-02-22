from utils.helpers import add_new_user, get_all_users,  edit_user_info, validate_email, is_email_unique


while True:
    print("1.Add new user!\n2.Get all users!\n3.Edit user info\n0.Exit program")
    flag = int(input("Choose option:"))

    if flag == 1:
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        email = input("Email: ")

        while not validate_email(email):
            print("Invalid Email!(example:vnv@i.ua)")
            email = input("Email: ")

        while not is_email_unique(email):
            print("This email already used!")
            email = input("Enter new email: ")

        user_dict = {'first_name': first_name, "last_name": last_name, "email": email}
        add_new_user(user_dict)

    elif flag == 2:
        users = get_all_users()
        for user in users:
            print("Users base:")
            print(user["first_name"])
            print(user["last_name"])
            print(user["email"])
            print("******************")

    elif flag == 3:
        id = int(input("Enter user_id to edit: "))
        edit_user_info(id)
    elif flag == 0:
        print("See you later,buddy))")
        break

    else:
        print("Choose another option:")
