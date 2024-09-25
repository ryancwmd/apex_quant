from data_pipeline.retrieve_data import retrieve_data
from backtesting_engine.SimpleMovingAverage import SimpleMovingAverage
from backtesting_engine.MovingAverageCD import MovingAverageCD
import os.path as osp
import argparse

def supported_strategies(strategy, params):
    if strategy == 'simple moving average':
        return SimpleMovingAverage(**params)
    elif strategy == 'macd':
        return MovingAverageCD(**params)
    else:
        print('Could not find this trading strategy.')
        exit(1)

def read_clargs():
    parser = argparse.ArgumentParser(description='Parse Optional Arguments')
    parser.add_argument('-t', '--ticker', type=str, help='Forex Pair Ticker to Retreive from yfinance', default='EURUSD=X')
    parser.add_argument('-p', '--period', type=str, help='Period to retrieve data, eg 1y, 5d', default='1y')
    parser.add_argument('-i', '--interval', type=str, help='Interval to retrieve data, eg 1d, 1m', default='1d')
    parser.add_argument('-o', '--outdir', type=str, help='Directory to store the CSV forex pair data in', default='./../assets/forex_data/')
    parser.add_argument('-r', '--rprofile', type=str, help='Filepath to the risk management profile', default='./../assets/risk_management_profile.json')
    parser.add_argument('-s', '--strategy', type=str, help='Trading strategy to use', default='simple moving average')

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = read_clargs()
    fp = retrieve_data(args.outdir, args.ticker, args.period, args.interval)

    params = {
        'ticker': args.ticker,
        'data_fp': fp,
        'risk_management_profile_fp': args.rprofile
    }

    engine = supported_strategies(args.strategy, params)
    engine.run()
