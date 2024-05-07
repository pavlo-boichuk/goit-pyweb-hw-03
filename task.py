from collections import UserDict
from datetime import datetime, timedelta
import pickle
from abc import ABC, abstractmethod


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено


class Field(ABC):
    def __init__(self, value):
        self.value = value

    @abstractmethod
    def __str__(self):
        pass


class Name(Field):
    def __str__(self):
        return str(f'Value: {self.value}')


class Phone(Field):
    def __init__(self, value):
        super().__init__(value) # check?
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        if len(value) == 10 and value.isdigit():
            self.__value = value
        else:
            raise ValueError(f'Вказаний номер телефону [{value}] не містить 10 цифр') # !!!
        
    def __str__(self):
        return str(f'Value: {self.value}')


class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
            # super().__init__(value) # check?
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
    
    def __str__(self):
        return str(f'Value: {self.value}')


class AbstractRecord(ABC):

    @abstractmethod
    def add_phone(self):
        pass

    @abstractmethod
    def find_phone(self):
        pass

    @abstractmethod
    def remove_phone(self):
        pass

    @abstractmethod
    def edit_phone(self):
        pass


class Record(AbstractRecord):
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_phone(self, phone_number):
        try:
            self.phones.append(Phone(phone_number))
        except ValueError as e:
            print(e)

    def find_phone(self, phone_number):
        for el in self.phones:
            if el.value == phone_number:
                return el
        return f'Не знайдено номер телефону [{phone_number}]'

    def remove_phone(self, phone_number):
        self.phones = [el for el in self.phones if el.value != phone_number]

    def edit_phone(self, phone_number, new_phone_number):
        for el in self.phones:
            if el.value == phone_number:
                el.value = new_phone_number
    
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, record_name):
        return self.data.get(record_name)

    def delete(self, record_name):
        del self.data[record_name]

    @staticmethod
    def find_next_weekday(date, weekday):
        day_ahead = weekday - date.weekday()
        if day_ahead <= 0:
            day_ahead += 7
        return date + timedelta(days=day_ahead)

    def get_upcoming_birthdays(self):
        greeting_period = 7 # період контролю привітань на 7 днів
        today = datetime.today().date()
        upcoming_birthdays = [] # список для зберігання користувачів, яких потрібно привітати

        for name, record in self.data.items():
            birthday_this_year = record.birthday.value.replace(year=today.year) # конвертуємо рік народження в поточний рік # 1985 -> 2024
            
            if birthday_this_year < today: # якщо день народження вже минув в цьому році
                birthday_this_year = birthday_this_year.replace(year=today.year + 1) # то розглянути дату на наступний рік
            
            if 0 <= (birthday_this_year - today).days <= greeting_period:
                if birthday_this_year.weekday() >= 5: # якщо випадає на субота, неділя
                    birthday_this_year = AddressBook.find_next_weekday(birthday_this_year, 0) # то переносимо привітання на понеділок

                congratulation_date_str = birthday_this_year.strftime("%Y.%m.%d")
                upcoming_birthdays.append({"name": name, "congratulation_date": congratulation_date_str})
            
        return upcoming_birthdays


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Enter user name."
        except KeyError:
            return "Contact not found! Enter new one."

    return inner

def input_error_birthday(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and correct birthdays please."
        except IndexError:
            return "Enter user name."
        except KeyError:
            return "Contact not found! Enter new one."

    return inner


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    
    return message


@input_error
def change_contact(args, book):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    
    if record is None:
        message = f"Contact [{name}] not found!"
    if old_phone and new_phone:
        record.edit_phone(old_phone, new_phone)
    else:
        message = "Give me correct phones please."
    return message


@input_error
def show_phone(args, book):
    name, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found! Enter new one."
    return record


def show_all(book):
    contacts = []
    for name, record in book.data.items():
        contacts.append(str(record))
    return contacts


@input_error_birthday
def add_birthday(args, book):
    name, birthday, *_ = args
    record = book.find(name)
    message = "Birthday added."
    
    if record is None:
        return "Contact not found! Enter new one."
    if birthday:
        record.add_birthday(birthday)
    
    return message


@input_error_birthday
def show_birthday(args, book):
    name, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found! Enter new one."
    return record.birthday


def birthdays(book):
    return book.get_upcoming_birthdays()


def main():
    book = load_data() # book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book)) 
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))    
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book)) 
        elif command == "birthdays":
            print(birthdays(book))         
        else:
            print("Invalid command.")

    save_data(book)


if __name__ == "__main__":
    main()