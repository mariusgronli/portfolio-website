import pandas as pd
import numpy as np
import yfinance as yf

class StockAnalysis(self,ticker,df):
    def __init__(self,ticker,df):
        self.ticker = ticker
        self.df = df

    def expected_return(self):
        self.df['returns'] = self.df.pct_change(1)
        daily_return = self.df['returns'].mean()
        annual_return = ((daily_return+1)**252-1)*100
        return annual_return

    def standard_deviation(self):
        self.df['returns'] = self.df.pct_change(1)
        daily_std = np.std(self.df['returns'])
        annual_std = np.sqrt(252)*daily_std*100
        return annual_std

    def sharpe_ratio(self):
        sharpe = self.expected_return()/self.standard_deviation()
        return sharpe
