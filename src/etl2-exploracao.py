import pandas as pd
from numpy import log, log1p
from datetime import datetime, timedelta

df = (
    pd.read_csv('data/precos.csv', parse_dates=['Date'])
    .sort_values('Date')
    .set_index('Date')
    )

# Calculo da taxa instantanea de retorno
# df = log(df/df.shift(1))
df = log1p(df.pct_change())
df = df.dropna()

print(df.head(3))


now = datetime.now().date()

tab = dict()
for j in [1, 3, 12, 24]:

    limiar = (now - timedelta(days=30*j))
    r = df.query('index > @limiar').describe().T[['mean', 'std']]
    
    tab.update({j: r})

# Exemplo do retorno em 24 meses
r = tab[3]
r.columns = ['retorno', 'risco']

r['ind'] = r.retorno/r.risco
r.sort_values('ind', ascending=False).query('ind>0')
print(r)


# Correlação 
print(df.corr())