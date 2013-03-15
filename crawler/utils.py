"""
The Utils
"""

import unidecode
import re
from datetime import timedelta

"""Define the weekday mnemonics to match the date.weekday function"""
(MON, TUE, WED, THU, FRI, SAT, SUN) = range(7)

# Settings
DEBUG = True


def log(str):
    """
    Logging method
    """

    print str


def slugify(str):
    """
    Slugify the string
    """
    str = unidecode.unidecode(str.encode('utf-8')).lower()
    str = re.sub(r'\W+', '-', str)

    # Just to be on the safe side
    if str[str.__len__()-1] == '-':
        str = str[:-1]

    return str


def workdaysub(start_date, end_date, whichdays=(MON, TUE, WED, THU, FRI)):
    '''
    Calculate the number of working days between two dates inclusive
    (start_date <= end_date).

    The actual working days can be set with the optional whichdays parameter
    (default is MON-FRI)
    '''
    delta_days = (end_date - start_date).days + 1
    full_weeks, extra_days = divmod(delta_days, 7)
    # num_workdays = how many days/week you work * total # of weeks
    num_workdays = (full_weeks + 1) * len(whichdays)
    # subtract out any working days that fall in the 'shortened week'
    for d in range(1, 8 - extra_days):
        if (end_date + timedelta(d)).weekday() in whichdays:
            num_workdays -= 1
    return num_workdays
