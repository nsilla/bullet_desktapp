import datetime

import dates

def test_this_week():
    tw = datetime.date.today().isocalendar()

    assert dates.this_week() == (str(tw[0]), str(tw[1]))

def test_week():

    assert dates.week(dates.get_today()) == dates.this_week()