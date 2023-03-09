import datetime

def get_begining_of_month():
    return get_today()[:-2] + '01'

def get_end_of_month():
    return get_today()[:-2] + '31'

def get_today():
    return str(datetime.date.today())

def test_future(date):
    return date == '' or (str(date) >= str(get_begining_of_month()) and str(date) <= str(get_end_of_month()))

def this_month():
    return get_today()[:-3]

def this_week():
    iso = datetime.date.today().isocalendar()
    return iso[0:2]

def week(date):
    iso = datetime.datetime.strptime(date, "%Y-%m-%d").isocalendar()
    return iso[0:2]