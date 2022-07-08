import rw_json
from datetime import date
from calendar import monthrange


def set_limit(limit):
    data = rw_json.read_json()
    data['limit'] = limit
    rw_json.write_json(data)


def get_limit():
    data = data = rw_json.read_json()
    limit = data['limit']

    return limit

def autolimit(balance):
    month = date.today().month
    year = date.today().year
    day = date.today().day
    days = monthrange(year, month)[1]
    days_left = days - day + 1
    limit = balance/days_left

    set_limit(limit)

    return limit