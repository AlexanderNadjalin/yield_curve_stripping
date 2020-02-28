import re


class Date:
    def __init__(self, date:str):
        self.date = date
        self.validate_date()

    def validate_date(self):
        rex = re.compile("^[1-2][0-9]{3}[-][0-1][0-9][-][0-3][0-9]$")

        if rex.match(self.date):
            print("Correct format")
        else:
            print("Incorrect")
