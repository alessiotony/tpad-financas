import pandas as pd
from numpy import log

df = (
    pd.read_csv('data/precos.csv')
    .sort_values('Date')
    .set_index('Date')
    )

# Calculo da taxa instantanea de retorno
df_t = log(df/df.shift(1))
df_t = df_t.dropna().reset_index()


print(df.head(3))
print(df_t.head(3))

print(df_t.info())