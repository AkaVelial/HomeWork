from datetime import datetime, timedelta


users = [
    {'name': 'Rina', 'birthday': datetime(1989, 4, 17)},
    {'name': 'Marina', 'birthday': datetime(1995, 4, 18)},
    {'name': 'Sabrina', 'birthday': datetime(2000, 4, 19)},
    {'name': 'Alina', 'birthday': datetime(1985, 4, 20)},
    {'name': 'Irina', 'birthday': datetime(1998, 4, 21)},
    {'name': 'Karina', 'birthday': datetime(1990, 4, 22)},
    {'name': 'Angelina', 'birthday': datetime(1987, 4, 23)},
]


def get_birthdays_per_week(users):
    today = datetime.today()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    birthdays = [[] for _ in range(7)]

    for user in users:
        birthday = user['birthday'].replace(year=today.year)
        if birthday < today:
            birthday = birthday.replace(year=today.year + 1)
        days_to_birthday = (birthday - today).days
        if days_to_birthday < 0 or days_to_birthday >= 7:
            continue
        index = (birthday.weekday() + 1) % 7
        birthdays[index].append(user['name'])

    for i in range(7):
        weekday = week_start + timedelta(days=i-1)
        weekday_name = weekday_names[i-1]
        if weekday > week_end or weekday.weekday() in [5, 6]:
            continue
        birthday_list = ', '.join(birthdays[i])
        if birthday_list:
            print(f"{weekday_name}: {birthday_list}")


if __name__ == '__main__':
    get_birthdays_per_week(users)
