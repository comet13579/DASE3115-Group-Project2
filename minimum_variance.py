from industries import Industries
from testcounter import TestCounter
import numpy

## A strategy that invests in the industry with the best average performance
## over the same period in previous years.
class MinVariance:
    def __init__(self, data:Industries, counter:TestCounter,riskfree:RiskFree, yearavg:int):
        self.data = data
        self.counter = counter
        self.riskfree = riskfree
        self.yearavg = yearavg
        print(f"-----Minimum variance strategy {yearavg} years-average initialized.-----")

    def __findBesttAvg(self,year:int):
        industries_list = self.data.industries_list()
        returns = dict.fromkeys(industries_list,0.0)
        data_calc = []
        for ind in industries_list:
            templist = []
            for i in range(self.counter.getyear()-1,self.counter.getyear()-self.yearavg-1,-1):
                for j in range(1,13):
                    val = self.data.get(ind,i,j)
                    if val is not None:
                        templist.append(val)
            data_calc.append(templist)
        cov_matrix = numpy.cov(data_calc,rowvar=True)
        expected_returns = numpy.array([numpy.mean(data) for data in data_calc])
        profolio = cov_matrix.inv().dot(expected_returns)
        min_var_index = numpy.argmin(profolio)

    def calculateCurrent(self,amount):
        pass

    def progressCounter(self):
        self.counter.progress()