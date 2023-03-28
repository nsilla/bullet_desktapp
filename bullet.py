import datetime

from tinydb import Query

import dates

entries = Query()

def check_date(date, year, month, day):
    return date["year"] == year and date["month"] == month and date["day"] == day

def check_done(state, done):
    return done or state in ["", "pending"]

def check_future(date):
    return date["year"] == "" and date["month"] == "" and date["day"] == "" and date["week"] == ""

def check_kind(kind, tasks, notes, events):
    return (kind == 'task' and tasks or
            kind == 'note' and notes or
            kind == 'event' and events)

def check_month(date, month):
    return date["year"] == str(month[0]) and date["month"] == str(month[1])

def check_overdue(date, year, month, day):
    date_check = datetime.datetime(year=int(date["year"]), month=int(date["month"]), day=int(date["day"]))
    date_reference = datetime.datetime(year=int(year), month=int(month), day=int(day))
    return date_check < date_reference


def daily_log(journal, tasks=True, notes=True, events=True):
    daily_log = []
    today = dates.get_today()
    for entry in journal.search(
            (entries.date.test(check_date, today["year"], today["month"], today["day"])) &
            (entries.kind.test(check_kind, tasks, notes, events))):
        daily_log.append(entry)
    return sorted(daily_log, key=lambda k: k['position'])

def future_log(journal):
    future_log = []

    for entry in journal.search(entries.date.test(check_future)):
        future_log.append(entry)
    return sorted(future_log, key=lambda k: k['position'])

def monthly_log(journal, month=None, tasks=True, notes=True, events=True, done=True):
    monthly_log = []
    month = month if month else dates.this_month()
    for entry in journal.search(
                    (entries.date.test(check_month, month)) &
                    (entries.kind.test(check_kind, tasks, notes, events) &
                     (entries.state.test(check_done, done)))):
        monthly_log.append(entry)
    return sorted(monthly_log, key=lambda k: k['position'])

def overdue(journal, dates_before=None):
    today = dates.get_today()
    year, month, day = (dates_before["year"], dates_before["month"], dates_before["day"]) if dates_before else (today["year"], today["month"], today["day"])
    overdue = journal.search(
        (~ entries.date.test(check_future)) &
        (entries.date.test(check_overdue, year, month, day)) &
        (entries.kind == "task") &
        (entries.state == "pending"))
    return sorted(overdue, key=lambda k: k['position'])

def weekly_log(journal, week=None, tasks=True, notes=True, events=True, done=True):
    weekly_log = []
    def check_week(date, week):
        return (
            len(date["year"]) and 
            len(date["month"]) and 
            len(date["day"]) and 
            len(date["week"]) and 
            dates.week(date) == (week if week else dates.this_week()))
    for entry in journal.search(
            (entries.date.test(check_week, week)) &
            (entries.kind.test(check_kind, tasks, notes, events)) &
            (entries.state.test(check_done, done))):
        weekly_log.append(entry)
    return sorted(weekly_log, key=lambda k: k['position'])