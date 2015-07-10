__author__ = 'keithblackwell1'

from datetime import timedelta
import datetime
import bisect as bs
import csv
import os


class Calendar(object):
    """
    Calendar class for making a financial calendar.

    __init__(self, holiday_file=None):

    initialized with a holiday calendar csv. default is:
    'data/ust_holidays.csv'

    Instance Methods are:

    param: today -> can be in the string form YYYY-mm-dd (2012/1/1, 2012-1-1, or 2012/1/2) or as a datetime object

    is_holiday(self, today):
    is_b_day(self, today):
    next_b_day(self, today, step=1):

    In[2]: from bondfuns import Calendar

    In[3]: cal = Calendar()

    In[4]: cal.is_holiday("2012/1/1")
    Out[4]: False

    In[5]: cal.is_b_day("2012/1/1")
    Out[5]: False

    In[10]: cal.is_holiday("2012/1/2")
    Out[10]: True

    In[6]: cal.next_b_day("2012/1/1")
    Out[6]: datetime.datetime(2012, 1, 3, 0, 0)

    """

    def __init__(self, holiday_file='ust_holidays.csv'):

        this_dir, this_filename = os.path.split(__file__)
        holiday_path = os.path.join(this_dir, 'data', holiday_file)

        self.holidays = open_string_csv_to_datetime(holiday_path)

    def is_holiday(self, today):

        if today is None:
            return None

        today = to_datetime(today)

        holidays = self.holidays
        i = bs.bisect_left(holidays, today)

        if i != len(holidays) and holidays[i] == today:
            return True

        else:
            return False

    def is_b_day(self, today):

        if today is None:
            return None

        today = to_datetime(today)

        if today.weekday() in [5, 6]:
            return False

        elif self.is_holiday(today):
            return False

        else:
            return True

    def next_b_day(self, today, step=1):

        if today is None:
            return None

        today = to_datetime(today)

        if step >= 0:
            step_ahead_rule = {0: 1, 1: 1, 2: 1, 3: 1, 4: 3, 5: 2, 6: 1}

        else:
            step_ahead_rule = {0: -3, 1: -1, 2: -1, 3: -1, 4: -1, 5: -1, 6: -2}

        if step == 0 and self.is_b_day(today) is False:
            reps = 1
        else:
            reps = step

        for _ in xrange(abs(reps)):

            while True:
                day_of_week = today.weekday()
                step_size = step_ahead_rule[day_of_week]
                today = today + timedelta(days=step_size)

                if self.is_holiday(today) is False:
                    break

        return today


def to_epoch_milli(today):

    t0 = datetime.datetime(1969, 12, 31, 19, 0)
    t1 = to_datetime(today)
    dif = t1 - t0

    micro_second_date = int(dif.total_seconds() * 1000)
    return micro_second_date


def xls_to_datetime(xldate):
    """
    switches from excel number datetime

    """
    xl_one = datetime.datetime(1899, 12, 31)
    return xl_one + timedelta(days=int(xldate))


def to_datetime(day):
    """
    """
    if isinstance(day, datetime.datetime):
        return day

    elif isinstance(day, str):
        day = day.replace('-', '/')
        day = day.replace('_', '/')
        return datetime.datetime.strptime(day, '%Y/%m/%d')

    else:
        return None


def open_string_csv_to_datetime(csv_path, opt='rU'):
    f = open(csv_path, opt)
    csv_f = csv.reader(f)
    xxx = [x for x in csv_f]
    xxx = [to_datetime(x) for x in xxx[0]]
    f.close()
    return xxx

def write_string_csv(data, csv_path):
    fp = open(csv_path, 'wb')
    a = csv.writer(fp)
    a.writerows([data])
    fp.close()