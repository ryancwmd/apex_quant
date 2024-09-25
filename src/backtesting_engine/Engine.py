import pandas as pd
import json
import math
import numpy as np
import statistics
import matplotlib.pyplot as plt
import csv

class Engine:
    def __init__(self, data_fp, risk_management_profile_fp, ticker, strategy):
        self.ticker = ticker
        self.strategy = strategy
        self.df = pd.read_csv(data_fp)
        self.data = self.df['Close'].to_numpy()
        self.dates = self.df['Date'].to_numpy()

        with open(risk_management_profile_fp, 'r') as file:
            risk_management_profile = json.load(file)

        self.initial_capital = risk_management_profile['initial_capital']
        self.capital = self.initial_capital
        self.position_limit = risk_management_profile['position_limit']
        self.loss_cap = risk_management_profile['loss_cap']
        self.risk_management_actions = []

        # used to record trades for evaluation or risk management
        self.trades = []

        # current position, bought, sold, none
        self.position = 'none'

        # number of stock owned
        self.position_size = 0

        # value at which we bought the stock (not total position value)
        self.position_value = 0

        self.total_loss = 0
        self.total_profit = 0

        self.return_history = [np.nan]
        self.portfolio_history = []

    # these two methods are for subclass to implement, they facilitate modularity for different strategies
    def iterate(self, i):
        pass
    def get_indicator(self, i):
        pass

    def calculate_position_size(self, i):
        """
        Calculates how much of the stock to buy.
        """
        return math.floor(self.capital * self.position_limit / self.data[i])

    def run(self):
        """Runs the engine."""

        # iterate through each datetime
        for i in range(len(self.data)):
            # updates the portfolio history if we have stock purchased
            if self.position == 'bought':
                stock_value = self.position_size * (self.data[i] - self.position_value)
                self.portfolio_history.append(stock_value + self.capital)
                if i > 0: #appends return history given we are at i >= 1
                    self.return_history.append((self.portfolio_history[i] - self.portfolio_history[i - 1]) / (self.portfolio_history[i - 1]))
            else: # otherwise if we have no stock purchased just append our stagnant capital
                self.portfolio_history.append(self.capital)

            # strategy dependent iteration
            self.iterate(i)

            # strategy dependent indicators
            indicator = self.get_indicator(i)
            if indicator == 'bullish': # buy
                self.position = 'bought'
                self.position_size = self.calculate_position_size(i)
                self.position_value = self.data[i]
                self.trades.append({
                    'date': self.dates[i],
                    'type': self.position,
                    'value': self.position_value,
                    'size': self.position_size,
                    'change': None,
                    'idx': i,
                })
            elif indicator == 'bearish': # sell
                self.capital += stock_value

                self.position = 'sold'
                self.trades.append({
                    'date': self.dates[i],
                    'type': self.position,
                    'value': self.data[i],
                    'size': self.position_size,
                    'change': stock_value,
                    'idx': i,
                })
                
                self.position_size = 0
                self.position_value = 0

                if stock_value >= 0:
                    self.total_profit += stock_value
                else:
                    self.total_loss += stock_value

            # if a stop loss has occurred
            if self.total_loss > self.initial_capital * self.loss_cap:
                self.management_actions = self.trades
                self.management_actions.append({
                    'date': self.dates[i],
                    'type': 'stop/loss',
                    'value': self.total_loss,
                    'idx': i,
                })
                self.stop_loss()
                break

        # evaluate our results
        self.evaluate()
    
    def evaluate(self):
        """Generates evaluation of the trading strategy's success."""
        self.print_statistics()
        self.plot_data()

    def print_statistics(self):
        """Prints relevant statistics."""
        # total profit/loss
        PnL = self.total_profit + self.total_loss

        # number of trades
        trades = len(self.trades)

        # winrate of trades (making profit / total trades)
        winrate = sum(1 for item in self.trades if item['type'] == 'sold' and item['change'] > 0) / trades

        # calculating sharpe ratio from return history
        stdv_returns = statistics.stdev(self.return_history[1:])
        Rp = statistics.mean(self.return_history[1:])
        Rf = 0.015
        sharpe = (Rp - Rf) / stdv_returns

        print(f'''
        Statistics:\n
        PnL: {PnL}\n
        Number of Trades: {trades}\n
        Winrate: {winrate}\n
        Sharpe Ratio: {sharpe}''')

    def plot_data(self):
        """Creates a matplotlib.pyplot line plot to represent the equity over time."""
        axes = plt.subplots()[1]
        axes.set_xticks([])
        axes.plot(self.dates, self.portfolio_history, color='black')
        axes.set_title(f'{self.ticker} {self.strategy}')

        plt.show()

    def stop_loss(self):
        """Writes risk management details to a CSV file in ~/assets."""
        filepath = f'./../../assets/{self.ticker+self.strategy}.csv'
        print('Stop Loss Occurred.')
        # open in append mode not write mode
        with open(filepath, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.management_actions[0].keys())

            # write header only if file is empty
            if file.tell() == 0:
                writer.writeheader()    

            for action in self.management_actions:
                writer.writerow(action) 
        self.dates = self.dates[:self.management_actions[-1]['idx']]


