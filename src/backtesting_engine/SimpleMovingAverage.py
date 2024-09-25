import numpy as np
from .Engine import Engine

class SimpleMovingAverage(Engine):
    def __init__(self, ticker, data_fp, risk_management_profile_fp, short_length=20, long_length=50):
        super().__init__(data_fp, risk_management_profile_fp, ticker, 'Simple Moving Average')

        self.short_length= short_length
        self.long_length = long_length

        self.short_avg = 0
        self.long_avg = 0
        self.short_start = 0
        self.long_start = 0

        self.short_avg_history: list = np.full(short_length, np.nan).tolist()
        self.long_avg_history: list = np.full(long_length, np.nan).tolist()

    def iterate(self, i):
        if i >= self.short_length:
            self.short_avg += (self.data[i] - self.data[self.short_start]) / self.short_length
            self.short_start += 1
            self.short_avg_history.append(self.short_avg)
        else:
            self.short_avg += self.data[i] / self.short_length

        if i >= self.long_length:
            self.long_avg += (self.data[i] - self.data[self.long_start]) / self.long_length
            self.long_start += 1
            self.long_avg_history.append(self.long_avg)
        else:
            self.long_avg += self.data[i] / self.long_length

    def get_indicator(self, i):
        if i >= self.long_length:
            if self.short_avg > self.long_avg and not self.position == 'bought':
                return 'bullish'
            elif self.position == 'bought' and (self.short_avg < self.long_avg or i == len(self.data) - 1):
                return 'bearish'
        else:
            return 'none' 
