import random
import numpy as np
import pandas as pd
import yfinance as yf
from scipy.optimize import minimize
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


def seed_everything(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    np.random.default_rng(seed)

seed_everything()

def fetch_data(tickers, start_date, end_date):
    data = yf.download(tickers, start=start_date, end=end_date)
    return data['Adj Close']

def random_weights(num_assets):
    weights = np.random.rand(num_assets)
    return weights / np.sum(weights)

def calculate_returns(data, annual_days=252):
    daily_returns = data.pct_change().dropna()
    mean_returns = daily_returns.mean() * annual_days
    cov_matrix = daily_returns.cov() * annual_days
    return mean_returns, cov_matrix

def forecast_returns(data, days_ahead=5):
    reg = LinearRegression()
    predicted_returns = {}
    
    for ticker in data.columns:
        returns = data[ticker].pct_change().dropna()
        if len(returns) > days_ahead:  
            X = np.arange(len(returns)).reshape(-1, 1) 
            y = returns.values
            reg.fit(X[days_ahead:], y[:-days_ahead]) 
            prediction = reg.predict(X[-1].reshape(1, -1))
            predicted_returns[ticker] = prediction[0] 

    predicted_returns = pd.Series(predicted_returns) * 252
    return predicted_returns



def portfolio_stats(weights, mean_returns, cov_matrix, risk_free_rate=0.02):
    portfolio_return = np.dot(weights, mean_returns)
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_volatility
    return portfolio_return, portfolio_volatility, sharpe_ratio

def maximize_sharpe(mean_returns, cov_matrix, risk_free_rate=0.02):
    target_function = lambda weights, mean_returns, cov_matrix: -portfolio_stats(weights, mean_returns, cov_matrix, risk_free_rate)[2]
    num_assets = len(mean_returns)
    bounds = [(0, 1)] * num_assets
    constraints = [{'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1}]
    return minimize_function(target_function, mean_returns, cov_matrix, bounds, constraints)

def minimize_volatility(mean_returns, cov_matrix):
    target_function = lambda weights, mean_returns, cov_matrix: portfolio_stats(weights, mean_returns, cov_matrix)[1]
    num_assets = len(mean_returns)
    bounds = [(0, 1)] * num_assets
    constraints = [{'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1}]
    return minimize_function(target_function, mean_returns, cov_matrix, bounds, constraints)

def minimize_function(target_function, mean_returns, cov_matrix, bounds, constraints):
    num_assets = len(mean_returns)
    initial_guess = random_weights(num_assets)
    result = minimize(target_function, initial_guess, args=(mean_returns, cov_matrix),
                      method='SLSQP', bounds=bounds, constraints=constraints)
    return result.x if result.success else None


tickers = ['MMM', 'AOS', 'ABT', 'ABBV', 'ACN', 'ADBE', 'AMD', 'AES', 'AFL', 'A']
start_date = '2015-01-01'
end_date = '2020-01-01'

data = fetch_data(tickers, start_date, end_date)
mean_returns, cov_matrix = calculate_returns(data)
predicted_returns = forecast_returns(data)

optimal_weights_sharpe = maximize_sharpe(predicted_returns, cov_matrix)
optimal_weights_vol = minimize_volatility(predicted_returns, cov_matrix)

# Output results
print("Optimal weights for maximum Sharpe ratio:", optimal_weights_sharpe)
print("Optimal weights for minimum volatility:", optimal_weights_vol)
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))

ax[0].bar(tickers, optimal_weights_sharpe, color='blue')
ax[0].set_title('Optimal Weights for Maximum Sharpe Ratio')
ax[0].set_ylabel('Weight')
ax[0].set_ylim(0, 1)

ax[1].bar(tickers, optimal_weights_vol, color='green')
ax[1].set_title('Optimal Weights for Minimum Volatility')
ax[1].set_ylim(0, 1)
plt.tight_layout()
plt.show()