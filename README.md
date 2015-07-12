# bondfuns : basic price / yield / calendar functions for evaluating US Treasuries

`bondfun` a creates a basic Treasury bond object `Treasury()` which follows UST conventions (i.e. Actual/Actual, semi-annual coupons, trades settle T+1 etc). It provides basic methods for solving for price, yield to maturity, accrued interest, etc as well as calendar functions to find trade settles, business days, etc. All methods assume entry of settle date not trade date, but have the options to assume trade date if necessary. 

`bondfun` will accept dates in datetime, 2012/3/15, 2013-3-15, or 2015_3_15 formats

#### Dependencies
- dateutils

#### Warning
- this is the alpha version 0.0 of this package and has only been tested on python 2.7

## Methods and Attributes
### Attribues
```
Treasury(maturity_date=None, coupon=None, issue_date=None, tenor=None, cf=None, name=None,
          reopened=False, cusip=None)
```
notes: 
- `issue_date` is the first trading day of the bond, which is the first business day on or after the first accrual day
- `cf` is the tuple of cash flow dates
- either `issue_date` or `tenor` will set the other
- if `issue_date` is not None and an earlier trade or settle date is entered that date will be assume to be the issue date of the bond
- if a trade or `settle_date` that is after or equal to `maturity_date`, all calculations will return 0
- all date attributes are saved and returned in datetime form
- if bond is created with `maturity_date` and `coupon`, then `name` will be automatically set.

### Methods

#### Basic Calculation 
- `ytm(self, settle_date, price, tplus=0)`: yield to maturity
- `price(self, settle_date, ytm, tplus=0)`: clean price
- `duration(self, settle_date, price_or_yield, tplus=0)`: modified duration
- `dv01(self, settle_date, price_or_yield, tplus=0)`: dollar value of a basis point
- `acc_int(self, settle_date, tplus=0)`:accrued interest
- `cash_flows(self, settle_date=None, tplus=0, all=True)`: cash flow dates

(note: all basic calculations assume the date entered is the settle date. if entering trade date, change tplus to 1)

#### Calendar Methods
- `is_holiday(self, today)`: True or False if a market holiday (does not count holidays on weekends)
- `is_b_day(self, today)`: True or False if market holiday or weekend
- `next_b_day(self, today, step=1)`: the next business day given desired steps ahead
- `settle(cls, trade_day)`: using calendar and settle convention to find settle day of trade on given date

#### Other Methods
- `from_name(cls, name)`: class method for initializing a bond from its name. `t = Treasury.from_name('T_.25_2013_1_15')`

## Basic Usage
```
In[2]: from bondfuns import Treasury
In[3]: t1 = Treasury('2020/5/31', .0125)
In[4]: t1.price('2015/7/8', .0125)
```
Out[4]: 99.9997
```
In[5]: t1 = Treasury('2018/5/31', .0075)
In[6]: t1.price('2015/7/8', .00075)
```
Out[6]: 101.9524
```
In[7]: t1.price('2015/7/8', .0075)
```
Out[7]: 99.9999
```
In[8]: t1.ytm('2015/7/8', 100)
```
Out[8]: 0.0075
```
In[9]: t2 = Treasury.from_name('T_1.25_2019_6_30')
In[10]: t2.maturity_date
```
Out[10]: datetime.datetime(2019, 6, 30, 0, 0)
```
In[13]: t2.ytm('2012_1_3', 101)
```
Out[13]: 0.011105
```
In[15]: t2.acc_int('2013-12-31')
```
Out[15]: 0.0
```
In[16]: t2.duration('2013-12-31', 100)
```
Out[16]: 5.30
```
In[17]: t2.duration('2013-12-31', .0125)
```
Out[17]: 5.30
```
In[18]: Treasury.is_holiday("2012-1-1")
```
Out[18]: False
```
In[21]: t2.next_b_day("2012-1-1")
```
Out[21]: datetime.datetime(2012, 1, 3, 0, 0)
