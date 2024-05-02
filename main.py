from fetch_data import *
from asset_optimization_file import *
import pandas as pd

def main():
    tickers_num = 10  # Specify the number of tickers you want to fetch
    start_date = "2017-01-01"  # Define the start date
    tickers_list = fetch_tickers(DATA_WIKI_URL, tickers_num)
    stock_data = create_sample(tickers_list, start_date)

    seed_everything()
    mean_returns, cov_matrix = stock_returns(stock_data)
    optimal_weights_sharpe = max_sharpe_ratio(mean_returns, cov_matrix)
    optimal_weights_vol = min_volatility(mean_returns, cov_matrix)

    print("Ticker Symbols: ", tickers_list)
    print("Optimal weights for maximum Sharpe ratio:", optimal_weights_sharpe)
    print("Optimal weights for minimum volatility:", optimal_weights_vol)

if __name__ == "__main__":
    main()
