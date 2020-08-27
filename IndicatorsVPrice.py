from oandapyV20 import API
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.forexlabs as forexlabs
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.positions as positions
import oandapyV20.endpoints.pricing as pricing
import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.transactions as transactions
import pandas as pd
from ta.trend import MACD
import json
import pandas as pd
from pprint import pprint
import mpl_finance as fin
import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt
from ta.utils import IndicatorMixin, ema, get_min_max

from mpl_finance import candlestick_ohlc

token = 'bb6ecb991f7922670296435c80304304-0bdce73e35bd6245f6c3917a8d11384e'
api = API(access_token=token)

accountID = "101-001-14543692-001"

params = {"count": 50,
          "granularity": "M5"
          }

r = instruments.InstrumentsCandles(instrument="EUR_USD", params=params)
# show the endpoint as it is constructed for this call
# print("REQUEST:{}".format(r))
rv = api.request(r)
# print("RESPONSE:\n{}".format(json.dumps(rv, indent=2)))

da = pd.DataFrame(data=rv['candles'])
ohlc_data = da['mid'].apply(pd.Series)
ohlc = pd.concat([da.drop(['mid'], axis=1), ohlc_data], axis=1)
# changing columns in df to complete, volume, time, open, high, low, close

# print(ohlc)
# print(ohlc.columns)


ohlc['time'] = pd.to_datetime(ohlc['time'])
ohlc['time'] = ohlc['time'].apply(mpl_dates.date2num)
# change format of time

plt.style.use('ggplot')

ohlc = ohlc.astype(float)

fig, ax = plt.subplots()

fin.candlestick2_ochl(ax, opens=ohlc['o'], closes=ohlc['c'], highs=ohlc['h'], lows=ohlc['l'], width=.5, colorup='k',
                      colordown='r', alpha=0.75)

def ema_ind(df, n):
    ema_ = ema(df['c'], n)
    data = {"EMA_" + str(n): ema_}
    emadf = pd.DataFrame(data=data)
    return emadf

# n is average value of past end periods

EMA8 = ema_ind(ohlc,n=8)
ohlc = pd.concat([ohlc,EMA8], axis=1)
# axis = 1 pastes into column
# adds EMA to OHLC dataframe

plt.plot(ohlc["EMA_8"], color='g')
# plotted as the green line

EMA14 = ema_ind(ohlc,n=14)
ohlc = pd.concat([ohlc, EMA14], axis=1)

plt.plot(ohlc["EMA_14"], color='b')
# plotted as the blue line

EMA5 = ema_ind(ohlc, n=5)
ohlc = pd.concat([ohlc, EMA5], axis=1)

plt.plot(ohlc["EMA_5"], color="y")


# Setting labels & titles
ax.set_xlabel('Datapoint')
ax.set_ylabel('Price')
fig.suptitle('Daily Candlestick Chart of EUR/USD')

plt.show()