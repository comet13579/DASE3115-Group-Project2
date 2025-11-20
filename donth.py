from testcounter import TestCounter
from riskfree import RiskFree


class DoNothing:
    def __init__(self, risk:RiskFree, counter:TestCounter):
        self.risk = risk
        self.counter = counter
        print("-----Do Nothing (Risk Free) initialized.-----")

    def calculateCurrent(self,amount):
        return (1 + self.risk.get(self.counter.getyear(), self.counter.getmonth()) / 100) * amount

    def progressCounter(self):
        self.counter.progress()