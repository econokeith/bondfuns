__author__ = 'keithblackwell1'

import bisect as bs
import datetime
import pickle

import scipy.optimize as optimize
from dateutil.relativedelta import relativedelta

from bondfuns.calendar import Calendar, to_datetime

UST_CALENDAR = Calendar()


class Bond(object):
    """
    Basic Fixed Income Object
    So, far mirrors US Treasuries although, I want to expand it to include other bond types later

    Will accept dates in datetime , YYYY/mm/dd, YYYY-mm-dd, or YYYY_mm_dd formatting
    """
    holiday_cal = UST_CALENDAR
    t_plus = 1

    def __init__(self, maturity_date=None, coupon=None, issue_date=None, tenor=None, cf=None, name=None):

        self.name = name
        self.coupon = coupon
        self.cf = cf

        self.maturity_date = to_datetime(maturity_date)

        if tenor is not None:
            self._issue_date = issue_date
            self.tenor = tenor

        else:
            self._tenor = tenor
            self.issue_date = self.holiday_cal.next_b_day(issue_date, 0)

    def __repr__(self):
        try:
            return self.name
        except:
            return self.__class__

    @classmethod
    def next_b_day(cls, today, steps=1):
        """
        next_b_day(cls, today, steps=1):
        returns the next business day of the bond given desired steps ahead
        """
        return cls.holiday_cal.next_b_day(today, steps)

    @classmethod
    def settle(cls, trade_day):
        """
        settle(cls, trade_day):
        returns settle day for trade on given day using bonds settle convention
        """
        return cls.holiday_cal.next_b_day(trade_day, cls.t_plus)

    @property
    def maturity_date(self):
        return self._maturity_date

    @property
    def issue_date(self):
        return self._issue_date

    @property
    def tenor(self):
        return self._tenor

    @maturity_date.setter
    def maturity_date(self, today):
        self._maturity_date = to_datetime(today)

    @issue_date.setter
    def issue_date(self, today):

        issue_date = self.holiday_cal.next_b_day(today, 0)
        maturity_date = self.maturity_date
        self._issue_date = issue_date

        if isinstance(issue_date, datetime.datetime) and isinstance(maturity_date, datetime.datetime):
            tenor = maturity_date - issue_date
            self._tenor = int(round(tenor.days / 365.25, 0))

    @tenor.setter
    def tenor(self, value):
        self._tenor = value

        if value is not None and isinstance(self.maturity_date, datetime.datetime):
            issue_date = self.maturity_date - relativedelta(years=self.tenor)
            self._issue_date = self.holiday_cal.next_b_day(issue_date, 0)

    def ytm(self, settle_date, price):
        pass

    def price(self, settle_date, ytm):
        pass

    def duration(self, settle_date, ytm_or_price):
        pass

    def cash_flows(self, settle_date=None):
        pass

    def acc_int(self, settle_date):
        pass

    def dv01(self, settle_date, ytm_or_price):
        pass


class Treasury(Bond):
    """
    Basic US Treasury Object:

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

    """
    acc_con = 'A/A'
    holiday_cal = UST_CALENDAR
    t_plus = 1 ## UST settle T+1

    def __init__(self, maturity_date=None, coupon=None, issue_date=None, tenor=None, cf=None, name=None, reopened=False,
                 cusip=None,**kwargs):
        super(Treasury, self).__init__(name=name, maturity_date=maturity_date, coupon=coupon, issue_date=issue_date,
                                       tenor=tenor, cf=cf, **kwargs)
        self.reopened = reopened
        self.cusip = cusip

    @classmethod
    def from_name(cls, name):
        """
        Treasury.from_name('T_.25_2013_1_15') will create an instance of Treasury() with
        the appropriate maturity and coupon

        the maturity must be in the form YYYY_mm_dd with either '_', '/', or '-' between:

        'T_.25_2013_1_15'
        'T_0.25_2013/1/15'
        'T_.25_2013-01-15'

        """
        split_name = name.split('_')
        coupon = float(split_name[1]) / 100

        if len(split_name) == 3:
            maturity = split_name[2]

        elif len(split_name) == 5:
            maturity = split_name[2] + '/' + split_name[3] + '/' + split_name[4]

        else:
            maturity = None

        return cls(maturity_date=maturity, coupon=coupon, name=name)

    def ytm(self, settle_date, price, tplus=0):
        """
        Yield to Maturity Function for UST.

        ytm(self, settle_date, price, tplus=0):

        :param settle_date: date the trade settles on
        :param price: clean price
        :param tplus: set to zero if entering settle date, set to 1 if entering trade date
        :return:

        Will accept dates in datetime , YYYY/mm/dd, YYYY-mm-dd, or YYYY_mm_dd formatting
        """

        accrued_interest, _, _, price_fun = self._price_yield_setup(settle_date, tplus)

        yield_fun = lambda y: price_fun(y) - price - accrued_interest
        return round(optimize.newton(yield_fun, .05),6)

    def price(self, settle_date, ytm, tplus=0):
        """
        price(self, settle_date, ytm, tplus=0):
        :param settle_date: date the trade settles on
        :param ytm: yield to maturity in decimals
        :param tplus: set to zero if entering settle date, set to 1 if entering trade date
        :return: price of bond

        Will accept dates in datetime , YYYY/mm/dd, YYYY-mm-dd, or YYYY_mm_dd formatting
        """
        accrued_interest, _, _, price_fun = self._price_yield_setup(settle_date, tplus)

        return round(price_fun(ytm) - accrued_interest, 4)

    def duration(self, settle_date, price_or_yield, tplus=0):
        """
        Solves for Modified Duration of the bond

        duration(self, settle_date, price_or_yield, tplus=0):

        :param settle_date: date the trade settles on
        :param price_or_yield: either price or yield
        :param tplus: set to zero if entering settle date, set to 1 if entering trade date
        :return:

        Will accept dates in datetime , YYYY/mm/dd, YYYY-mm-dd, or YYYY_mm_dd formatting
        """
        accrued_interest, cf_times, cf_values, price_fun = self._price_yield_setup(settle_date, tplus)

        if price_or_yield > 1:
            price = price_or_yield
            yield_fun = lambda y: price_fun(y) - price - accrued_interest
            ytm = optimize.newton(yield_fun, .05)

        else:
            ytm = price_or_yield
            price = price_fun(ytm) - accrued_interest

        return sum((-.5 * cf * t * (1 + ytm / 2) ** (-1 - t) for cf, t in zip(cf_values, cf_times))) / price

    def dv01(self, settle_date, price_or_yield, tplus=0):
        """
        Solves for dv01: Dollar Value of a basis point

        dv01(self, settle_date, price_or_yield, tplus=0):

        :param settle_date: date the trade settles on
        :param price_or_yield: either price or yield of the bond
        :param tplus: set to zero if entering settle date, set to 1 if entering trade date:

        Will accept dates in datetime , YYYY/mm/dd, YYYY-mm-dd, or YYYY_mm_dd formatting
        """
        accrued_interest, cf_times, cf_values, price_fun = self._price_yield_setup(settle_date, tplus)

        if price_or_yield > 1:
            price = price_or_yield
            yield_fun = lambda y: price_fun(y) - price - accrued_interest
            ytm = optimize.newton(yield_fun, .05)

        else:
            ytm = price_or_yield
            price = price_fun(ytm) - accrued_interest

        return sum((-.5 * cf * t * (1 + ytm / 2) ** (-1 - t) for cf, t in zip(cf_values, cf_times))) / 100

    def acc_int(self, settle_date, tplus=0):
        """
        Solves for accrued interest of the bond

        acc_int(self, settle_date, tplus=0):

        :param settle_date: date the trade settles on
        :param tplus: set to zero if entering settle date, set to 1 if entering trade date:
        :return:

        Will accept dates in datetime , YYYY/mm/dd, YYYY-mm-dd, or YYYY_mm_dd formatting
        """
        accrued_interest, _, _, _ = self._price_yield_setup(settle_date, tplus)
        return accrued_interest

    def _price_yield_setup(self, settle_date, tplus=0):
        """
        Does set up work
        :param settle_date:
        :return:
        """
        maturity_date = self.maturity_date
        issue_date = self.issue_date
        coupon = self.coupon

        if maturity_date is None:
            return None

        if tplus == 0:
            settle_date = to_datetime(settle_date)

        else:
            settle_date = self.holiday_cal.next_b_day(settle_date, tplus)

        if settle_date > maturity_date:
            return None

        if issue_date is not None and settle_date < issue_date:
            settle_date = issue_date

        coupon *= 100
        cash_flows = ust_get_cash_flow(settle_date, maturity_date)

        cf0, cf1 = cash_flows[:2]
        cash_flow_count = len(cash_flows) - 1

        accrual_time = float((settle_date - cf0).days) / float((cf1 - cf0).days)
        accrued_interest = coupon * accrual_time / 2

        cf_times = [1 - accrual_time + i for i in xrange(cash_flow_count)]
        cf_times.append(cf_times[-1])

        cf_values = [coupon / 2 for _ in xrange(cash_flow_count)]
        cf_values.append(100)

        price_fun = lambda ytm: sum(cf * (1 + ytm / 2) ** -t for cf, t in zip(cf_values, cf_times))

        return accrued_interest, cf_times, cf_values, price_fun

    def cash_flows(self, settle_date=None, tplus=0, all=True):
        """
        Solves for the tuple of cash flows dates of the bond.

        cash_flows(self, settle_date=None, tplus=0, all=True):

        :param settle_date: date the trade settles. if None, will give entire cash flow structure of bond.
                            if a date, will return all cash flows up the one immediately before settle_date
        :param tplus: set to zero if entering settle date, set to 1 if entering trade date
        :param all: will override settle_date to give full cash flow structure of the bond

        Will accept dates in datetime , YYYY/mm/dd, YYYY-mm-dd, or YYYY_mm_dd formatting

        """
        issue_date = self.issue_date
        maturity_date = self.maturity_date

        if isinstance(issue_date, datetime.datetime) and settle_date is None:
            settle_date = issue_date

        elif settle_date is None:
            return None

        else:
            return _ust_cash_flow(settle_date, maturity_date)


class UstCashFlows(object):
    """
    this is just an object to hide the cash flow tuples for fast UST cf creation
    """
    def __init__(self):
        with open('bondfuns/ust_cash_flow_dates.pickle','rb') as pick:
            self.mid, self.end = pickle.load(pick)

## initializes the cash flow object
UST_CFS = UstCashFlows()

def _ust_cash_flow(settle_date, maturity_date):
    """

    :type issue_date: object
    """
    if maturity_date.day == 15:
        search_list = UST_CFS.mid
        min_date = datetime.datetime(1980, 1, 15, 0, 0)
        max_date = datetime.datetime(2063, 3, 15, 0, 0)

    else:
        search_list = UST_CFS.end
        min_date = datetime.datetime(1980, 1, 31, 0, 0)
        max_date = datetime.datetime(2063, 3, 31, 0, 0)


    if settle_date < min_date or maturity_date > max_date:
        return _ust_create_cashflow(settle_date, maturity_date)

    skip_rule = {1: 0, 7: 0, 2: 1, 8: 1, 3: 2, 9: 2, 4: 3, 10: 3, 5: 4, 11: 4, 6: 5, 12: 5}

    m_month = maturity_date.month
    skip = skip_rule[m_month]
    search_list = search_list[skip:: 6]

    p_mat = bs.bisect_left(search_list, maturity_date)
    p_set = bs.bisect_right(search_list, settle_date)

    return search_list[p_set - 1: p_mat + 1]


def ust_get_cash_flow(settle_date, maturity_date, issue_date=None, tenor=None, all=False):
    """

    :type issue_date: object
    """
    if maturity_date.day == 15:
        search_list = UST_CFS.mid
        min_date = datetime.datetime(1980, 1, 15, 0, 0)
        max_date = datetime.datetime(2063, 3, 15, 0, 0)

    else:
        search_list = UST_CFS.end
        min_date = datetime.datetime(1980, 1, 31, 0, 0)
        max_date = datetime.datetime(2063, 3, 31, 0, 0)

    if all is not None:
        if isinstance(issue_date, datetime.datetime):
            settle_date = issue_date

        elif isinstance(tenor, int):
            settle_date = maturity_date - relativedelta(years=tenor)

        else:
            pass

    else:
        if isinstance(issue_date, datetime.datetime) and issue_date > settle_date:
            settle_date = issue_date

        else:
            pass

    if settle_date < min_date or maturity_date > max_date:
        return _ust_create_cashflow(settle_date, maturity_date)

    skip_rule = {1: 0, 7: 0, 2: 1, 8: 1, 3: 2, 9: 2, 4: 3, 10: 3, 5: 4, 11: 4, 6: 5, 12: 5}

    m_month = maturity_date.month
    skip = skip_rule[m_month]
    search_list = search_list[skip:: 6]

    p_mat = bs.bisect_left(search_list, maturity_date)
    p_set = bs.bisect_right(search_list, settle_date)

    return search_list[p_set - 1: p_mat + 1]


def _ust_create_cashflow(settle_date, maturity_date):
    """
    Alternative function for creating cash flows for UST
    """
    cashflows = []
    i = 0
    while True:
        cashflows.append(maturity_date - relativedelta(months=6 * i))
        i += 1
        if settle_date >= cashflows[-1]:
            break

    return sorted(cashflows)



