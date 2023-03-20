# Capital Asset Pricing Model (CAPM) and Value at Risk Analysis

## This code outputs the following analysis on publicly traded security:
<code>
************************************************************************************
********  Capital Asset Pricing Model (CAPM) & Value at Risk (VaR) Analysis ********
************************************************************************************

Enter Stock Symbol : aapl
Enter Investment Horizon in Years : 5
Enter Initial Investment in $'s : 100000

Asset|Security: AAPL
	Look Back Period: 5 Years
	Total Trading Days: 1259 Days
	Start Price: $43.83 on 2018-03-19
	End Price: $155.0 on 2023-03-17
	Dollars Gains: $111.0 Per Share

CAPM Calculation Parameters used: 
	Stock Beta: 1.232 
	AAPL Average Yearly Return (5 Years): 50.7359%
	S&P 500 Average Yearly Return (5 Years): 8.87%
	Risk-Free-Return Period: 5 Yr T-Bond 
	Today's 5 Yr Treasury Bond Yield Used: As of 2023-03-19 20:40:53.438795, is 3.44%
	Investment Horizon: 5 Years from today (From 2023-03-19 until 2028-03-17)

CAPM: Expected 5 Years Risk Adjusted Return for AAPL Stock: 10.13%

Assume Initial Investment of $100000.0:
The Following 5 Years Future Values were Calculated Based on Continuation of Above % Returns:
	Future Bond Investment Value: $118,424.77**
	Future Stock investment Value: $778,185.63***

**Bond future value assumes no re-investment of coupon payments
***Stock investment assumes buy and hold for duration

Value at Risk (VaR) Analysis for AAPL Stock:
Using Confidence Level: 99.0% for VaR Calculations
Using Monte-Carlo Simulation Method:
	Value at Risk (VaR) as % of Price using Monte Carlo simulation: 5.1227%
	Value at Risk (VaR) using Monte Carlo simulation: $7.94 dollars
Using Variance-Covariance Method:
	Value at Risk (VaR) as % of Price using Variance-CoVariance Method: 4.91%
	Value at Risk (VaR) using Variance-CoVariance Method: $7.62

</code>
