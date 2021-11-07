from datetime import datetime
from os import environ

from holidays import CountryHoliday

birthday = environ.get('birthday')


def celebrate() -> str:
    """Function to look if the current date is a holiday or a birthday.

    Returns:
        str:
        A string of the event observed today.
    """
    day = datetime.today().date()
    today = datetime.now().strftime("%d-%B")
    us_holidays = CountryHoliday('US').get(day)  # checks if the current date is a US holiday
    in_holidays = CountryHoliday('IND', prov='TN', state='TN').get(day)  # checks if Indian (esp TN) holiday
    if in_holidays:
        return in_holidays
    elif us_holidays and 'Observed' not in us_holidays:
        return us_holidays
    elif birthday and today == birthday:
        return 'Birthday'
