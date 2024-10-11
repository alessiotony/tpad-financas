import pandas as pd
from numpy import log, log1p
from datetime import datetime, timedelta

df = (
    pd.read_csv('data/precos.csv', parse_dates=['Date'])
    # .sort_values('Date')
    # .set_index('Date')
    )
print(df.info())