import datetime

from tinydb import TinyDB, Query

import bullet
import dates

def test_future_log():

    journal = TinyDB("/tmp/test.json")
    entries = Query()

    tw = dates.this_week()
    this_monday = str(datetime.datetime.strptime('%s %s 1' % (tw[0], tw[1]), '%G %V %u').date())
    last_sunday = str(datetime.datetime.strptime('%s %s 7' % (tw[0], tw[1]-1), '%G %V %u').date())
    next_monday = str(datetime.datetime.strptime('%s %s 1' % (tw[0], tw[1]+1), '%G %V %u').date())

    journal.remove(entries.description.matches(".*"))
    journal.insert({'description': "previous month task", 'date': "2023-02-03", 'position': "1"})
    journal.insert({'description': "task unscheduled", 'date': "", 'position': "2"})
    journal.insert({'description': "next month task", 'date': "2023-04-03", 'position': "3"})
    journal.insert({'description': "today's task", 'date': dates.get_today(), 'position': "4"})
    journal.insert({'description': "last week task", 'date': last_sunday, 'position': "5"})
    journal.insert({'description': "next week task", 'date': next_monday, 'position': "6"})
    journal.insert({'description': "this week task", 'date': this_monday, 'position': "7"})

    future_log = bullet.future_log(journal)

    assert len(future_log) == 1
    assert future_log[0]['description'] == "task unscheduled"

def test_monthly_log():

    tm = dates.this_month()
    today = dates.get_today()

    journal = TinyDB("/tmp/test.json")
    entries = Query()

    monthly_log = bullet.monthly_log(journal)
    
    assert len(monthly_log) >= 1
    assert monthly_log[0]['description'] == "today's task"

def test_weekly_log():

    tm = dates.this_month()
    today = dates.get_today()

    journal = TinyDB("/tmp/test.json")
    entries = Query()

    weekly_log = bullet.weekly_log(journal)
    
    assert len(weekly_log) == 2
    assert weekly_log[-1]['description'] == "this week task"