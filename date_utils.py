import re
import datetime as dt
import calendar
from loguru import logger


class Date:
    def __init__(self, d: str):
        self.date_string = d
        self.date = None
        self.validate_date()
        self.year = self.date.year
        self.month = self.date.month
        self.day = self.date.day
        self.leap_year = self.is_leap_year()
        self.eom = self.is_end_of_month()

    def set_date(self, d: dt.date):
        self.date = d
        self.year = d.year
        self.month = d.month
        self.day = d.day

    def set_year(self, y: dt.date.year):
        self.year = y
        self.set_date(dt.date(self.year, self.month, self.day))

    def set_month(self, m: dt.date.month):
        self.month = m
        self.set_date(dt.date(self.year, self.month, self.day))

    def set_day(self, d: dt.date.day):
        self.day = d
        self.set_date(dt.date(self.year, self.month, self.day))

    def validate_date(self):
        rex = re.compile("^[0-9]{4}[-][0-1][0-9][-][0-3][0-9]$")

        if not rex.match(self.date_string):
            logger.critical('Date format not "YYYY-MM-DD". Aborted.')
            quit()

        try:
            dt.datetime.strptime(self.date_string, "%Y-%m-%d")
        except ValueError:
            logger.critical('Date is not valid. Aborted.')
            quit()
        year = int(self.date_string[0:4])
        if self.date_string[5:6] == '0':
            month = int(self.date_string[6:7])
        else:
            month = int(self.date_string[5:7])
        day = int(self.date_string[8:10])
        self.date = dt.date(year, month, day)

    def is_leap_year(self):
        if (self.year % 4) == 0:
            if (self.year % 100) == 0:
                if (self.year % 400) == 0:
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False

    def is_end_of_month(self):
        if self.day == calendar.monthrange(self.year, self.month)[1]:
            return True
        else:
            return False

    def add_days(self, n: int):

    def add_months(self, n: int, eom_flag: bool):
        new_month = self.month + n
        # Subtracting over January.
        if new_month < 1:
            new_month = 12 + new_month
        # Adding over December.
        if new_month > 12:
            new_month = 12 - new_month
        if self.day > calendar.monthrange(self.year, new_month)[1]:
            self.set_day(calendar.monthrange(self.year, new_month)[1])
            self.set_month(new_month)
        # End-of-month flag. Adding months always yields last day.
        if eom_flag and self.is_end_of_month():
            self.set_month(new_month)
            self.set_day(calendar.monthrange(self.year, self.month)[1])

    def add_years(self, n: int, eom_flag: bool):
        new_year = self.year + n

    def add(self, n: int, units: str, eom_flag: bool):
        if units == 'D':
            self.set_date(self.date + dt.timedelta(n))
        # months
        elif units == 'M':
            self.add_months(n, eom_flag)
        # years
        elif units == 'Y':
            self.add_years(n, eom_flag)
        elif units == 'BD':
            pass
        else:
            logger.critical('Parameter values for "units" is not in [Y, M, D, BD]. Aborted.')
            quit()
