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
    description: previous month task
    date: "{last_month}"
    position: 1
  2:
    description: task unscheduled
    date: ""
    position: 2
  3:
    description: next month task
    date: "{next_month}"
    position: 3
  4:
    description: today's task
    date: "{today}"
    position: 4 
  5:
    description: last week task
    date: "{last_week}"
    position: 5 
  6:
    description: next week task
    date: "{next_week}"
    position: 6 
  7:
    description: this week task
    date: "{this_monday}"
    position: 7     
'''
    print(journal_yaml)
    journal_json = yaml.safe_load(journal_yaml.format(today=dates.get_today(), last_month=last_month, next_month=next_month, last_week=last_week, next_week=next_week, this_monday=this_monday))
    with open('/tmp/test.json', 'w') as json_file:
        json.dump(journal_json, json_file)

    journal = TinyDB("/tmp/test.json")
    entries = Query()

    #journal.remove(entries.description.matches(".*"))
    #journal.insert({'description': "previous month task", 'date': "2023-02-03", 'position': "1"})
    #journal.insert({'description': "task unscheduled", 'date': "", 'position': "2"})
    #journal.insert({'description': "next month task", 'date': "2023-04-03", 'position': "3"})
    #journal.insert({'description': "today's task", 'date': dates.get_today(), 'position': "4"})
    #journal.insert({'description': "last week task", 'date': last_week, 'position': "5"})
    #journal.insert({'description': "next week task", 'date': next_monday, 'position': "6"})
    #journal.insert({'description': "this week task", 'date': this_monday, 'position': "7"})

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

def test_overdue():

    journal = TinyDB("/tmp/test.json")

    today_epoch = datetime.datetime.today().timestamp()
    
    assert bullet.overdue(journal)[0]['description'] == 'previous month task'
    assert bullet.overdue(journal, str(datetime.datetime.fromtimestamp(today_epoch-6*24*60*60)))[-1]["description"] == "last week task"

def test_weekly_log():

    tm = dates.this_month()
    today = dates.get_today()

    journal = TinyDB("/tmp/test.json")
    entries = Query()

    weekly_log = bullet.weekly_log(journal)
    
    assert len(weekly_log) == 2
    assert weekly_log[-1]['description'] == "this week task"