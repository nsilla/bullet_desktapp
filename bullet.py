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