from tools.industries import Industries
from tools.testcounter import TestCounter
from tools.riskfree import RiskFree
import numpy as np
from scipy.optimize import minimize

## A strategy that calculates the tangency portfolio based on historical data.
class Tangency:
    def __init__(self, data:Industries, counter:TestCounter, riskfree:RiskFree, yearavg:int, ignore:float=0.0):
        self.data = data
        self.counter = counter
        self.riskfree = riskfree
        self.yearavg = yearavg
        self.ignore = ignore
        print(f"-----Tangency portfolio strategy {yearavg} years data initialized.-----")

    def _calcMeanCoMatrix(self):
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
        return mean_returns, cov_matrix

    #disabling trade with very small weight (ie 0.0001)
    def _remove_small_weights(self,normalized_weights):
        if self.ignore == 0:
            return normalized_weights
        for i in range(len(normalized_weights)):
            if abs(normalized_weights[i]) < self.ignore:
                normalized_weights[i] = 0.0
        return_weight = normalized_weights / np.sum(normalized_weights)
        return return_weight


    def _calcweight(self):
        mean_returns, cov_matrix = self._calcMeanCoMatrix()
        def objective(w):
            return - (w @ mean_returns) / np.sqrt(w @ cov_matrix @ w)   # maximize Sharpe → minimize negative
        constraints = [
            {'type': 'eq',   'fun': lambda w: np.sum(w) - 1},   # sum to 1
        ]
        bounds = [(-1, 1) for _ in range(len(mean_returns))]                    # no short, no >100%
        result = minimize(objective, x0=np.ones(len(mean_returns))/len(mean_returns), method='SLSQP',
                      bounds=bounds, constraints=constraints)
        normalized_weights = self._remove_small_weights(result.x)
        return list(normalized_weights)

    def calculateCurrent(self,amount):
        year = self.counter.getyear()
        month = self.counter.getmonth()
        weights = self._calcweight()
        industries_list = self.data.industries_list()
        revenue_percentage = 0.0
        ##print(f"Calculating for Year: {year}, Month: {month} with weights: {weights}")
        for ind, weight in zip(industries_list, weights):
            #print(f"Industry: {ind}, Weight: {weight:.4f}")
            value = self.data.get(ind, year, month)
            if value is not None:
                revenue_percentage += value * weight
            else:
                raise ValueError(f"No data for industry: {ind} in {year}-{month}")
        #print(f"Total revenue percentage: {revenue_percentage:.4f}%")
        amount = (1 + revenue_percentage / 100) * amount
        return amount

    def progressCounter(self):
        self.counter.progress()

class TangencyNoSS(Tangency):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("!! No short-selling version initialized !!")

    def _calcweight(self):
        mean_returns, cov_matrix = self._calcMeanCoMatrix()
        def objective(w):
            return - (w @ mean_returns) / np.sqrt(w @ cov_matrix @ w)   # maximize Sharpe → minimize negative
        constraints = [
            {'type': 'eq',   'fun': lambda w: np.sum(w) - 1},   # sum to 1
        ]
        bounds = [(0, 1) for _ in range(len(mean_returns))]                    # no short, no >100%
        result = minimize(objective, x0=np.ones(len(mean_returns))/len(mean_returns), method='SLSQP',
                      bounds=bounds, constraints=constraints)
        normalized_weights = self._remove_small_weights(result.x)
        return list(normalized_weights)