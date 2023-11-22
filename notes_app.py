import datetime


def input_title():
    return input("Введите название заметки: ")


def input_content():
    return input("Содержание заметки:\n")


def create_note(ID):
    ID += 1;
    title = input_title()
    content = input_content()
    date = datetime.date.today()
    str_contact = f"{ID};{title};{date};{content}\n"
    with open("notebook.csv", "a", encoding="UTF-8") as file:
        file.write(str_contact)
    return ID


def read_file():
    with open("notebook.csv", "r", encoding="UTF-8") as file:
        return file.read()


def print_notes():
    notebook_list = read_file().rstrip().split("\n")
    print("_______________________________________")
    for note_str in notebook_list:
        note_lst = note_str.split(";")
        print(f"Заметка: {note_lst[1]}\n(id: {note_lst[0]}, дата создания/изменения: {note_lst[2]})\n"
              f"Содержание:\n{note_lst[3]}")
        print("_______________________________________")


# вспомогательная функция для запроса параметров поиск записи: по какому полю и какое значение ищем
def ask_parameter():
    print("Параметры поиска:\n"
          "1) Заголовок\n"
          "2) Дата создания (изменения)\n")
    command = input("Укажите номер поля для поиска: ")
    while command not in ("1", "2"):
        print("Некорректный ввод!\n"
              "Повторите ввод\n")
        command = input("Укажите номер поля для поиска: ")
    print()
    i_search_param = int(command)
    search = input("Введите данные для поиска (для даты ГГГГ-ММ-ДД): ")
    return (search, i_search_param)  # возвращает искомое значение и индекс поля для поиска


def search_note():
    search, i_search_param = ask_parameter()
    notebook_list = read_file().rstrip().split("\n")
    print("_______________________________________")
    for note_str in notebook_list:
        note_lst = note_str.split(";")
        if search in note_lst[i_search_param]:
            print(f"Заметка: {note_lst[1]}\n(id: {note_lst[0]}, дата создания/изменения: {note_lst[2]})\n"
                  f"Содержание:\n{note_lst[3]}")
            print("_______________________________________")


def ask_change_field():  # вспомогательная функция для запроса параметров изменения контакта: какое поле и новое значение
    print("Какое поле контакта изменить:\n"
          "1) Фамилия\n"
          "2) Имя\n"
          "3) Отчество\n"
          "4) Телефон\n"
          "5) Адрес\n")
    command = input("Укажите номер поля: ")
    while command not in ("1", "2", "3", "4", "5"):
        print("Некорректный ввод!\n"
              "Повторите ввод\n")
        command = input("Укажите номер поля: ")
    print()
    i_change_field = int(command) - 1
    new_value = input("Введите новые данные для поля контакта: ").title()
    return (new_value, i_change_field)  # возвращает новое значение и индекс поля для изменения


def change_note():
    print("Укажите контакт для изменения\n")
    search, i_search_param = ask_parameter()
    phonebook_list: list = read_file().rstrip().split("\n\n")
    # new_phonebook = "" # для формирования нового экземпляра телефонной книги

    for i, contact_str in enumerate(phonebook_list):
        contact_lst = contact_str.replace("\n", " ").split()
        if search in contact_lst[i_search_param]:
            # спрашиваем подтверждение перед изменением контакта
            print(contact_str + "\n")
            command = input("Изменить найденный контакт (да \ нет): \n").lower()
            if command == "да":
                new_value, i_change_field = ask_change_field()  # получаем параметры для изменений
                contact_lst[i_change_field] = new_value  # перезаписываем поле контакта
                contact_lst[-1] = "\n" + contact_lst[-1]  # добавляем необходимые переносы для адреса и новой строки
                # new_phonebook += " ".join(contact_lst) # собираем телефонную книгу, приращивая каждый контакт
                phonebook_list[i] = " ".join(contact_lst)  # собираем телефонную книгу, приращивая каждый контакт

    with open("phonebook.txt", "w", encoding="UTF-8") as file:
        file.write("\n\n".join(phonebook_list) + "\n\n")
    print("_______________________________________\n")


def remove_note():
    print("Укажите контакт для удаления\n")
    search, i_search_param = ask_parameter()  # получаем от пользователя параметры для поиска контакта
    phonebook_list: list = read_file().rstrip().split("\n\n")
    contacts_to_del = []  # используем список, т.к. может быть больше 1 контакта, подходящего под параметры поиска

    for contact_str in phonebook_list:
        contact_lst = contact_str.replace("\n", " ").split()
        if search in contact_lst[i_search_param]:
            # спрашиваем подтверждение перед удалением контакта
            print(contact_str + "\n")
            command = input("Подтвердите удаление найденного контакта (да \ нет): \n").lower()
            if command == "да":
                contacts_to_del.append(contact_str)  # добавляем контакт в список для удаления

    for contact in contacts_to_del:
        phonebook_list.remove(contact)  # удаляем все отобранные контакты

    with open("phonebook.txt", "w", encoding="UTF-8") as file:
        for contact_str in phonebook_list:
            file.write(contact_str + "\n\n")  # перезаписываем телефонную книгу
    print("_______________________________________\n")


def interface():
    with open("notebook.csv", "a", encoding="UTF-8"):
        pass
    ID = None;
    notebook_list = read_file().rstrip().split("\n")
    if len(notebook_list) > 1:
        ID = int(notebook_list.pop().split(";")[0])
    else:
        ID = 0
    command = ""
    print("""
======================================
        Приложение \"Заметки\"
======================================""")
    while command != "6":
        print("""
Главное меню:
1) Создать заметку
2) Показать список заметок
3) Найти заметку
4) Изменить заметку
5) Удалить заметку
6) Выход
_______________________________________""")
        command = input("Укажите номер действия: ")
        while command not in ("1", "2", "3", "4", "5", "6"):
            print("Некорректный ввод!\n")
            command = input("Повторно укажите номер действия: ")
        print()

        match command:
            case "1":
                ID = create_note(ID)
            case "2":
                print_notes()
            case "3":
                search_note()
            case "4":
                change_note()
            case "5":
                remove_note()
            case "6":
                print("======================================\n"
                      "           Приложение закрыто\n"
                      "======================================""")


if __name__ == "__main__":
    interface()
