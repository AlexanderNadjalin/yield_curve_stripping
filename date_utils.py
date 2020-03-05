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

    def add(self, n: int, units: str, eom_flag: bool):
        if units == 'D':
            self.date += dt.timedelta(n)
        elif units == 'M':
            self.date += dt.timedelta(n * 365 / 12)
        elif units == 'Y':
            self.date += dt.timedelta(n * 365)
        elif units == 'BD':
            pass
        else:
            logger.critical('Parameter values for "units" is not in [Y, M, D, BD]. Aborted.')
            quit()
