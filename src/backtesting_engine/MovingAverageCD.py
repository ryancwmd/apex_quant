import numpy as np
from .Engine import Engine

class MovingAverageCD(Engine):
    def __init__(self, ticker, data_fp, risk_management_profile_fp, ema_long=26, ema_short=12, signal=9):
        super().__init__(data_fp, risk_management_profile_fp, ticker, 'Moving Average CD')

        self.ema_long = ema_long
        self.ema_short = ema_short
        self.signal = signal

        self.macd_line: list = np.full(ema_long, np.nan).tolist() 
        self.signal_line: list = np.full(ema_long + signal, np.nan).tolist()

    def iterate(self, i):
        if i >= self.ema_long:
            ema_short = calculate_ema(self.data, self.ema_short, i)
            ema_long = calculate_ema(self.data, self.ema_long, i)

            self.macd_line.append(ema_long - ema_short)
            
        if i >= self.ema_long + self.signal:
            ema_signal = calculate_ema(self.macd_line, self.signal, i)
            self.signal_line.append(ema_signal)

    def get_indicator(self, i):
        if i >= self.ema_long + self.signal:
            if self.macd_line[i] > self.signal_line[i] and not self.position == 'bought':
                return 'bullish'
            elif self.position == 'bought' and (self.macd_line[i] > self.signal_line[i] or i == len(self.data) - 1):
                return 'bearish'
        else:
            return 'none' 

def calculate_ema(data, length, i):
    if length == 1:
        return data[i]
    
    a = 2 / (length + 1)
    return data[i] * a + calculate_ema(data, length - 1, i - 1) * (1 - a)