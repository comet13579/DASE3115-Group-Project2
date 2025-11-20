from tools.industries import Industries
from tools.testcounter import TestCounter

## A strategy that invests in the industry with the best average performance
## over the same period in previous years.
class AverageMonthlyReturn:
    def __init__(self, data:Industries, counter:TestCounter,yearavg:int):
        self.data = data
        self.counter = counter
        self.yearavg = yearavg
        print(f"-----Average monthly return strategy {yearavg} years-average initialized.-----")

    def __findBesttAvg(self):
        year = self.counter.getyear()
        month = self.counter.getmonth()
        industries_list = self.data.industries_list()
        returns = dict.fromkeys(industries_list,0.0)
        for ind in industries_list:
            counter = self.yearavg * 12
            yearmonth = TestCounter.month_minus_1(year,month)
            while counter != 0:
                returns[ind] += self.data.get(ind,yearmonth[0],yearmonth[1])
                counter -= 1
                yearmonth = TestCounter.month_minus_1(yearmonth[0],yearmonth[1])
        return max(returns,key=returns.get)


    def calculateCurrent(self,amount):
        year = self.counter.getyear()
        month = self.counter.getmonth()
        stockToBuy = self.__findBesttAvg()
        value = self.data.get(stockToBuy, year, month)
        if value is not None:
            result_value = (1 + value / 100) * amount
            #print(f"Year:{self.counter.getyear()}, Month: {self.counter.getmonth()}, Buying industry: {stockToBuy} with return: {value}%")
            return result_value
        else:
            #print(f"Year:{self.counter.getyear()}, Month: {self.counter.getmonth()}, No data for industry: {stockToBuy}")
            return amount

    def progressCounter(self):
        self.counter.progress()