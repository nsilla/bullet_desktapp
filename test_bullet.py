import datetime
import json
import yaml

from tinydb import TinyDB, Query

import bullet
import dates

def test_future_log():

    tw = datetime.datetime.today().isocalendar()[0:2]
    this_monday = str(datetime.datetime.strptime('%s %s 1' % (tw[0], tw[1]), '%G %V %u').date())
    last_month = str(datetime.datetime.fromtimestamp(datetime.datetime.today().timestamp()-31*24*60*60).date())
    next_month = str(datetime.datetime.fromtimestamp(datetime.datetime.today().timestamp()+31*24*60*60).date())
    last_week = str(datetime.datetime.fromtimestamp(datetime.datetime.today().timestamp()-7*24*60*60).date())
    next_week = str(datetime.datetime.fromtimestamp(datetime.datetime.today().timestamp()+7*24*60*60).date())

    journal_yaml = '''
_default:
  1:
    description: previous month event
    date: "{last_month}"
    position: 1
    kind: event
  2:
    description: previous month note
    date: "{last_month}"
    position: 1
    kind: note
  3:
    description: previous month task
    date: "{last_month}"
    position: 1
    kind: task
    state: done
  4:
    description: previous month incomplete task
    date: "{last_month}"
    position: 1
    kind: task
    state: pending
  5:
    description: task unscheduled
    date: ""
    position: 2
    kind: task
    state: pending
  6:
    description: next month task
    date: "{next_month}"
    position: 3
    kind: task
    state: pending
  7:
    description: today's task
    date: "{today}"
    position: 4 
    kind: task
    state: pending
  8:
    description: last week task
    date: "{last_week}"
    position: 5 
    kind: task
    state: pending
  9:
    description: next week task
    date: "{next_week}"
    position: 6 
    kind: task
    state: pending
  10:
    description: this week task
    date: "{this_monday}"
    position: 7     
    kind: task
    state: pending
  11:
    description: today's event
    date: "{today}"
    position: 8
    kind: event
  12:
    description: today's note
    date: "{today}"
    position: 9
    kind: note
  13:
    description: last week's event
    date: "{last_week}"
    position: 10
    kind: event
  14:
    description: last week's note
    date: "{last_week}"
    position: 11
    kind: note
'''
    print(journal_yaml)
    journal_json = yaml.safe_load(journal_yaml.format(today=dates.get_today(), last_month=last_month, next_month=next_month, last_week=last_week, next_week=next_week, this_monday=this_monday))
    with open('/tmp/test.json', 'w') as json_file:
        json.dump(journal_json, json_file)

    journal = TinyDB("/tmp/test.json")
    entries = Query()

    future_log = bullet.future_log(journal)

    assert len(future_log) == 1
    assert future_log[0]['description'] == "task unscheduled"

def test_daily_log():
    today = dates.get_today()

    journal = TinyDB("/tmp/test.json")
    entries = Query()

    dl = bullet.daily_log(journal)

    assert len(dl) == 3
    assert dl[0]["description"] == "today's task"

    dl = bullet.daily_log(journal, notes=False, events=False)
    assert len(dl) == 1
    assert dl[0]["description"] == "today's task"

    dl = bullet.daily_log(journal, tasks=False, events=False)
    assert len(dl) == 1
    assert dl[0]["description"] == "today's note"

    dl = bullet.daily_log(journal, tasks=False, notes=False)
    assert len(dl) == 1
    assert dl[0]["description"] == "today's event"

def test_monthly_log():

    tm = dates.this_month()
    today = dates.get_today()

    journal = TinyDB("/tmp/test.json")
    entries = Query()

    monthly_log = bullet.monthly_log(journal)
    
    assert len(monthly_log) >= 1
    assert monthly_log[0]['description'] == "today's task"

def test_overdue():

    journal = TinyDB("/tmp/test.json")

    today_epoch = datetime.datetime.today().timestamp()
    
    assert bullet.overdue(journal)[0]['description'] == 'previous month incomplete task'
    assert bullet.overdue(journal, str(datetime.datetime.fromtimestamp(today_epoch-6*24*60*60)))[-1]["description"] == "last week task"

def test_weekly_log():
    journal = TinyDB("/tmp/test.json")
    weekly_log = bullet.weekly_log(journal)
    
    assert len(weekly_log) == 4
    assert weekly_log[1]['description'] == "this week task"