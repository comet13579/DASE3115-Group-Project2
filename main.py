from industries import Industries
from equally_weighted import EquallyWeighted
from same_period_maket_perf import SamePeriodMarketPerf
from average_monthly_return import AverageMonthlyReturn
from globalminvar import GlobalMinVar
from tangency import Tangency
from donth import DoNothing
from testcounter import TestCounter

YEAR_AVG = 5

def main():
    data = Industries('industries.csv')
    counter = TestCounter()
    ew = EquallyWeighted(data, counter)

    # Example calculation
    amount = 1000000.0
    for i in range(120):  # Simulate 10 years
        amount = ew.calculateCurrent(amount)
        #print(f"New amount after iteration {i}: {amount:.2f}")
        ew.progressCounter()
    print("Simulation complete, the final amount is {:.2f}".format(amount))

    counter = TestCounter()
    same_period_perf = SamePeriodMarketPerf(data, counter, yearavg=YEAR_AVG)
    amount = 1000000.0
    for i in range(120):  # Simulate 10 years
        amount = same_period_perf.calculateCurrent(amount)
        #print(f"New amount after iteration {i}: {amount:.2f}")
        same_period_perf.progressCounter()
    print("Simulation complete, the final amount is {:.2f}".format(amount))

    counter = TestCounter()
    same_period_perf = AverageMonthlyReturn(data, counter, yearavg=YEAR_AVG)
    amount = 1000000.0
    for i in range(120):  # Simulate 10 years
        amount = same_period_perf.calculateCurrent(amount)
        #print(f"New amount after iteration {i}: {amount:.2f}")
        same_period_perf.progressCounter()
    print("Simulation complete, the final amount is {:.2f}".format(amount))

    counter = TestCounter()
    global_min_var = GlobalMinVar(data, counter, yearavg=YEAR_AVG)
    amount = 1000000.0
    for i in range(120):  # Simulate 10 years
        amount = global_min_var.calculateCurrent(amount)
        #print(f"New amount after iteration {i}: {amount:.2f}")
        global_min_var.progressCounter()
    print("Simulation complete, the final amount is {:.2f}".format(amount))

    import riskfree
    riskfreedata = riskfree.RiskFree('risk-free.csv')
    counter = TestCounter()
    tangency = Tangency(data, counter,riskfreedata, yearavg=YEAR_AVG)
    amount = 1000000.0
    for i in range(120):  # Simulate 10 years
        amount = tangency.calculateCurrent(amount)
        #print(f"New amount after iteration {i}: {amount:.2f}")
        tangency.progressCounter()
    print("Simulation complete, the final amount is {:.2f}".format(amount))

    counter = TestCounter()
    donothing = DoNothing(riskfreedata, counter)
    amount = 1000000.0
    for i in range(120):  # Simulate 10 years
        amount = donothing.calculateCurrent(amount)
        #print(f"New amount after iteration {i}: {amount:.2f}")
        donothing.progressCounter()
    print("Simulation complete, the final amount is {:.2f}".format(amount))

if __name__ == '__main__':
    main()