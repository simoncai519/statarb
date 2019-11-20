
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.api import adfuller
import statistics as sta
import pandas_datareader.data as pdr
import numpy as np
from math import log
import statsmodels.api as sm
from statsmodels.regression.linear_model import OLS
from statsmodels.tsa.tsatools import lagmat, add_trend
from statsmodels.tsa.adfvalues import mackinnonp



class StatisticalAnalysis:

    @classmethod
    def dosomething(self):
        pass

    pass


    def get_stock(symbol, start, end):
    df = pdr.DataReader(symbol, 'yahoo', start, end)
    df = df.sort_index(axis = 0)
    df = df['Adj Close']
    return df


    def half_life(ts):
        """
        Calculates the half life of a mean reversion
        """
        # make sure we are working with an array, convert if necessary
        ts = np.asarray(ts)

        # delta = p(t) - p(t-1)
        delta_ts = np.diff(ts)

        # calculate the vector of lagged values. lag = 1
        lag_ts = np.vstack([ts[1:], np.ones(len(ts[1:]))]).T

        # calculate the slope of the deltas vs the lagged values
        beta = np.linalg.lstsq(lag_ts, delta_ts)

        # compute and return half life
        return (np.log(2) / beta[0])[0]





start_date = '09/15/2019'
end_date = '11/15/2019'

vanguard = get_stock('SPY', start_date, end_date)
vti = get_stock('VTI', start_date, end_date)


fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(30,15))
axs[0].plot(vanguard)
axs[1].plot(vti)


np.corrcoef(vanguard, vti)



Y = [log(i) for i in vanguard]
X = [log(i) for i in vti]
model = sm.OLS(Y,X).fit()
slope=model.params[0]


st1=np.asarray(Y)-slope*np.asarray(X)


standardized_st1 = (st1 - np.mean(st1)) / np.std(st1)


plt.plot(standardized_st1)


# ADF Test
adf=adfuller(standardized_st1)


#Logic that states if our test statistic is less than
#a specific critical value, then the pair is cointegrated at that
#level, else the pair is not cointegrated
if adf[0] < adf[4]['1%']:
    print('Spread is Cointegrated at 1% Significance Level')
elif adf[0] < adf[4]['5%']:
    print('Spread is Cointegrated at 5% Significance Level')
elif adf[0] < adf[4]['10%']:
    print('Spread is Cointegrated at 10% Significance Level')
else:
    print('Spread is not Cointegrated')