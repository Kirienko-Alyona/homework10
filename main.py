from address_book import AddressBook, Record


contacts_dict = AddressBook()


def input_error(func):
    """
    Декоратор для обробки помилок при виконанні команд бота
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "This name is wrong"
        except ValueError as exception:
            return exception.args[0]
        except TypeError:
            return "I don't know this command" 
        except IndexError:
            return "Please, print name and phone"   

    return inner


@input_error
def hello_func():
    """
    Ввічливий бот, вміє вітатися
    """
    
    return "How can I help you?"


@input_error
def add_func(data):
    """
    Додає дані (ім'я та номер телефону) до списку контактів
    """
    name, phones = validation_data(data)

    record = Record(name)
    for phone in phones:
        if phone in contacts_dict:
            raise IndexError("Phone number is in contacts")
        else:
            record.add_phone(phone) 
    contacts_dict.add_record(record)       
    
    return f"Your new contact added: {name} {phones}" 


@input_error
def change_phone_func(data):
    """
    Змінює номер телефону за ім'ям контакта
    """
    name, phones = validation_data(data)
    record = contacts_dict[name]
    record.change_phones(phones)

    return f"The phone number changed."


@input_error
def phone_search_func(value):
    """
    Повертає номер телефону за ім'ям контакта
    """
 
    return contacts_dict.search(value.strip()).get_info()


@input_error
def delete_func(name):
    """
    Функція видаляє контакт за ім'ям
    """ 
    name = name.strip()
    contacts_dict.remove_record(name)

    return f"The contact {name} deleted" 


@input_error
def delete_phone_func(data):
    """
    Функція видаляє номер телефону контакту за ім'ям і номером
    """   
    name, phone = data.strip().split(" ")
    record = contacts_dict[name]
    if record.delete_phone(phone):
        return f"Phone number {phone} for contact {name} deleted"
    else:
        return f"Contact {name} doesn't have this phone number"


@input_error
def show_all_func():
    """
    Виводить на екран весь список контантів
    """
    contacts = ""
    if contacts_dict:
        for key, record in contacts_dict.get_all_record().items():
            contacts += f"{record.get_info()}\n"
    else:
        raise ValueError("Your contacts list is empty") 
   
    return contacts


@input_error
def exit_func():
    """
    Закінчення роботи бота
    """
    return "Good bye!"


BOT_COMMANDS = {
    "hello": hello_func,
    "add": add_func,
    "change": change_phone_func,
    "phone": phone_search_func,
    "delete phone": delete_phone_func,
    "delete": delete_func,
    "show all": show_all_func,
    "good bye": exit_func,
    "close": exit_func,
    "exit": exit_func
    }   


def bot_answer_func(question):
    """
    Функція повертає відповідь бота
    """
    return BOT_COMMANDS.get(question, incorrect_input_func)


def incorrect_input_func():
    """
    Функція корректної обробки невалідних команд для бота
    """
    return ValueError("I don't know this command. Try again.") 


def input_func(input_string):
    """
    Функція відокремлює слово-команду для бота
    """
    command = input_string
    data = ""
    for key in BOT_COMMANDS:
        if input_string.strip().lower().startswith(key):
            command = key
            data = input_string[len(command):]
            break
    if data:
        return bot_answer_func(command)(data)
    
    return bot_answer_func(command)()


def validation_data(data):
    """
    Функція перевіряє чи другим значенням введено ім'я, а третім номер телефону
    """
    name, *phones = data.strip().split(" ") 
  
    if name.isnumeric():
        raise ValueError("Name must be in letters")
    for phone in phones:
        if not phone.isnumeric():
            raise ValueError("Phone must be in numbers")   
    
    return name, phones


def main():
    """
    Користувач вводить команду для бота або команду, ім'я, номер телефону через пробіл
    Функція повертає відповідь бота
    Бот завершує роботу після слів "good bye" або "close" або "exit"
    """
    while True:
        input_string = input("Input command, please: ")
        get_command = input_func(input_string)
        print(get_command)
        if get_command == "Good bye!":
            break

    return           


if __name__ == '__main__':
    main()    