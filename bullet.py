from tinydb import Query

import dates

entries = Query()

def future_log(journal):
    future_log = []

    for entry in sorted(journal.search(entries.date == ""), key=lambda k: k['position']):
        future_log.append(entry)
    return future_log

def monthly_log(journal):
    monthly_log = []
    for entry in sorted(journal.search(entries.date.search(dates.this_month())), key=lambda k: k['position']):
        monthly_log.append(entry)
    return monthly_log

def overdue(journal, reference=None):
    return sorted(journal.search(entries.date.test(lambda d: len(d) and d < (reference if reference else dates.get_today()))), key=lambda k: k['position'])

def weekly_log(journal):
    weekly_log = []
    for entry in sorted(journal.search(entries.date.test(lambda d: len(d) and dates.week(d) == dates.this_week())), key=lambda k: k['position']):
        weekly_log.append(entry)
    return weekly_log