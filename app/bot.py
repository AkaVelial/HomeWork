import os
from models.record import Record
from models.fields import Name, Phone, Birthday
from models.address_book import AddressBook
from view.view import ConsoleView
from decorators.decorators import input_error
from datetime import datetime
from typing import List
import pickle
import sys
import logging


class BotAssistant:
    def __init__(self):
        self.address_book = AddressBook()
        self.view = ConsoleView()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        self.command_handler = logging.StreamHandler()
        self.command_handler.setLevel(logging.INFO)

        self.file_handler = logging.FileHandler("logs/logs.txt")
        self.file_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        self.command_handler.setFormatter(formatter)

        self.file_handler.setFormatter(formatter)

        self.logger.addHandler(self.command_handler)
        self.logger.addHandler(self.file_handler)

    @input_error
    def save_address_book(self, filename):
        directory = "AddressBooks"
        os.makedirs(directory, exist_ok=True)
        filepath = os.path.join(directory, filename)
        try:
            with open(filepath, "wb") as file:
                pickle.dump(self.address_book.data, file)
            self.view.display_message("Address book saved successfully.")
        except IOError:
            self.view.display_message("Error: Failed to save the address book.")

    @input_error
    def load_address_book(self, filename):
        directory = "AddressBooks"
        filepath = os.path.join(directory, filename)
        try:
            with open(filepath, "rb") as file:
                self.address_book.data = pickle.load(file)
            self.view.display_message("Address book loaded successfully.")
        except (IOError, pickle.UnpicklingError):
            self.view.display_message("Error: Failed to load the address book")

    @input_error
    def add_contact(self, name: str, phones: List[str]) -> str:
        name_field = Name(name)
        record = Record(name_field)

        for phone in phones:
            phone_field = Phone(phone)
            phone_field.value = phone
            record.add_phone(phone_field)

        self.address_book.add_record(record)
        return "Contact added"

    @input_error
    def change_phone(self, name: str, old_phone: str, new_phone: str) -> str:
        record = self.address_book.data.get(name)
        if not record:
            return "Contact not found"

        for phone in record.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                return "Phone number updated"

        return "Old phone number not found for the contact"

    @input_error
    def get_phone(self, name: str) -> str:
        record = self.address_book.data.get(name)
        if record:
            phones = record.phones
            if phones:
                return phones[0]
        return "Phone number not found"

    @input_error
    def set_birthday(self, name: str, birthday: Birthday) -> str:
        record = self.address_book.data.get(name)
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

    @input_error
    def show_all(self) -> List[str]:
        if not self.address_book.data:
            return ["No contacts found"]
        output = []
        for name, record in self.address_book.data.items():
            phones = [phone.value for phone in record.phones]
            phones_str = ", ".join(phones)
            birthday_info = ""
            if record.birthday:
                days_to_birthday = record.days_to_birthday()
                if days_to_birthday == 0:
                    birthday_info = " (Today is their birthday!)"
                elif days_to_birthday > 0:
                    birthday_info = f" ({days_to_birthday} days until their birthday)"
                else:
                    birthday_info = f" (Their birthday has already passed)"
            output.append(f"{name}: {phones_str}{birthday_info}\n")
        return output

    @input_error
    def paginate_contacts(self, page_size: int) -> str:
        output = ""
        for page in self.address_book.paginate(page_size):
            for name, record in page:
                phones = [phone.value for phone in record.phones]
                phones_str = ", ".join(phones)
                if record.birthday:
                    birthday = record.birthday.strftime("%d-%m-%Y")
                    output += f"{name}: {phones_str}(Birthday: {birthday})\n"
                else:
                    output += f"{name}: {phones_str}\n"
            output += "-----------------\n"
        return output

    @input_error
    def search_contacts(self, query):
        matching_contacts = []
        for record in self.address_book.data.values():
            name = record.name.value
            phone_numbers = [phone.value for phone in record.phones]
            if query in name or any(query in number for number in phone_numbers):
                matching_contacts.append(record)

        if len(matching_contacts) == 0:
            return "No matching contacts found."

        output = ""
        for record in matching_contacts:
            name = record.name.value
            phones = ", ".join(phone.value for phone in record.phones)
            output += f"Name: {name}\nPhone Numbers: {phones}\n\n"

        return output

    def close_program(self) -> None:
        self.view.display_message("Good bye!")
        sys.exit()

    def handle_command(self, command: str) -> None:
        parts = command.split()
        if parts[0].lower() == "hello":
            self.view.display_message("How can I help you?")
            self.logger.info("Command: hello")

        elif parts[0].lower() == "help":
            self.view.display_commands()
            self.logger.info("Command: help")

        elif parts[0].lower() == "add":
            if len(parts) < 3:
                self.view.display_message("Missing input")
            name = parts[1]
            phones = parts[2:]
            self.view.display_message(self.add_contact(name, phones))
            self.logger.info(f"Command: add contact name:{name}, phone:{phones}")

        elif parts[0].lower() == "change":
            if len(parts) < 4:
                self.view.display_message("Missing input")
            name = parts[1]
            old_phone = parts[2]
            new_phone = parts[3]
            self.view.display_message(self.change_phone(name, old_phone, new_phone))
            self.logger.info(f"Command: {name} changed {old_phone} to {new_phone}")

        elif parts[0].lower() == "phone":
            if len(parts) < 2:
                self.view.display_message("Missing input")
            name = parts[1]
            self.view.display_message(self.get_phone(name))
            self.logger.info(f"Command: {name} phone is {self.get_phone(name)}")

        elif (
            len(parts) >= 2 and parts[0].lower() == "show" and parts[1].lower() == "all"
        ):
            self.view.display_contacts(self.show_all())
            self.logger.info("Command: show all")

        elif parts[0].lower() == "birthday":
            if len(parts) < 3:
                self.view.display_message("Missing input")
            name = parts[1]
            birthday_str = parts[2]
            try:
                birthday = datetime.strptime(birthday_str, "%d-%m-%Y").date()
                birthday_field = Birthday(birthday)
                self.view.display_message(self.set_birthday(name, birthday_field))
            except ValueError:
                self.view.display_message(
                    "Invalid date format. Please use the format: DD-MM-YYYY"
                )
            self.logger.info(f"Command: {name} birthday at {birthday_str}")

        elif parts[0].lower() == "paginate":
            if len(parts) < 2:
                self.view.display_message("Missing input")
            page_size = int(parts[1])
            self.view.display_message(self.paginate_contacts(page_size))
            self.logger.info("Command: paginate")

        elif parts[0].lower() == "search":
            if len(parts) < 2:
                self.view.display_message("Missing input")
            search_query = " ".join(parts[1:])
            self.view.display_message(self.search_contacts(search_query))
            self.logger.info("Command: search")

        elif parts[0].lower() == "save":
            if len(parts) < 2:
                self.view.display_message("Missing input")
            filename = parts[1]
            self.view.display_message(self.save_address_book(filename))
            self.logger.info(f"Command: address book saved to {filename}")

        elif parts[0].lower() == "load":
            if len(parts) < 2:
                self.view.display_message("Missing input")
            filename = parts[1]
            self.view.display_message(self.load_address_book(filename))
            self.logger.info(f"Command: address book loaded from {filename}")

        elif parts[0].lower() in ["close", "exit"] or (
            len(parts) >= 2 and parts[0].lower() == "good" and parts[1].lower() == "bye"
        ):
            self.close_program()
            self.logger.info("Command: exit")
        else:
            self.view.display_message("Invalid command")
            self.logger.warning("Invalid command")

    def run_bot(self) -> None:
        self.view.display_message("Welcome to the assistant bot!")
        self.view.display_message("Type 'help' for list of commands.")
        while True:
            command = input("Enter command: ")
            self.handle_command(command)


if __name__ == "__main__":
    bot = BotAssistant()
    bot.run_bot()
