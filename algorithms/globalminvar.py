from tools.industries import Industries
from tools.testcounter import TestCounter
import numpy as np
from scipy.optimize import minimize


## A strategy that calculates the global minimum variance portfolio based on historical data.
class GlobalMinVar:
    def __init__(self, data:Industries, counter:TestCounter, yearavg:int):
        self.data = data
        self.counter = counter
        self.yearavg = yearavg
        print(f"-----Global minimum variance portfolio strategy {yearavg} years data initialized.-----")

    def _calcCoMatrix(self):
        year = self.counter.getyear()
        month = self.counter.getmonth()
        industries_list = self.data.industries_list()
        datacalc = []
        for ind in industries_list:
            counter = self.yearavg * 12
            yearmonth = TestCounter.month_minus_1(year,month)
            temp = []
            while counter != 0:
                temp.append(self.data.get(ind,yearmonth[0],yearmonth[1]))
                counter -= 1
                yearmonth = TestCounter.month_minus_1(yearmonth[0],yearmonth[1])
            datacalc.append(temp)
        datacalc = np.array(datacalc)
        cov_matrix = np.cov(datacalc, rowvar=True)
        return cov_matrix
    
    def _calcweight(self):
        cov_matrix = self._calcCoMatrix()
        vector_of_ones = np.ones(cov_matrix.shape[0])
        inv_cov_matrix = np.linalg.inv(cov_matrix)
        weights = inv_cov_matrix.dot(vector_of_ones)
        normalized_weights = weights / np.linalg.norm(weights)
        return list(normalized_weights)


    def calculateCurrent(self,amount):
        year = self.counter.getyear()
        month = self.counter.getmonth()
        weights = self._calcweight()
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

class GobalMinVarNoSS(GlobalMinVar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("!! No short-selling version initialized !!")

    def _calcweight(self):
        cov_matrix = self._calcCoMatrix()
        def objective(w):
            return w @ cov_matrix @ w
        constraints = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1}]
        bounds = [(0, 1) for _ in range(cov_matrix.shape[0])]
        result = minimize(objective, x0=np.ones(cov_matrix.shape[0])/cov_matrix.shape[0], method='SLSQP',
                      bounds=bounds, constraints=constraints)
        return list(result.x)