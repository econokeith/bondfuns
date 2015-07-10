
from distutils.core import setup

long_description = """
bondfuns : basic price / yield / calendar functions for evaluating US Treasuries:

bondfun creates a basic Treasury bond object Treasury() which follows UST conventions 
(i.e. Actual/Actual, semi-annual coupons, trades settle T+1 etc). It provides basic methods 
for solving for price, yield to maturity, accrued interest, etc as well as calendar 
functions to find trade settles, business days, etc. All methods assume entry of settle date 
not trade date, but have the options to assume trade date if necessary.
"""

setup(
    name="bondfuns",
    version="1.0",
    description="bondfuns : basic price / yield / calendar functions for evaluating US Treasuries",
    long_description=long_description,
    keywords="finance, bonds, yield, Treasuries",
    author="Keith Blackwell",
    author_email="keith.blackwell@gmail.com",
    url="https://github.com/econokeith/bondfuns",
    license="MIT",
    packages=["bondfuns", "bondfuns.data"],
    install_requires=["dateutils"],
    classifiers=[
        'Development Status :: Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2'])
