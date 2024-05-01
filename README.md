## Portfolio Optimization

This Python project implements portfolio optimization techniques to maximize the Sharpe ratio and minimize volatility using historical stock price data.

### Cloning the Repository
To clone the repository and navigate into the project directory, use the following commands:

```bash
git clone https://github.com/AUSt-in/mean_variance_optimization.git
cd mean_variance_optimization
```
## Installation of Dependencies

Before running the project, install the required Python libraries:

```bash
pip install -r requirements.txt
```

This will install libraries like `pandas`, `numpy`, and `scipy`, which are necessary for financial data analysis and optimization tasks.

## Usage

### Data Preparation

First, ensure that your stock price data is in a CSV file with columns for each stock and rows for each trading day. The script expects a 'DATE' column for dates and other columns for stock tickers with their respective price data.

### Running the Optimization

To perform portfolio optimization, run the `portfolio.py` script:

```bash
python asset_optimization_file.py
```

The script will read historical price data, compute daily returns, calculate mean returns and the covariance matrix of returns, and then find the optimal weights for the portfolio to either maximize the Sharpe ratio or minimize volatility.

## Output

The results of the portfolio optimization will be output to the console and also saved to a CSV file, `result.csv`, in the project directory. This file will contain the optimal asset weights along with performance metrics such as expected return, volatility, and the Sharpe ratio.

## Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request with your enhancements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
