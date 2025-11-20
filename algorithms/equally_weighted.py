from tools.industries import Industries
from tools.testcounter import TestCounter

class EquallyWeighted:
    def __init__(self, data:Industries, counter:TestCounter):
        self.data = data
        self.counter = counter
        print("-----Equally Weighted strategy initialized.-----")

    def calculateCurrent(self,amount):
        year = self.counter.getyear()
        month = self.counter.getmonth()
        stockcount = len(self.data.industries_list())
        amount_per_stock = amount / stockcount
        total_value = 0.0
        for industry in self.data.industries_list():
            value = self.data.get(industry, year, month)
            if value is not None:
                total_value += (1 + value / 100) * amount_per_stock
        return total_value

    def progressCounter(self):
        self.counter.progress()