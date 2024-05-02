import numpy as np
import pandas as pd
from scipy import optimize

def seed_everything(seed=42):
    np.random.seed(seed)
    np.random.seed(seed)

def random_weights(num_assets):
    weights = np.random.rand(num_assets)
    return weights / sum(weights)

def stock_returns(data, log_returns=False, annual_days=252):
    if log_returns:
        returns = data.pct_change().apply(lambda x: np.log(1+x))
    else:
        returns = data.pct_change()
    returns = returns.dropna()
    return returns.mean() * annual_days, returns.cov() * annual_days

def portfolio_performance(weights, mean_returns, covariance_matrix):
    returns = np.dot(weights, mean_returns)
    variance = np.dot(weights.T, np.dot(covariance_matrix, weights))
    return np.sqrt(variance), returns

def neg_sharpe_ratio(weights, mean_returns, covariance_matrix, risk_free_rate=0.02):
    std, ret = portfolio_performance(weights, mean_returns, covariance_matrix)
    return -(ret - risk_free_rate) / std

def max_sharpe_ratio(mean_returns, covariance_matrix, risk_free_rate=0.02):
    num_assets = len(mean_returns)
    args = (mean_returns, covariance_matrix, risk_free_rate)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = [(0.0, 1.0)] * num_assets
    initial_guess = num_assets * [1. / num_assets]
    result = optimize.minimize(neg_sharpe_ratio, initial_guess, args=args, method='SLSQP', bounds=bounds, constraints=constraints)
    return result.x if result.success else None

def min_volatility(mean_returns, cov_matrix):
    num_assets = len(mean_returns)
    constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})
    bounds = [(0.0, 1.0)] * num_assets
    initial_guess = np.array([1. / num_assets] * num_assets)

    # Correctly pass additional arguments to the function inside lambda
    result = optimize.minimize(lambda w, mean_returns, cov_matrix: portfolio_performance(w, mean_returns, cov_matrix)[0],
                               initial_guess,
                               args=(mean_returns, cov_matrix),  # passing mean_returns and cov_matrix as additional arguments
                               method='SLSQP',
                               bounds=bounds,
                               constraints=constraints)

    return result.x if result.success else None

