import random
import datetime
import json

login = '12345'
user = input('Введи логин: ')
while user != login:
    print('Неверный логин ')
    user = input('Введи логин: ')
password = 'lika'
user = input('Введи пароль: ')
while user != password:
    print('Неверный пароль ')
    user = input('Введи пароль: ')
else:
    print('Вход выполнен ')

name = input('Как тебя зовут? ')
print('Приятно познакомиться ', name)
print('1 - Узнать время ')
print('2 - Узнать дату ')

answer = int(input('Чем тебе помочь? ') )

if answer == 1:
    date_time = datetime.datetime.now()
    print('Текущее время:', date_time.time())

if answer == 2:
    date_time = datetime.datetime.now()
    print('Сегоднящняя дата:', date_time.date())

print('1 - Первая игра')
print('2 - Вторая игра')
print('3 - Третья игра')
print('4 - Таблица умножения')
print('5 - Заметки')
answer = int(input('Чем тебе помочь?'))

if answer == 1:
    list = ['Орел', 'Решка']
    print('Добро пожаловать в игру орел - решка')
    print('Выбери один из вариантов:')
    print(f'1 - {list[0]} \n 2 - {list[1]}')
    user = int(input('Ваш выбор (Введи одно число от 1 до 2):'))
    user = list[user - 1]
    print('Ваш выбор: ' + user)
    bot = random.randint(1, 2)
    bot = list[bot - 1]
    print('Ваш бот:' + bot)
    if user == bot:
        print('Ничья')
    elif (user == 'решка' and bot == 'орел') or (user == 'орел' and bot == 'решка'):
        print('Победа!')
    else:
        print('Проигрыш')

if answer == 2:
    list = ['Камень', 'Ножницы', 'Бумага']
    print('Добро пожаловать в игру Камень-ножницы-бумага')
    print('Выбери один из вариантов:')
    print(f'1 - {list[0]} \n 2 - {list[1]} \n 3 - {list[2]}')
    user = int(input('Ваш выбор (Введи одно чесло от 1 до 3):'))
    user = list[user - 1]
    print('Ваш выбор: ' + user)
    bot = random.randint(1, 3)
    bot = list[bot - 1]
    print('Ваш бот:' + bot)
    if user == bot:
        print('Ничья')
    elif (user == 'камень' and bot == 'ножницы') or (user == 'ножницы' and bot == 'бумага') or (
            user == 'бумага' and bot == 'камень'):
        print('Победа!')
    else:
        print('Проигрыш:( ')

if answer == 3:
    number = random.randint(1, 100)
    lives = 5
    while True:
        guess = int(input('Угадай число от 1 до 100 '))
        lives -= 1
        if lives <= 0:
            print('Вы проиграли :(')
            break
        if guess > number:
            print('Слишком большое число, попробуй еще раз!')
        elif guess < number:
            print('Ты глупый? Слишком маленькое число, попробуй еще раз!')
        elif guess < number:
            print('О господи! Ты дурак или как? Слишком маленькое число, попробуй еще раз!')
        elif guess > number:
            print('Как тебе объяснить? СЛИШКОМ БОЛЬШОЕ ЧИСЛО, ну давай еще раз!')
        else:
            print('Ну наконец-то. Поздравляю, ты победил!')
            break

if answer == 4:
    for num1 in range(1, 10):
        for num2 in range(1, 10):
            print(f'{num1} * {num2} = {num1 * num2}')
        print('----------')

if answer == 5:
    notes = dict()

    def add_note(title, text):
        notes[title] = text
        print("Заметка успешно добавлена!")

    def update_notes():
        global notes
        with open('notes.json', 'r') as json_file:
            notes = json.load(json_file)
    def display_notes():
        update_notes()
        if len(notes) == 0:
            print("Заметок пока нет.")
        else:
            for title, text in notes.items():
                print(f"{title}: {text}")

    def delete_note(title):
        if title in notes.keys():
            del notes[title]
            print(f'Запись {title} удалена')
        else:
            print('Записи не существует')

    def save_notes():
        with open("user_info.json", "w") as file:
            json.dump(notes, file)

    def main():
        while True:
            print("\n1. Добавить заметку\n2. Просмотреть все заметки\n3. Удалить заметку\n4. Выйти")
            choice = input("Выберите действие: ")
            if choice == "1":
                note_title = input("Введите название заметки: ")
                note_text = input("Введите текст заметки: ")
                add_note(note_title, note_text)
                save_notes()
            elif choice == "2":
                display_notes()
            elif choice == "3":
                update_notes()
                for title in notes.keys():
                    print(title)
                title_to_del = input('Введи название заметки для удаления: ')
                delete_note(title_to_del)
                save_notes()
            elif choice == "4":
                break
            else:
                print("Некорректный ввод. Повторите попытку.")
main()