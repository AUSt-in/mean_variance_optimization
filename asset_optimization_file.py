import random
import numpy as np
import pandas as pd
from scipy.optimize import minimize

def seed_everything(seed=42):
    random.seed(seed)
    np.random.seed(seed)

def random_weights(num_assets):
    """Generate random weights for portfolio assets that sum to 1."""
    weights = np.random.rand(num_assets)
    return weights / np.sum(weights)

def calculate_returns(data, annual_days=252):
    """Calculate annualized mean returns and covariance matrix."""
    daily_returns = data.pct_change().dropna()
    mean_returns = daily_returns.mean() * annual_days
    cov_matrix = daily_returns.cov() * annual_days
    return mean_returns, cov_matrix

def portfolio_stats(weights, mean_returns, cov_matrix, risk_free_rate=0.02):
    """Calculate portfolio performance metrics."""
    portfolio_return = np.dot(weights, mean_returns)
    portfolio_volatility = np.sqrt(weights.T @ cov_matrix @ weights)
    sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_volatility
    return portfolio_return, portfolio_volatility, sharpe_ratio

def minimize_function(target_function, mean_returns, cov_matrix, bounds, constraints):
    """General function for optimization."""
    num_assets = len(mean_returns)
    initial_guess = num_assets * [1. / num_assets]
    result = minimize(target_function, initial_guess, args=(mean_returns, cov_matrix),
                      method='SLSQP', bounds=bounds, constraints=constraints)
    return result.x if result.success else None

def maximize_sharpe(mean_returns, cov_matrix, risk_free_rate=0.02):
    """Maximize Sharpe Ratio."""
    target_function = lambda weights, mean_returns, cov_matrix: -portfolio_stats(weights, mean_returns, cov_matrix, risk_free_rate)[2]
    bounds = [(0, 1)] * len(mean_returns)
    constraints = [{'type': 'eq', 'fun': lambda x: np.sum(x) - 1}]
    return minimize_function(target_function, mean_returns, cov_matrix, bounds, constraints)

def minimize_volatility(mean_returns, cov_matrix):
    """Minimize portfolio volatility."""
    target_function = lambda weights, mean_returns, cov_matrix: portfolio_stats(weights, mean_returns, cov_matrix)[1]
    bounds = [(0, 1)] * len(mean_returns)
    constraints = [{'type': 'eq', 'fun': lambda x: np.sum(x) - 1}]
    return minimize_function(target_function, mean_returns, cov_matrix, bounds, constraints)

# Load actual data
data_path = 'data/sp500_1990_2000.csv.csv'
data = pd.read_csv(data_path)
data['DATE'] = pd.to_datetime(data['DATE'], format='%m/%d/%Y')

stock_data = data.drop(columns=['DATE'])

mean_returns, cov_matrix = calculate_returns(stock_data)

optimal_weights_sharpe = maximize_sharpe(mean_returns, cov_matrix)
optimal_weights_vol = minimize_volatility(mean_returns, cov_matrix)

# Output results
print("Optimal weights for maximum Sharpe ratio:", optimal_weights_sharpe)
print("Optimal weights for minimum volatility:", optimal_weights_vol)
