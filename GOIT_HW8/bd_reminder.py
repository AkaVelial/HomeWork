import datetime


def is_leap_year(year):
    """Проверяет, является ли год высокосным."""
    if year % 4 != 0:
        return False
    elif year % 100 != 0:
        return True
    elif year % 400 != 0:
        return False
    else:
        return True


def get_birthdays_per_week(users):
    # Получаем текущую дату
    today = datetime.date.today()

    # Определяем день недели, с которого начинается текущая неделя (понедельник)
    start_of_week = today - datetime.timedelta(days=today.weekday())

    # Определяем день недели, на котором наступит следующий понедельник
    next_monday = start_of_week + datetime.timedelta(days=7)

    # Создаем словарь, где ключи — дни недели, значения — списки именниников
    birthdays_per_week = {
        'Monday': [],
        'Tuesday': [],
        'Wednesday': [],
        'Thursday': [],
        'Friday': [],
        'Saturday': [],
        'Sunday': []
    }

    # Проходимся по каждому пользователю
    for user in users:
        name = user['name']
        birthday = user['birthday'].date()  # Преобразуем дату рождения в тип datetime.date

        # Определяем день недели дня рождения
        birthday_weekday = birthday.weekday()

        # Проверяем, попадает ли день рождения пользователя в текущую неделю или на следующей неделе
        if start_of_week <= birthday <= next_monday or (birthday_weekday >= 5 and birthday < next_monday):
            # Определяем день недели, на который нужно поздравить пользователя
            if birthday_weekday >= 5:  # Если день рождения выпадает на субботу или воскресенье
                weekday = 'Monday'  # Поздравляем в понедельник
            else:
                weekday = datetime.date.strftime(birthday, '%A')

            birthdays_per_week[weekday].append(name)
    # Возвращаем именниников по дням недели
    return birthdays_per_week
    # Выводим именниников по дням недели
    for weekday, names in birthdays_per_week.items():
        if names:
            print(f"{weekday}: {', '.join(names)}")


# Пример использования функции

users = [
    {'name': 'Alice', 'birthday': datetime.datetime(2023, 5, 15)},
    {'name': 'Bob', 'birthday': datetime.datetime(2023, 5, 16)},
    {'name': 'Charlie', 'birthday': datetime.datetime(2023, 5, 17)},
    {'name': 'David', 'birthday': datetime.datetime(2023, 5, 18)},
    {'name': 'Eve', 'birthday': datetime.datetime(2023, 5, 20)},
    {'name': 'Dew', 'birthday': datetime.datetime(2023, 5, 21)},
    {'name': 'Buddy', 'birthday': datetime.datetime(2023, 5, 22)},
    {'name': 'Joe', 'birthday': datetime.datetime(2023, 5, 23)}
]

get_birthdays_per_week(users)
