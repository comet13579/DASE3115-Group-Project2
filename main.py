from industries import Industries
from equally_weighted import EquallyWeighted
from same_period_maket_perf import SamePeriodMarketPerf
from average_monthly_return import AverageMonthlyReturn
from testcounter import TestCounter

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
    same_period_perf = SamePeriodMarketPerf(data, counter, yearavg=20)
    amount = 1000000.0
    for i in range(120):  # Simulate 10 years
        amount = same_period_perf.calculateCurrent(amount)
        #print(f"New amount after iteration {i}: {amount:.2f}")
        same_period_perf.progressCounter()
    print("Simulation complete, the final amount is {:.2f}".format(amount))

    counter = TestCounter()
    same_period_perf = AverageMonthlyReturn(data, counter, yearavg=20)
    amount = 1000000.0
    for i in range(120):  # Simulate 10 years
        amount = same_period_perf.calculateCurrent(amount)
        #print(f"New amount after iteration {i}: {amount:.2f}")
        same_period_perf.progressCounter()
    print("Simulation complete, the final amount is {:.2f}".format(amount))

if __name__ == '__main__':
    main()