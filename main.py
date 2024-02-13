from collections import UserDict
from datetime import datetime, date
import pickle


class Field:
    def __init__(self, value):
        self._value = value

    def get_value(self):
        return self._value

    def set_value(self, new_value):
        self._value = new_value

    def __str__(self):
        return str(self._value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.valid_phone()

    def valid_phone(self):
        if len(self._value) != 10 or not self._value.isdigit():
            raise ValueError


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        self.valid_birthday()

    def valid_birthday(self):
        if not isinstance(self._value, str):
            raise ValueError("Error! Valid format for date of birth is DD-MM-YYYY")
        try:
            datetime.strptime(self._value, "%d-%m-%Y")
        except ValueError:
            raise ValueError("Error! Valid format for date of birth is DD-MM-YYYY")


class Record:
    def __init__(self, name: Name, birthday: Birthday = None):
        self.name = name
        self.phones = []

        if birthday:
            self.birthday = str(birthday)

    def days_to_birthday(self):
        today = date.today()
        birthday_day, birthday_month, birthday_year = self.birthday.split('-')
        birthday_day, birthday_month, birthday_year = int(birthday_day), int(birthday_month), int(birthday_year)
        next_birthday = date(year=today.year, month=birthday_month, day=birthday_day)

        if today > next_birthday:
            next_birthday = date(year=today.year + 1, month=birthday_month, day=birthday_day)

        days_until_birthday = (next_birthday - today).days
        return days_until_birthday

    def add_phone(self, phone_number: str):
        phone = Phone(phone_number)
        phone.valid_phone()
        self.phones.append(phone)

    def remove_phone(self, phone_number: str):
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                return

    def edit_phone(self, old_phone: str, new_phone: str):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                return
        raise ValueError('Invalid phone number')

    def find_phone(self, phone_number: str):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone

    def __str__(self):
        return f"Contact name: {self.name}, phones: {'; '.join(p._value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name] = record

    def find(self, found_name: Name):
        for name, record in self.data.items():
            if name == found_name:
                return record

    def delete(self, deleted_name: Name):
        if deleted_name in self.data.keys():
            del self.data[deleted_name]

    def iterator(self, n):
        iteration_list = list(self.data.values())
        for i in range(0, len(iteration_list), n):
            yield iteration_list[i: i + n]

    def searching(self, keyword):
        result = ''
        for k, v in self.data.items():
            if keyword.lower() in v.name.lower() or keyword in '; '.join(p._value for p in v.phones):
                result += f"{k}: {v}\n"
        return repr('No contact with such code word') if (result == '') else result

    def __str__(self):
        result = ''
        for k, v in self.data.items():
            result += f"{k}: {v}\n"
        return result


def save_address_book(filename, address_book: AddressBook):
    try:
        with open(filename, 'wb') as file:
            pickle.dump(address_book, file)
            print("Address book dumped successfully.")
    except IOError:
        print("Error: Failed to save the address book.")


def load_address_book(filename):
    try:
        with open(filename, 'rb') as file:
            address_book = pickle.load(file)
            print("Address book loaded successfully.")
            return address_book
    except (IOError, pickle.UnpicklingError):
        print("Error: Failed to load the address book")


if __name__ == "__main__":
    book = AddressBook()

    john_record = Record("John", '10-3-1991')
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    book.add_record(john_record)

    poul_record = Record("Poul")
    poul_record.add_phone("9876783210")
    book.add_record(poul_record)

    ana_record = Record("Ana")
    ana_record.add_phone("9876543210")
    book.add_record(ana_record)

    nadia_record = Record("Nadia")
    nadia_record.add_phone("9876543210")
    book.add_record(nadia_record)

    rood_record = Record("Rood")
    rood_record.add_phone("9876543210")
    book.add_record(rood_record)
    print(book.searching('Ro'))

    save_address_book('address_book.pkl', book)

    load_address_book('address_book.pkl')
