# DASE3115 Engineering economics and finance Group Project 2
## Investment Strategy Development (Simulation)

### Abstract
This github repository is the Group Project 2 of Group 5 of HKU DASE3115 Engineering economics and finance in 2025-2026 semester 1.

The task of the project is to invest 1 million US dollars on the 30 industry pofolios (of stocks) in the US stock market for the time horizon from October 2010 to September 2020 (120 months in total). The performance of strategies are being evaluated at the end of each month and entire time horizon, i.e., September 2020.

### Investment Strategies
1. Average Monthly Return:
The algorithm calculates the average return of all the industry pofolios using the previous data and **ALL-IN** to the portfolio with best calculated performance. The implementations are in ```algorithms/average_monthly_return.py```

2. Same Period Maket Performance:
The algorithm calculates the average return of all the industry pofolios **same month in pervious years** and **ALL-IN** to the portfolio with best calculated performance. The implementations are in ```algorithms/same_period_maket_perf.py```

3. Do Nothing:
This algorithm literally does nothing to improve its return and getting interest with the risk free rate (ie 2000001 – 1-month rates on [CSRP](https://www.crsp.org/research/crsp-us-treasury-database/) )

4. Equally Weighted (Naive Method):
This algorithm evenly distribute the money into all 30 industry pofolios. Assets are rearranged every month

5. Global Minimum Variance: This algorithm calculates the investment weight of all 30 assets using previous data to find out a combination with the lowest overall variance. The algorithm recalculates the weight every month and  There is also a version which bans short sell. The implementations are in ```algorithms/globalminvar.py```

6. Tangency Profolio: This algorithms calculates the investments weight of all 30 assets using previous data to find out a combination with the highest [Sharpe ratio](https://en.wikipedia.org/wiki/Sharpe_ratio). The algorithm recalculates the weight every month and  There is also a version which bans short sell. The implementations are in ```algorithms/tangency.py```

### How to use
First, install python and install all the dependency by:
```
pip install -r requirements.txt
```
Then, run the program with provided datasets in ```datasets/```
```
py main.py
```
To change the years of data being calculated, change the ```YEAR_AVG``` value in ```main.py```
```python
YEAR_AVG = 50 ## Change this for different years of data used
```
