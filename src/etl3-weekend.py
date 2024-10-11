from glob import glob
from numpy import log1p, select
from pandas import read_csv, DataFrame, to_datetime
import holidays
from datetime import datetime, timedelta
feriados = [i for i in holidays.Brazil()['2020-01-01': '2024-10-11']]
print(feriados)


d = (
    read_csv('data/precos.csv', parse_dates=['Date'])
    .set_index('Date')
)
    
d = log1p(d.pct_change())
d = d.dropna().reset_index()

# Vespera do feriado
feriados = DataFrame(dict(data=feriados)).assign(
    data=lambda x: to_datetime(x.data)-timedelta(1), vespera=1)

# Dados IBOV
file = glob(f'data/IBOVDia*.csv')[0]
ibov = (
    read_csv(file, sep=';', encoding='ISO-8859-1', decimal=',', skiprows=1, index_col=False)
    .dropna(subset=['Tipo'])
    .sort_values('Part. (%)', ascending=False)
    .head(30)
    .reset_index(drop=True)
    .filter(items=['Código', 'Ação', 'Tipo'])
)


# Data Mart Painel
d1 = (
    d.melt(id_vars=['Date'], value_vars=d.columns, var_name='Código', value_name='Retorno')
    .merge(ibov)
    .rename(columns={'Date':'data'})
    .rename(columns=lambda x: x.lower())
    .merge(feriados, how='left')
    .fillna(value={'vespera':0})
    .assign(
        dia=lambda x: x.data.dt.weekday.map({0:'SEG', 1:'TER', 2:'QUA', 3:'QUI', 4:'SEX', 5:'SAB', 6:'DOM'}),
        trimestre = lambda x: x.data.dt.quarter,
        mes = lambda x: x.data.dt.month,
        fim_semana = lambda x: select([x.dia=='SEX', x.dia=='SEG'], ['Sexta', 'Segunda'], default='Outro'))
)

print(d1.head(3))

# Exportando data mart para Visualização
d1.to_excel('data/tbl_acoes.xlsx', index=False, sheet_name = 'data')