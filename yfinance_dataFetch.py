import pandas as pd
from datetime import datetime
import yfinance as yf


def get_sp500_stocks():
    """
    Get the list of S&P 500 stocks from Wikipedia.
    :return: A list of S&P 500 stock symbols.
    """
    sp500_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    table = pd.read_html(sp500_url)
    sp500_df = table[0]
    return sp500_df['Symbol'].tolist()

# import cProfile
# import pstats
#
# cProfile.run('get_sp500_stocks()', 'output.pstats')
# # Load the profiling data
# p = pstats.Stats('output.pstats')
# p.sort_stats('cumulative').print_stats(10)

def get_ndx_stocks():
    """
    Get the list of Nasdaq-100 stocks from Wikipedia.
    :return: A list of Nasdaq-100 stock symbols.
    """
    ndx_url = 'https://en.wikipedia.org/wiki/Nasdaq-100'
    table = pd.read_html(ndx_url)
    ndx_df = table[4]  # The table containing Nasdaq-100 companies is the 5th table on the page
    return ndx_df['Ticker'].tolist()

class StockDataFetcher:
    def __init__(self, start_date, end_date, symbols=None):
        """
        Initialize the SP500DataFetcher with a start date and an end date.

        :param start_date: The start date for fetching historical data (format: 'YYYY-MM-DD').
        :param end_date: The end date for fetching historical data (format: 'YYYY-MM-DD').
        :param symbols: List of stock symbols to fetch data for. If None, fetches S&P 500 stocks.
        """
        self.start_date = start_date
        self.end_date = end_date
        if symbols == ["SPX500"]:
            self.symbols = get_sp500_stocks()
        elif symbols == ["NDX100"]:
            self.symbols = get_ndx_stocks()
        else:
            self.symbols = symbols

    def fetch_data(self):
        """
        Fetch historical adjusted close prices for S&P 500 stocks.

        :return: A DataFrame containing the adjusted close prices of S&P 500 stocks.
        """
        data_dict = {}
        for symbol in self.symbols:
            print(f"Fetching data for {symbol}...")
            try:
                stock_data = yf.download(symbol, start=self.start_date, end=self.end_date)
                data_dict[symbol] = stock_data['Adj Close']
            except Exception as e:
                print(f"Could not fetch data for {symbol}: {e}")
        # Combine all data into a single DataFrame
        closing_prices = pd.concat(data_dict, axis=1)

        return closing_prices

    def save_to_csv(self, df, filename, index=True):
        """
        Save the DataFrame to a CSV file.

        :param df: The DataFrame to save.
        :param filename: The name of the CSV file.
        """
        df.to_csv(filename, index=index)
        print(f"Data fetching complete. Saved to {filename}.")


# Example usage
if __name__ == "__main__":
    # Set the date range for the last 10 years
    #end_date = datetime.datetime.now()
    end_date = datetime.now()
    start_date = "2014-01-01"

    # fetcher = StockDataFetcher(start_date=start_date, end_date=end_date)
    fetcher = StockDataFetcher(start_date=start_date, end_date=end_date, symbols=['^NDX'])
    closing_prices = fetcher.fetch_data()
    fetcher.save_to_csv(closing_prices, 'NDX_2014_2024.csv')
    #fetcher.save_to_csv(closing_prices, 'sp500_closing_prices_last_10_years.csv')
