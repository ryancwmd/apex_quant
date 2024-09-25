import yfinance as yf
import os.path as osp

asset_fp = "./../assets/"

def retrieve_data(base_fp, ticker, period, interval):
    """
    This function stores financial history data for a particular forex pair. The data is
    stored in a csv file denoted `~/assets/forex_data/[ticker-'=X']_[period]_[interval].csv` 

    Parameters
    ----------
        base_fp: str
            File path to where the data should be written.
        ticker: str
            Ticker for forex pair
        period: str
            Period to retrieve data for, examples include 5d, 1m, 6m, 1yr, ...
        interval: str
            Interval on which to retrieve data, examples include 1m, 1d

    Returns
    -------
        str
            fp to csv file
    """
    if not (base_fp.endswith('/')):
        base_fp += '/'

    fp = osp.join(base_fp, f'{ticker[:-2]}_{period}_{interval}.csv')

    # initialize ticker
    forex = yf.Ticker(ticker)
    
    # retrieve history
    df = forex.history(period=period, interval=interval) 

    # filter nan values
    df = df.dropna()
    
    df.to_csv(fp)

    return fp