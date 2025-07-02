import random

name = ["Алина", "Самира", "Лина", "Лия"]
age = ["10", "20", "30", "40"]
name2 = ["Руслан", "Даня", "Игорь", "Феликс"]
city = ["Казань", "Москва", "Углич", "Киров"]
country = ["Россия", "Америка", "Израиль", "Украина", "США"]

history = [
    f"{name2[random.randint(0, len(name2) - 1)]} неожиданно встретил свою первую любовь, {name[random.randint(0, len(name) - 1)]}, после {age[random.randint(0, len(age) - 1)]} лет разлуки.",
    f"{name[random.randint(0, len(name) - 1)]} в {age[random.randint(0, len(age) - 1)]} лет нашла работу своей мечты в {city[random.randint(0, len(city) - 1)]}, стала успешным дизайнером.",
    f"{name2[random.randint(0, len(name2) - 1)]} из {country[random.randint(0, len(country) - 1)]}, спас котенка из горящего здания и стал местным героем.",
    f"{age[random.randint(0, len(age) - 1)]}  {name[random.randint(0, len(name) - 1)]} из {country[random.randint(0, len(country) - 1)]}, открыла новый способ лечения редкой болезни.",
    f"{age[random.randint(0, len(age) - 1)]} {name2[random.randint(0, len(name2) - 1)]} из {city[random.randint(0, len(city) - 1)]}, после долгой работы, наконец смог уйти в отставку и отправился путешествовать.",
]

num = random.randint(0, len(history) - 1)
print(history[num])

