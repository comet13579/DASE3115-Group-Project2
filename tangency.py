from industries import Industries
from testcounter import TestCounter
from riskfree import RiskFree
import numpy as np


## A strategy that calculates the tangency portfolio based on historical data.
class Tangency:
    def __init__(self, data:Industries, counter:TestCounter, riskfree:RiskFree, yearavg:int):
        self.data = data
        self.counter = counter
        self.riskfree = riskfree
        self.yearavg = yearavg
        print(f"-----Tangency portfolio strategy {yearavg} years data initialized.-----")

    def __calcweight(self):
        year = self.counter.getyear()
        month = self.counter.getmonth()
        industries_list = self.data.industries_list()
        datacalc = []
        for ind in industries_list:
            counter = self.yearavg * 12
            yearmonth = TestCounter.month_minus_1(year,month)
            temp = []
            while counter != 0:
                temp.append(self.data.get(ind,yearmonth[0],yearmonth[1]) - self.riskfree.get(yearmonth[0],yearmonth[1]))
                counter -= 1
                yearmonth = TestCounter.month_minus_1(yearmonth[0],yearmonth[1])
            datacalc.append(temp)
        datacalc = np.array(datacalc)
        cov_matrix = np.cov(datacalc, rowvar=True)
        mean_returns = np.mean(datacalc, axis=1)
        inv_cov_matrix = np.linalg.inv(cov_matrix)
        weights = inv_cov_matrix.dot(mean_returns)
        normalized_weights = weights / np.linalg.norm(weights)
        return list(normalized_weights)

    def calculateCurrent(self,amount):
        year = self.counter.getyear()
        month = self.counter.getmonth()
        weights = self.__calcweight()
        industries_list = self.data.industries_list()
        revenue_percentage = 0.0
        for ind, weight in zip(industries_list, weights):
            #print(f"Industry: {ind}, Weight: {weight:.4f}")
            value = self.data.get(ind, year, month)
            if value is not None:
                revenue_percentage += value * weight
            else:
                raise ValueError(f"No data for industry: {ind} in {year}-{month}")
        amount = (1 + revenue_percentage / 100) * amount
        return amount

    def progressCounter(self):
        self.counter.progress()