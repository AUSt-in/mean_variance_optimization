import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from argparse import ArgumentParser
import yfinance as yf
import datetime
import numpy as np
DATA_WIKI_URL = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

def fetch_tickers(data_url, tickers_num):
    """Download the data."""
    response = requests.get(data_url)
    assert response.status_code == 200, "Connection error"
    soup = BeautifulSoup(response.text, 'html.parser')
    indiatable = soup.find('table', {'class': "wikitable"})
    tickers_df = pd.read_html(str(indiatable))[0]
    if tickers_num > len(tickers_df):
        print("Please, enter number less than", len(tickers_df))
    return tickers_df['Symbol'].iloc[:tickers_num].tolist()  # Return a list of tickers

def create_sample(tickers_list, start_date, end_date=None):
    """
    Fetch data sample and save it.
    """
    os.makedirs('data', exist_ok=True)
    print("Downloading the data...")
    if not end_date:
        end_date = datetime.date.today()

    # Ensure tickers_list is a list of strings, not a numpy array
    if isinstance(tickers_list, np.ndarray):
        tickers_list = tickers_list.tolist()

    stock_data = yf.download(tickers_list, start=start_date, end=end_date)['Adj Close']
    print('Creating csv file...')
    stock_data.to_csv('data/stock_prices.csv')
    return stock_data

