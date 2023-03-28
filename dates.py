import datetime

def get_begining_of_month():
    return get_today()[:-2] + '01'

def get_end_of_month():
    return get_today()[:-2] + '31'

def get_today():
    today = datetime.datetime.today()
    return {"year": str(today.year), "month": str(today.month), "day": str(today.day), "week": str(today.isocalendar()[1])}

def test_future(date):
    return date == '' or (str(date) >= str(get_begining_of_month()) and str(date) <= str(get_end_of_month()))

def this_month():
    today = get_today()
    return (today["year"], today["month"])

def this_week():
    today = get_today()
    return (today["year"], today["week"])

def week(date):
    return (date["year"], date["week"])