from tools.industries import Industries
from tools.testcounter import TestCounter

## A strategy that invests in the industry with the best average performance
## over the same period in previous years.
class SamePeriodMarketPerf:
    def __init__(self, data:Industries, counter:TestCounter,yearavg:int):
        self.data = data
        self.counter = counter
        self.yearavg = yearavg
        print(f"-----Same Period Market Performance strategy {yearavg} years-average initialized.-----")

    def __findBesttAvg(self,year:int,month:int):
        industries_list = self.data.industries_list()
        returns = dict.fromkeys(industries_list,0.0)
        for ind in industries_list:
            for i in range(self.counter.getyear()-1,self.counter.getyear()-self.yearavg-1,-1):
                val = self.data.get(ind,i,month)
                returns[ind] += val
        return max(returns,key=returns.get)


    def calculateCurrent(self,amount):
        year = self.counter.getyear()
        month = self.counter.getmonth()

        stockToBuy = self.__findBesttAvg(year,month)
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