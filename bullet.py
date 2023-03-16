from tinydb import Query

import dates

entries = Query()

def check_kind(kind, tasks, notes, events):
    return (kind == 'task' and tasks or
            kind == 'note' and notes or
            kind == 'event' and events)
        
def daily_log(journal, tasks=True, notes=True, events=True):
    daily_log = []

    for entry in sorted(
        journal.search(
            (entries.date == dates.get_today()) & 
            (entries.kind.test(check_kind, tasks, notes, events))),
        key=lambda k: k['position']):
        daily_log.append(entry)
    return daily_log

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

def overdue(journal, dates_before=None):
    def check_overdue(date):
        return len(date) and date < (dates_before if dates_before else dates.get_today())
    overdue = journal.search(
        (entries.date != '') &
        (entries.date < (dates_before if dates_before else dates.get_today())) &
        (entries.kind == "task") &
        (entries.state == "pending"))
    return sorted(overdue, key=lambda k: k['position'])

def weekly_log(journal, week=None, tasks=True, notes=True, events=True):
    weekly_log = []
    def check_week(date, week):
        return len(date) and dates.week(date) == (week if week else dates.this_week())
    for entry in sorted(journal.search(entries.date.test(check_week, week) & entries.kind.test(check_kind, tasks, notes, events)), key=lambda k: k['position']):
        weekly_log.append(entry)
    return weekly_log