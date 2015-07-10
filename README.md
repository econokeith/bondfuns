# bondfuns : basic price / yield / calendar functions for evaluating US Treasuries

`bondfun` is a creates a basic Treasury bond object called 'Treasury()' which follows the UST conventions (i.e. Actual/Actual, semi-annual coupons, etc). It provides then provides basic methods for solving for price, yield to maturity, accrued interest, etc as well as calendar function. 

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




