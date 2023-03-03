import datetime

from tinydb import TinyDB, Query

import bullet
import dates

def test_monthly_log():

    journal = TinyDB("/tmp/test.json")
    entries = Query()

    journal.remove(entries.description.matches(".*"))
    journal.insert({'description': "previous month task", 'date': "2023-02-03", 'position': "1"})
    journal.insert({'description': "task unscheduled", 'date': "", 'position': "2"})
    journal.insert({'description': "next month task", 'date': "2023-04-03", 'position': "3"})
    journal.insert({'description': "this month task", 'date': today, 'position': "4"})

    future_log = bullet.future_log(journal)

    assert len(future_log) == 1
    assert future_log[0]['description'] == "task unscheduled"

def test_monthly_log():

    tm = dates.this_month()
    today = dates.get_today()

    journal = TinyDB("/tmp/test.json")
    entries = Query()

    monthly_log = bullet.monthly_log(journal)
    
    assert len(monthly_log) == 1
    assert monthly_log[0]['description'] == "this month task"