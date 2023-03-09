from tinydb import Query

import dates

def future_log(journal):
    future_log = []

    entries = Query()

    for entry in sorted(journal.search(entries.date == ""), key=lambda k: k['position']):
        future_log.append(entry)
    return future_log

def monthly_log(journal):
    monthly_log = []
    entries = Query()

    for entry in sorted(journal.search(entries.date.search(dates.this_month())), key=lambda k: k['position']):
        monthly_log.append(entry)
    return monthly_log

def weekly_log(journal):
    weekly_log = []
    entries = Query()

    for entry in sorted(journal.search(entries.date.test(lambda d: len(d) and dates.week(d) == dates.this_week())), key=lambda k: k['position']):
        weekly_log.append(entry)
    return weekly_log