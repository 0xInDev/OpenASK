import datetime

one_day = datetime.timedelta(days=1)


def get_week(date):
    """Return the full week (Sunday first) of the week containing the given date.

    'date' may be a datetime or date instance (the same type is returned).
    """
    day_idx = (date.weekday()+2) % 7  # 7 turn sunday into 0, monday into 1, etc.
    saturday = date - datetime.timedelta(day_idx) #saturday
    date = saturday
    data = []
    for n in range(7):
        data.append(date)
        date += one_day
    print(data)
    return data


def get_week_name(mon, sun):
    return 'Le {} {} - {} {} {}'.format(mon.day, mon.strftime("%b"), sun.day, sun.strftime("%b"), sun.year)
