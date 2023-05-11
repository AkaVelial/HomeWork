import datetime

def birthday_this_week():
    today = datetime.date.today()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    end_of_week = start_of_week + datetime.timedelta(days=6)
    next_monday = start_of_week + datetime.timedelta(days=7)
    birthdays = []
    for name, birthday in birthday_dict.items():
        if start_of_week <= birthday.date() <= end_of_week:
            birthdays.append((name, birthday))
        elif next_monday <= birthday.date() <= end_of_week + datetime.timedelta(days=7):
            birthdays.append((name, birthday))
    return birthdays

birthday_dict = {'Person 1': datetime.date(2004, 5, 12),
                 'Person 2': datetime.date(2000, 5, 13),
                 'Person 3': datetime.date(1996, 5, 18),
                 'Person 4': datetime.date(1992, 5, 16)}

print(birthday_this_week())
