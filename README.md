
## Asset Portfolio Optimization for Different Type of Investors

This Python project utilizes advanced portfolio optimization techniques to maximize the Sharpe ratio and minimize volatility using historical stock price data.

### Cloning the Repository
Clone the repository and navigate to the project directory with the following commands:

```bash
git clone https://github.com/AUSt-in/mean_variance_optimization.git
cd mean_variance_optimization
```



## Usage

### Data Preparation

Prepare your stock price data in a CSV file with a 'DATE' column and additional columns for each stock ticker, representing daily prices.

### Running the Optimization

Execute the portfolio optimization by running:

```bash
python asset_optimization_file.py
```

This script processes historical price data to compute daily returns, mean returns, covariance matrix of returns, and determines the optimal portfolio weights.

## Output

The optimization results, including the optimal asset weights and key performance metrics such as expected return, volatility, and the Sharpe ratio, are displayed in the console and saved to `result.csv` in the project directory.

## Contributing

We encourage contributions! If you have suggestions or enhancements, please fork the repository and submit a pull request.

## License

This project is open-sourced under the MIT License. For more details, see the [LICENSE](LICENSE) file.
```

This version incorporates clearer instructions and ensures consistency in the documentation format and command examples. It also emphasizes the open-source nature of the project and encourages community contributions.
