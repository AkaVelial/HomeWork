import sys
from models import Record, AddressBook, Name, Phone

# Словарь для хранения контактов
address_book = AddressBook()


# Декоратор для обработки ошибок ввода
def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except KeyError:
            return "Contact not found"
        except ValueError:
            return "Invalid input"
        except IndexError:
            return "Missing input"
    return inner


# Функция для добавления нового контакта
@input_error
def add_contact(name: str, phone: str) -> str:
    # Создаем экземпляр записи
    name_field = Name(name)
    phone_field = Phone(phone)
    record = Record(name_field)
    record.add_phone(phone_field)

    # Добавляем запись в адресную книгу
    address_book.add_record(record)
    return "Contact added"


# Функция для изменения номера телефона у существующего контакта
@input_error
def change_phone(name: str, phone: str) -> str:
    # Ищем запись по имени в адресной книге
    record = address_book.data.get(name)
    if not record:
        return "Contact not found"

    # Находим телефон для замены
    old_phone = record.phones[0]

    # Заменяем номер телефона
    new_phone_field = Phone(phone)
    record.edit_phone(old_phone, new_phone_field)
    return "Phone number updated"


# Функция для поиска номера телефона по имени контакта
@input_error
def get_phone(name: str) -> str:
    record = address_book.data[name]
    return record.phones[0].value


# Функция для вывода всех сохраненных контактов
def show_all() -> str:
    if not address_book:
        return "No contacts found"
    output = ""
    for name, record in address_book.items():
        output += f"{name}: {record.phones[0].value}\n"
    return output


# Функция для завершения работы программы
def close_program() -> None:
    print("Good bye!")
    sys.exit()


# Функция для обработки команд пользователя
def handle_command(command: str) -> str:
    parts = command.split()
    if parts[0].lower() == "hello":
        return "How can I help you?"
    elif parts[0].lower() == "add":
        if len(parts) < 3:
            return "Missing input"
        name = parts[1]
        phone = parts[2]
        return add_contact(name, phone)
    elif parts[0].lower() == "change":
        if len(parts) < 3:
            return "Missing input"
        name = parts[1]
        phone = parts[2]
        return change_phone(name, phone)
    elif parts[0].lower() == "phone":
        if len(parts) < 2:
            return "Missing input"
        name = parts[1]
        return get_phone(name)
    elif len(parts) >= 2 and parts[0].lower() == "show" and parts[1].lower() == "all":
        return show_all()
    elif parts[0].lower() in ["close", "exit"] \
            or (len(parts) >= 2 and parts[0].lower() == "good" and parts[1].lower() == "bye"):
        close_program()
    else:
        return "Invalid command"


# Функция для запуска бота помощника
def main() -> None:
    print("Welcome to the assistant bot!")
    while True:
        command = input("Enter command: ")
        response = handle_command(command)
        print(response)


if __name__ == '__main__':
    main()
