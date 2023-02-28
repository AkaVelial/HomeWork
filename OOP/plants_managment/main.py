from models import Plant, Employee
import re


def menu():
    while True:
        print("1. Add plant")
        print("2. Add employee")
        print("3. List all plants")
        print("4. List all employees")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter plant name: ")
            address = input("Enter plant address: ")
            plant = Plant(name, address)
            plant.save()

        elif choice == "2":
            name = input("Enter employee name: ")
            email = input("Enter employee email: ")
            plant_id = input("Enter plant ID: ")

            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                print("Invalid email.(example: vnv@i.ua)")
                continue
            else:
                employee = Employee(name, email, plant_id)
                employee.save()

        elif choice == "3":
            Plant.get_all()

        elif choice == "4":
            Employee.get_all()

        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    menu()
