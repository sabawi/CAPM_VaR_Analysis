#!/usr/bin/env python
# coding: utf-8

# In[20]:


import pandas as pd
import numpy as np
import datetime
import yfinance as yf
from scipy.stats import norm


def var_cov_var2(P, c, mu, sigma):
    alpha = norm.ppf(1-c, mu, sigma)
    print(f"alpha = {alpha}")
    # return P - P*(alpha + 1)
    return -(P * alpha)

def monte_carlo_var2(P, c, mu, sigma, T, iterations):
    dt = 1/252
    returns = np.exp((mu - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * np.random.normal(size=(iterations, T)))
    P_T = P * np.cumprod(returns, axis=1)
    P_T_sorted = np.sort(P_T[:, -1])
    return P - P_T_sorted[int(iterations * (1 - c))]


def var_covariance3(stock_prices, time_horizon, confidence_level):
    returns = np.diff(stock_prices) / stock_prices[:-1] # Calculate daily returns
    mu = np.mean(returns)
    sigma = np.std(returns)

    # Calculate the z-score corresponding to the confidence level
    z = norm.ppf(1 - confidence_level)

    # Calculate the daily return VaR
    daily_var = stock_prices[-1] * sigma * z * np.sqrt(time_horizon)
    daily_pct_var = sigma * z * np.sqrt(time_horizon)
    var_pct = daily_pct_var * np.sqrt(time_horizon) * 100

    # Calculate the VaR for the holding period
    var = daily_var * np.sqrt(time_horizon)
    print("Using Variance-Covariance Method:")
    print(f'\tValue at Risk (VaR) as % of Price using Variance/CoVariance Method: {round(var_pct,2)}%')
    print(f'\tValue at Risk (VaR) using Variance/CoVariance Method: ${round(var,2)}')

    return var_pct, var

def monte_carlo_var4(stock_price, c, T, iterations, mu, sigma, n_days=2):
    dt = 1/252
    N = n_days
    S_0 = stock_price.values[-n_days:]
    S_T = S_0*np.exp(np.cumsum((mu - 0.5*sigma**2)*dt + sigma*np.sqrt(dt)*np.random.normal(size=(iterations, N, T)), axis=2))
    S_T_sorted = np.sort(S_T[:, -1, :])
    P_T = np.mean(S_T, axis=0)
    VaR = P_T - S_T_sorted[int((1-c)*iterations), :]
    print("Using Monte Carlo Method:")
    print(f"\tValue at Risk (VaR) as % of Price using Monte Carlo Method: {round(np.mean(VaR/P_T)*100, 2)}%")
    print(f"\tValue at Risk (VaR) using Monte Carlo Method: ${round(np.mean(VaR), 2)}")
    return VaR/P_T, VaR

def var_covariance(last_stock_price, time_horizon, std_dev_return, confidence_level):
    # Calculate the z-score corresponding to the confidence level
    z = norm.ppf(1 - confidence_level)

    # Calculate the daily return VaR
    daily_var = last_stock_price * std_dev_return * z * np.sqrt(time_horizon)
    daily_pct_var = std_dev_return * z * np.sqrt(time_horizon)
    var_pct = daily_pct_var * np.sqrt(time_horizon) * 100

    # Calculate the VaR for the holding period
    var = daily_var * np.sqrt(time_horizon)
    print("Using Variance-Covariance Method:")
    print(f'\tValue at Risk (VaR) as % of Price using Variance-CoVariance Method: {round(var_pct,2)}%')
    print(f'\tValue at Risk (VaR) using Variance-CoVariance Method: ${round(var,2)}')
    return var_pct, var

def var_monte_carlo(data, time_horizon, num_simulations, mean_return, std_dev_return, confidence_level) :
    # Run Monte Carlo simulations to generate potential future stock prices
    simulated_prices = np.zeros((time_horizon + 1, num_simulations))
    simulated_prices[0] = data.iloc[-1]
    for t in range(1, time_horizon + 1):
        simulated_prices[t] = simulated_prices[t - 1] * np.exp((mean_return - 0.5 * std_dev_return ** 2) * time_horizon + std_dev_return * np.sqrt(time_horizon) * norm.ppf(np.random.rand(num_simulations)))

    # Calculate potential losses from simulations and sort them in ascending order
    potential_losses = (simulated_prices[-1] - simulated_prices[0]) / simulated_prices[0]
    potential_losses_sorted = np.sort(potential_losses)

    # Calculate VaR at specified confidence level from sorted potential losses
    # var_monte_carlo = potential_losses_sorted[int((1 - confidence_level) * num_simulations)]
    
    var_percent = potential_losses_sorted[int((1 - confidence_level) * num_simulations)]
    var_dollar = var_percent * simulated_prices[0]
    index = np.argmax(potential_losses_sorted >= -var_percent)
    var_dollar_selected = var_dollar[index]  
      
    print("Using Monte-Carlo Simulation Method:")
    print(f'\tValue at Risk (VaR) as % of Price using Monte Carlo simulation: {round(100 * var_percent,4)}%')    
    print(f'\tValue at Risk (VaR) using Monte Carlo simulation: ${round(var_dollar_selected,2)} dollars')
    
    return var_percent, var_dollar_selected

def calculate_beta(stock_data, market="^GSPC", strPeriod="3y") -> float:

    # Calculate the stock's returns
    stock_returns = stock_data['returns']

    # If a market index is specified, get the market data and calculate the market's returns
    if market:
        market_data = yf.Ticker(market).history(period=strPeriod)
        market_data = market_data.tz_localize(None)  # convert to timezone-naive DataFrame
        market_returns = market_data["Close"].pct_change().dropna()
    else:
        market_returns = np.ones_like(stock_returns)

    # Calculate the stock's beta using the returns
    beta = stock_returns.cov(market_returns) / market_returns.var()

    return beta, market_data

print("************************************************************************************")
print("********  Capital Asset Pricing Model (CAPM) & Value at Risk (VaR) Analysis ********")
print("************************************************************************************\n")
stock_symbol = str(input("Enter Stock Symbol : ")).upper()
investment_period_years = int(input("Enter Investment Horizon in Years : "))
initial_investment = float(input("Enter Initial Investment in $'s : "))

today = datetime.datetime.today()
today_str= today.strftime("%Y-%m-%d")
beta_lookback_period = 5

# Stringify periods 
stock_data_period = f"{beta_lookback_period}y"
bond_maturity = f"{investment_period_years} Yr"

# Download daily price data for the stock for the last n years
stock_data = yf.download(stock_symbol, period=stock_data_period)

# Calculate daily returns
stock_data['returns'] = stock_data['Close'].pct_change().dropna()

# Calculate average daily return and daily volatility over the last n years
mu_daily = np.mean(stock_data['returns'])

# Calculate average Yearly returns ((last - first)/first)/years
mu_yearly = ((stock_data.iloc[-1].Close - stock_data.iloc[0].Close) / stock_data.iloc[0].Close)/beta_lookback_period

# print(f"mu_yearly = {mu_yearly*100}")
sigma = np.std(stock_data['returns'])

# Define the risk-free rate (use 10-year Treasury bond yield as an example)
ustd_url = "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/"
this_year = str(pd.Timestamp.now().year)
last_five_years = [str(i) for i in range(int(this_year)-5, int(this_year))]
ustd_rates = pd.read_csv(ustd_url+this_year+"/all?type=daily_treasury_yield_curve&field_tdr_date_value="+last_five_years[0]+"&page&_format=csv")

# print(ustd_rates)

risk_free_rate = ustd_rates.iloc[0][bond_maturity]/100

# Calculate expected return using CAPM
stock_beta, market_data = calculate_beta(stock_data, market="^GSPC",strPeriod=stock_data_period)

market_returns_yearly = ((market_data.iloc[-1].Close - market_data.iloc[0].Close) / market_data.iloc[0].Close)/beta_lookback_period

expected_return = risk_free_rate + stock_beta * (market_returns_yearly - risk_free_rate)

end_of_bond_invest = today + datetime.timedelta(days=investment_period_years*365)  # add N years (approximating 1 year as 365 days)
end_of_bond_invest_str = end_of_bond_invest.strftime("%Y-%m-%d")

print(f"Asset|Security: {stock_symbol}")
print(f"\tLook Back Period: {beta_lookback_period} Years")
print(f"\tTotal Trading Days: {len(stock_data)} Days")
print(f"\tStart Price: ${round(stock_data.iloc[0].Close,2)} on {stock_data.index[0].strftime('%Y-%m-%d')}")
print(f"\tEnd Price: ${round(stock_data.iloc[-1].Close,2)} on {stock_data.index[-1].strftime('%Y-%m-%d')}")
print(f"\tDollars Gains: ${round(stock_data.iloc[-1].Close - round(stock_data.iloc[0].Close),2)} Per Share")

print(f"\nCAPM Calculation Parameters used: \
\n\tStock Beta: {round(stock_beta,3)} \
\n\t{stock_symbol} Average Yearly Return ({beta_lookback_period} Years): {round(mu_yearly*100,4)}%\
\n\tS&P 500 Average Yearly Return ({beta_lookback_period} Years): {round(market_returns_yearly*100,2)}%\
\n\tRisk-Free-Return Period: {bond_maturity} T-Bond \
\n\tToday's {bond_maturity} Treasury Bond Yield Used: As of {today}, is {risk_free_rate*100}%\
\n\tInvestment Horizon: {investment_period_years} Years from today (From {today_str} until {end_of_bond_invest_str})")

print('\nCAPM: Expected {} Years Risk Adjusted Return for {} Stock: {:.2f}%'.format(investment_period_years,stock_symbol,expected_return * 100))

print(f"\nAssume Initial Investment of ${initial_investment}:")
# Calculate the future value of a $10,000 bond investment after 5 years
bond_fv = initial_investment*(1 + risk_free_rate)**investment_period_years

# Calculate the future value of a $10,000 stock investment after 5 years
stock_fv = initial_investment*(1 + mu_yearly)**investment_period_years

# Print the total return of the bond investment and the stock investment
print(f"The Following {investment_period_years} Years Future Values were Calculated Based on Continuation of Above % Returns:")
print("\tFuture Bond Investment Value: ${:,.2f}**".format(bond_fv))
print("\tFuture Stock investment Value: ${:,.2f}***".format(stock_fv))

print("\n**Bond future value assumes no re-investment of coupon payments\n***Stock investment assumes buy and hold for duration")



# In[29]:


# VaR Analysis

print(f"\nValue at Risk (VaR) Analysis for {stock_symbol} Stock:")
# Set the confidence level for VaR calculation (e.g. 95% confidence level)
confidence_level = 1.0 - 0.99
print(f"Using Confidence Level: {(1.0-confidence_level)*100}% for VaR Calculations")

# Calculate the log returns of the stock
log_returns = np.log(1 + stock_data['returns'])

# Set the number of simulations and time horizon for VaR calculation
num_simulations = 1000000
# time_horizon = 1

trading_days = 50  

# Calculate the mean and standard deviation of log returns
mean_return = log_returns.mean()
std_dev_return = log_returns.std()

# monte_carlo_var4(stock_price, c, T, iterations, mu, sigma, n_days=2)
# var_monte_carlo (data, time_horizon, num_simulations, mean_return, std_dev_return, confidence_level)
var_mc_pct, var_mc_dol = var_monte_carlo(stock_data.Close,
                                          1,
                                        #   investment_period_years*trading_days,
                                          num_simulations,
                                          mean_return,
                                          std_dev_return,
                                          confidence_level)

var_cov_pct, var_cov_dol = var_covariance(stock_data.Close.iloc[-1], 1, std_dev_return, confidence_level)



# In[ ]:


# if __name__ == "__main__":
#     main()

