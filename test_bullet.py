import datetime
import json
import yaml

from tinydb import TinyDB, Query

import bullet
import dates

def from_epoch(epoch):
    date = datetime.datetime.fromtimestamp(epoch)
    return (date.year, date.month, date.day, date.isocalendar()[1])
    
def test_future_log():

    ts = datetime.datetime.today().timestamp()
    today = from_epoch(ts)
    this_week = from_epoch(datetime.datetime.strptime('%s %s 1' % (today[0], today[3]), '%G %V %u').timestamp())
    if this_week == today:
        this_week = from_epoch(datetime.datetime.strptime('%s %s 2' % (today[0], today[3]), '%G %V %u').timestamp())
    last_month = from_epoch(ts-31*24*60*60)
    next_month = from_epoch(ts+31*24*60*60)
    last_week = from_epoch(ts-7*24*60*60)
    next_week = from_epoch(ts+7*24*60*60)

    journal_yaml = '''
_default:
  1:
    description: previous month event
    date:
      year: "{last_month_year}"
      month: "{last_month_month}"
      day: "{last_month_day}"
      week: "{last_month_week}"
    position: 1
    kind: event
    state: ""
  2:
    description: previous month note
    date:
      year: "{last_month_year}"
      month: "{last_month_month}"
      day: "{last_month_day}"
      week: "{last_month_week}"
    position: 2
    kind: note
    state: ""
  3:
    description: previous month task
    date:
      year: "{last_month_year}"
      month: "{last_month_month}"
      day: "{last_month_day}"
      week: "{last_month_week}"
    position: 3
    kind: task
    state: done
  4:
    description: previous month incomplete task
    date:
      year: "{last_month_year}"
      month: "{last_month_month}"
      day: "{last_month_day}"
      week: "{last_month_week}"
    position: 4
    kind: task
    state: pending
  5:
    description: task unscheduled
    date:
      year: ""
      month: ""
      day: ""
      week: ""
    position: 5
    kind: task
    state: pending
  6:
    description: next month task
    date:
      year: "{next_month_year}"
      month: "{next_month_month}"
      day: "{next_month_day}"
      week: "{next_month_week}"
    position: 6
    kind: task
    state: pending
  7:
    description: today's task
    date:
      year: "{today_year}"
      month: "{today_month}"
      day: "{today_day}"
      week: "{today_week}"
    position: 7 
    kind: task
    state: pending
  8:
    description: last week task
    date:
      year: "{last_week_year}"
      month: "{last_week_month}"
      day: "{last_week_day}"
      week: "{last_week_week}"
    position: 8 
    kind: task
    state: pending
  9:
    description: next week task
    date:
      year: "{next_week_year}"
      month: "{next_week_month}"
      day: "{next_week_day}"
      week: "{next_week_week}"
    position: 9 
    kind: task
    state: pending
  10:
    description: this week task
    date:
      year: "{this_week_year}"
      month: "{this_week_month}"
      day: "{this_week_day}"
      week: "{this_week_week}"
    position: 10     
    kind: task
    state: pending
  11:
    description: today's event
    date:
      year: "{today_year}"
      month: "{today_month}"
      day: "{today_day}"
      week: "{today_week}"
    position: 11
    kind: event
    state: ""
  12:
    description: today's note
    date:
      year: "{today_year}"
      month: "{today_month}"
      day: "{today_day}"
      week: "{today_week}"
    position: 12
    kind: note
    state: ""
  13:
    description: last week's event
    date:
      year: "{last_week_year}"
      month: "{last_week_month}"
      day: "{last_week_day}"
      week: "{last_week_week}"
    position: 13
    kind: event
    state: ""
  14:
    description: last week's note
    date:
      year: "{last_week_year}"
      month: "{last_week_month}"
      day: "{last_week_day}"
      week: "{last_week_week}"
    position: 14
    kind: note
    state: ""
  15:
    description: last week's done task
    date:
      year: "{last_week_year}"
      month: "{last_week_month}"
      day: "{last_week_day}"
      week: "{last_week_week}"
    position: 15
    kind: task
    state: done
'''
    print(journal_yaml)
    journal_json = yaml.safe_load(
        journal_yaml.format(
          today_year=today[0],
          today_month=today[1],
          today_day=today[2],
          today_week=today[3],
          last_month_year=last_month[0],
          last_month_month=last_month[1],
          last_month_day=last_month[2],
          last_month_week=last_month[3],
          next_month_year=next_month[0],
          next_month_month=next_month[1],
          next_month_day=next_month[2],
          next_month_week=next_month[3],
          last_week_year=last_week[0],
          last_week_month=last_week[1],
          last_week_day=last_week[2],
          last_week_week=last_week[3],
          next_week_year=next_week[0],
          next_week_month=next_week[1],
          next_week_day=next_week[2],
          next_week_week=next_week[3],
          this_week_year=this_week[0],
          this_week_month=this_week[1],
          this_week_day=this_week[2],
          this_week_week=this_week[3]))
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

    today_epoch = datetime.datetime.today().timestamp()
    last_month = datetime.datetime.fromtimestamp(today_epoch-31*24*60*60).date()
    last_month = (last_month.year, last_month.month)

    monthly_log = bullet.monthly_log(journal, month=last_month)
    assert len(monthly_log) == 4

    monthly_log = bullet.monthly_log(journal, month=last_month, notes=False, events=False)
    assert len(monthly_log) == 2
    assert monthly_log[0]["description"] == "previous month task"

    monthly_log = bullet.monthly_log(journal, month=last_month, tasks=False, events=False)
    assert len(monthly_log) == 1
    assert monthly_log[0]["description"] == "previous month note"

    monthly_log = bullet.monthly_log(journal, month=last_month, notes=False, tasks=False)
    assert len(monthly_log) == 1
    assert monthly_log[0]["description"] == "previous month event"

    monthly_log = bullet.monthly_log(journal, month=last_month, done=False)
    assert len(monthly_log) == 3
    assert "previous month task" not in [entry["description"] for entry in monthly_log]

def test_overdue():

    journal = TinyDB("/tmp/test.json")
    
    assert bullet.overdue(journal)[0]['description'] == 'previous month incomplete task'

    today_epoch = datetime.datetime.today().timestamp()
    last_week = datetime.datetime.fromtimestamp(today_epoch-6*24*60*60)
    last_week = {"year": last_week.year, "month": last_week.month, "day": last_week.day}
    assert bullet.overdue(journal, last_week)[-1]["description"] == "last week task"

def test_weekly_log():
    journal = TinyDB("/tmp/test.json")
    weekly_log = bullet.weekly_log(journal)
    
    assert len(weekly_log) == 4
    assert weekly_log[1]['description'] == "this week task"
    
    today_epoch = datetime.datetime.today().timestamp()
    last_week = datetime.datetime.fromtimestamp(today_epoch-7*24*60*60).isocalendar()
    last_week = (str(last_week[0]), str(last_week[1]))
    weekly_log = bullet.weekly_log(journal, week=last_week)
    assert len(weekly_log) == 4

    weekly_log = bullet.weekly_log(journal, week=last_week, notes=False, events=False)
    assert len(weekly_log) == 2
    assert weekly_log[0]["description"] == "last week task"

    weekly_log = bullet.weekly_log(journal, week=last_week, tasks=False, events=False)
    assert len(weekly_log) == 1
    assert weekly_log[0]["description"] == "last week's note"

    weekly_log = bullet.weekly_log(journal, week=last_week, notes=False, tasks=False)
    assert len(weekly_log) == 1
    assert weekly_log[0]["description"] == "last week's event"

    weekly_log = bullet.weekly_log(journal, week=last_week, notes=False, events=False, done=False)
    assert len(weekly_log) == 1
    assert weekly_log[0]["description"] == "last week task"
    