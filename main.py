from algorithms.equally_weighted import EquallyWeighted
from algorithms.same_period_maket_perf import SamePeriodMarketPerf
from algorithms.average_monthly_return import AverageMonthlyReturn
from algorithms.globalminvar import GlobalMinVar, GobalMinVarNoSS
from algorithms.tangency import Tangency, TangencyNoSS
from algorithms.donth import DoNothing
from tools.testcounter import TestCounter
from tools.industries import Industries
from tools.riskfree import RiskFree

import matplotlib.pyplot as plt

YEAR_AVG = 30 ##Change this for different years of data used
IGNORE_THRESHOLD = 0.1 ##Change this for different threshold for small weights

def main():
    data = Industries('datasets/industries.csv')
    xaxis = range(120)

    counter = TestCounter()
    equally_weighted = EquallyWeighted(data, counter)
    amount = 1000000.0
    ew = [0]*120
    for i in range(120):  # Simulate 10 years
        amount = equally_weighted.calculateCurrent(amount)
        #print(f"New amount after iteration {i}: {amount:.2f}")
        ew[i] = amount
        equally_weighted.progressCounter()
    print("Simulation complete, the final amount is {:.2f}".format(amount))

    counter = TestCounter()
    same_period_perf = SamePeriodMarketPerf(data, counter, yearavg=YEAR_AVG)
    amount = 1000000.0
    spm = [0]*120
    for i in range(120):  # Simulate 10 years
        amount = same_period_perf.calculateCurrent(amount)
        #print(f"New amount after iteration {i}: {amount:.2f}")
        spm[i] = amount
        same_period_perf.progressCounter()
    print("Simulation complete, the final amount is {:.2f}".format(amount))

    counter = TestCounter()
    average_monthly_return = AverageMonthlyReturn(data, counter, yearavg=YEAR_AVG)
    amount = 1000000.0
    amr = [0]*120
    for i in range(120):  # Simulate 10 years
        amount = average_monthly_return.calculateCurrent(amount)
        #print(f"New amount after iteration {i}: {amount:.2f}")
        amr[i] = amount
        average_monthly_return.progressCounter()
    print("Simulation complete, the final amount is {:.2f}".format(amount))

    counter = TestCounter()
    global_min_var = GlobalMinVar(data, counter, yearavg=YEAR_AVG, ignore = 0.0)
    amount = 1000000.0
    gmv = [0]*120
    for i in range(120):  # Simulate 10 years
        amount = global_min_var.calculateCurrent(amount)
        #print(f"New amount after iteration {i}: {amount:.2f}")
        gmv[i] = amount
        global_min_var.progressCounter()
    print("Simulation complete, the final amount is {:.2f}".format(amount))

    counter = TestCounter()
    global_min_var_no_ss = GobalMinVarNoSS(data, counter, yearavg=YEAR_AVG, ignore = 0.0)
    amount = 1000000.0
    gmv_no_ss = [0]*120
    for i in range(120):  # Simulate 10 years
        amount = global_min_var_no_ss.calculateCurrent(amount)
        #print(f"New amount after iteration {i}: {amount:.2f}")
        gmv_no_ss[i] = amount
        global_min_var_no_ss.progressCounter()
    print("Simulation complete, the final amount is {:.2f}".format(amount))

    riskfreedata = RiskFree('datasets/risk-free.csv')
    counter = TestCounter()
    tangency = Tangency(data, counter,riskfreedata, yearavg=YEAR_AVG)
    amount = 1000000.0
    tg = [0]*120
    total_sharpe = 0.0
    for i in range(120):  # Simulate 10 years
        amount = tangency.calculateCurrent(amount)
        #tangency.print_sharpe()
        total_sharpe += tangency.sharpe_ratio()
        #print(f"New amount after iteration {i}: {amount:.2f}")
        tg[i] = amount
        tangency.progressCounter()
    print("Average Sharpe ratio over the period is {:.4f}".format(total_sharpe / 120))
    print("Simulation complete, the final amount is {:.2f}".format(amount))

    counter = TestCounter()
    tangency_no_ss = TangencyNoSS(data, counter,riskfreedata, yearavg=YEAR_AVG)
    amount = 1000000.0
    tg_no_ss = [0]*120
    total_sharpe = 0.0
    for i in range(120):  # Simulate 10 years
        amount = tangency_no_ss.calculateCurrent(amount)
        #tangency_no_ss.print_sharpe()
        total_sharpe += tangency_no_ss.sharpe_ratio()
        #print(f"New amount after iteration {i}: {amount:.2f}")
        tg_no_ss[i] = amount
        tangency_no_ss.progressCounter()
    print("Average Sharpe ratio over the period is {:.4f}".format(total_sharpe / 120))
    print("Simulation complete, the final amount is {:.2f}".format(amount))

    counter = TestCounter()
    tangency_ignore = Tangency(data, counter,riskfreedata, yearavg=YEAR_AVG, ignore = IGNORE_THRESHOLD)
    amount = 1000000.0
    tg_ignore = [0]*120
    total_sharpe = 0.0
    for i in range(120):  # Simulate 10 years
        amount = tangency_ignore.calculateCurrent(amount)
        #tangency_ignore.print_sharpe()
        total_sharpe += tangency_ignore.sharpe_ratio()
        #print(f"New amount after iteration {i}: {amount:.2f}")
        tg_ignore[i] = amount
        tangency_ignore.progressCounter()
    print("Average Sharpe ratio over the period is {:.4f}".format(total_sharpe / 120))
    print("Simulation complete, the final amount is {:.2f}".format(amount))

    counter = TestCounter()
    tangency_no_ss_ignore = TangencyNoSS(data, counter,riskfreedata, yearavg=YEAR_AVG, ignore = IGNORE_THRESHOLD)
    amount = 1000000.0
    tg_no_ss_ignore = [0]*120
    total_sharpe = 0.0
    for i in range(120):  # Simulate 10 years
        amount = tangency_no_ss_ignore.calculateCurrent(amount)
        #tangency_no_ss_ignore.print_sharpe()
        total_sharpe += tangency_no_ss_ignore.sharpe_ratio()
        #print(f"New amount after iteration {i}: {amount:.2f}")
        tg_no_ss_ignore[i] = amount
        tangency_no_ss_ignore.progressCounter()
    print("Average Sharpe ratio over the period is {:.4f}".format(total_sharpe / 120))
    print("Simulation complete, the final amount is {:.2f}".format(amount))

    counter = TestCounter()
    donothing = DoNothing(riskfreedata, counter)
    amount = 1000000.0
    dn = [0]*120
    for i in range(120):  # Simulate 10 years
        amount = donothing.calculateCurrent(amount)
        #print(f"New amount after iteration {i}: {amount:.2f}")
        dn[i] = amount
        donothing.progressCounter()
    print("Simulation complete, the final amount is {:.2f}".format(amount))

    #########################################################################
    ## GRAPH PLOTTING
    plt.plot(xaxis, ew, label='Equally Weighted')
    plt.plot(xaxis, spm, label='Same Period Market Performance')
    plt.plot(xaxis, amr, label='Average Monthly Return')
    plt.plot(xaxis, gmv, label='Global Minimum Variance')
    plt.plot(xaxis, gmv_no_ss, label='Global Minimum Variance No Short Selling')
    plt.plot(xaxis, tg, label='Tangency Portfolio')
    plt.plot(xaxis, tg_no_ss, label='Tangency Portfolio No Short Selling')
    plt.plot(xaxis, tg_ignore, label=f'Tangency Portfolio (ignore {IGNORE_THRESHOLD} weights)')
    plt.plot(xaxis, tg_no_ss_ignore, label=f'Tangency Portfolio No Short Selling (ignore {IGNORE_THRESHOLD} weights)')
    plt.plot(xaxis, dn, label='Do Nothing (Risk-Free)')
    plt.xlabel('Epoches (Months)')
    plt.ylabel('Amount ($)')
    plt.title(f'Portfolio Strategy Performance Over Time (Using {YEAR_AVG} Years of Data)')
    plt.grid(True)
    plt.xlim(0, 120)
    plt.ylim(0, max(max(ew), max(spm), max(amr), max(gmv), max(gmv_no_ss), max(tg), max(tg_no_ss), max(tg_ignore), max(tg_no_ss_ignore), max(dn)) * 1.1)
    plt.legend()
    plt.gcf().set_size_inches(16, 9)
    plt.savefig(f"portfolio_perf_{YEAR_AVG}_years.png",dpi=100)
    plt.show()

if __name__ == '__main__':
    main()