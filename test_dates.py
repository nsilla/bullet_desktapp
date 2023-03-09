import datetime

import dates

def test_this_week():
    tw = datetime.date.today().isocalendar()[0:2]

    assert dates.this_week() == tw

def test_week():

    assert dates.week(dates.get_today()) == dates.this_week()