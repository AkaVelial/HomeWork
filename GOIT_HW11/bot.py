import sys
from typing import List
from models import Record, AddressBook, Name, Phone, Birthday
from datetime import datetime


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
def add_contact(name: str, phones: List[str]) -> str:
    # Создаем экземпляр записи
    name_field = Name(name)
    record = Record(name_field)

    for phone in phones:
        phone_field = Phone(phone)
        phone_field.value = phone   # setter
        record.add_phone(phone_field)

    # Добавляем запись в адресную книгу
    address_book.add_record(record)
    return "Contact added"


# Функция для изменения номера телефона у существующего контакта
@input_error
def change_phone(name: str, old_phone: str, new_phone: str) -> str:
    record = address_book.data.get(name)
    if not record:
        return "Contact not found"

    for phone in record.phones:
        if phone.value == old_phone:
            phone.value = new_phone
            return "Phone number updated"

    return "Old phone number not found for the contact"


# Функция для поиска номера телефона по имени контакта
@input_error
def get_phone(name: str) -> str:
    record = address_book.data.get(name)
    if record:
        phones = record.phones
        if phones:
            return phones[0]
    return "Phone number not found"


# Функция для установки дня рождения у контакта
@input_error
def set_birthday(name: str, birthday: Birthday) -> str:
    record = address_book.data.get(name)
    if not record:
        return "Contact not found"

    try:
        birthday_date_str = birthday.value.strftime("%d-%m-%Y")
        birthday_date = datetime.strptime(birthday_date_str, "%d-%m-%Y").date()
        birthday_field = Birthday(birthday_date)
        record.set_birthday(birthday_field)
        return "Birthday set"
    except ValueError:
        return f"Invalid date format. Please use the format: DD-MM-YYYY. Birthday: {birthday.value}"


# Функция для вывода всех сохраненных контактов
def show_all() -> str:
    if not address_book.data:
        return "No contacts found"
    output = ""
    for name, record in address_book.data.items():
        phones = [phone.value for phone in record.phones]  # Получаем все значения номеров телефонов
        phones_str = ", ".join(phones)  # Преобразуем список в строку с разделителем ", "
        birthday_info = ""
        if record.birthday:
            days_to_birthday = record.days_to_birthday()
            if days_to_birthday == 0:
                birthday_info = " (Today is their birthday!)"
            elif days_to_birthday > 0:
                birthday_info = f" ({days_to_birthday} days until their birthday)"
            else:
                birthday_info = f" (Their birthday has already passed)"
        output += f"{name}: {phones_str}{birthday_info}\n"
    return output


# Функция для пагинации контактов
def paginate_contacts(page_size: int) -> str:
    output = ""
    for page in address_book.paginate(page_size):
        for name, record in page:
            output += f"{name}: {record.phones[0].value}\n"
        output += "---\n"  # Разделитель между страницами
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
        phones = parts[2:]
        return add_contact(name, phones)

    elif parts[0].lower() == "change":
        if len(parts) < 4:
            return "Missing input"
        name = parts[1]
        old_phone = parts[2]
        new_phone = parts[3]
        return change_phone(name, old_phone, new_phone)

    elif parts[0].lower() == "phone":
        if len(parts) < 2:
            return "Missing input"
        name = parts[1]
        return get_phone(name)

    elif len(parts) >= 2 and parts[0].lower() == "show" and parts[1].lower() == "all":
        return show_all()

    elif parts[0].lower() == "birthday":
        if len(parts) < 3:
            return "Missing input"
        name = parts[1]
        birthday_str = parts[2]
        try:
            birthday = datetime.strptime(birthday_str, "%d-%m-%Y").date()
            birthday_field = Birthday(birthday)
            return set_birthday(name, birthday_field)
        except ValueError:
            return "Invalid date format. Please use the format: DD-MM-YYYY"

    elif parts[0].lower() == "paginate":
        if len(parts) < 2:
            return "Missing input"
        page_size = int(parts[1])
        return paginate_contacts(page_size)

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
