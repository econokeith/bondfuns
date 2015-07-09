# bondfuns
Basic library of function for evaluating US Treasuries

Basic US Treasury Object:

Treasury()

Will accept dates in datetime , YYYY/mm/dd, YYYY-mm-dd, or YYYY_mm_dd formatting

class attributes:

acc_con = accrual convention = Actual/Actual
holiday_cal = UST_CALENDAR
t_plus = 1 = settle convention t+1

attributes are:
maturity_date, coupon, issue_date, tenor, cf (cash flows), name, reopened, cusip

(note: setting either issue_date or tenor will set the other)

Class Methods:

from_name(cls, name): Treasury.from_name('T_.25_2013_1_15')
next_b_day(cls, today, steps=1): next_business_day using class holiday calendar
settle(cls, trade_day): using calendar and settle convention to find settle day of trade on given date

Instance Methods:

ytm(self, settle_date, price, tplus=0): yield to maturity
price(self, settle_date, ytm, tplus=0): clean price
duration(self, settle_date, price_or_yield, tplus=0): modified duration
dv01(self, settle_date, price_or_yield, tplus=0): dollar value of a basis point
acc_int(self, settle_date, tplus=0):accrued interest
cash_flows(self, settle_date=None, tplus=0, all=True): cash flow dates

Is a child class of the Bond Class

Basic Calendar Object: 

Calendar()

Calendar class for making a financial calendar.

__init__(self, holiday_path=None):

initialized with a pickled holiday calendar. default is:
'bondfuns/ust_holiday_cal.pickle'

Instance Methods are:

param: today -> can be in the string form YYYY-mm-dd (2012/1/1, 2012-1-1, or 2012/1/2) or as a datetime object

is_holiday(self, today):
is_b_day(self, today):
next_b_day(self, today, step=1):

In[2]: from bondfuns.calendar import Calendar

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
