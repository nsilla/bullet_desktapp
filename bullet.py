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
    def check_overdue(date):
        return len(date) and date < (reference if reference else dates.get_today())
    overdue = journal.search(
        (entries.date != '') &
        (entries.date < (reference if reference else dates.get_today())) &
        (entries.kind == "task") &
        (entries.state == "pending"))
    return sorted(overdue, key=lambda k: k['position'])

def weekly_log(journal):
    weekly_log = []
    for entry in sorted(journal.search(entries.date.test(lambda d: len(d) and dates.week(d) == dates.this_week())), key=lambda k: k['position']):
        weekly_log.append(entry)
    return weekly_log