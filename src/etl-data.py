import pandas as pd
from glob import glob
from yfinance import download

# 1. 30 principais ações
file = glob(f'data/IBOVDia*.csv')[0]
print(file)

tickets =(
    pd.read_csv(file, sep=';', decimal=',',
                      names=['codigo', 'empresa', 'tipo',
                      'quantidade', 'peso'], index_col=False,
                      encoding='latin1', skiprows=2)
    .dropna(subset=['empresa'])
    .sort_values('peso', ascending=False)
    .head(30)
                      )
print(tickets)

# 2. Preços de fechamento dos tickets
ticket = "VALE3"

df = pd.DataFrame(None)
count = 0
for ticket in tickets.codigo:
    count += 1
    print(f"Baixando a ação {ticket}: {count}/{len(tickets)}")
    data = download(f'{ticket}.SA', period="2y")[['Adj Close']]
    data = data.rename(columns={'Adj Close': ticket}).reset_index()

    if len(df)==0:
        df = data
    else:
        df = pd.merge(df, data, on="Date")

# 3. Salvar os dados
print(f"Salvando os dados: {len(df)} datas")
df.to_csv("data/precos.csv.gz", index=False, compression='gzip')
df.to_csv("data/precos.csv", index=False)

