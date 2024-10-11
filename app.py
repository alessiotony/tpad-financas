
# Terminal: streamlit run app.py

import streamlit as st
import pandas as pd
import numpy as np

# Leitura dos dados
d = pd.read_excel('data/tbl_acoes.xlsx', parse_dates=[0])
# Designer do Application

# Customizar a aba da janela do APP
st.set_page_config(page_icon='🚀', page_title='CDN - UFPB')

# Cabeçalho do App
a,b = st.columns([1,10])

with a:
    st.image('img/logo-cdn.png')
with b:
    st.title('Weekend Effect na B3 🇧🇷')
    
# Introdução
st.markdown(
    """
    Este APP visa identificar o efeito do fim de semana
    no mercado financeiro brasileiro, usando dados das 
    30 principais ações que compõem o índice Bovespa.
    """)

with st.expander('Você conhece o Weekend Effect?', False):
    st.markdown(
    """
    O efeito fim de semana é um velho conhecido do mercado 
    financeiro. Frank Cross (1973) observou que o retorno das 
    ações na segunda feira era inferior aos demais dias da 
    semana, especialmente quando comparado com sexta-feira.
    """)

# Segmentador de dados
lista_acoes = d.código.unique()
lista_empresas = d.ação.unique()

#Example controlers
with st.sidebar:
    st.subheader("MENU")
    acoes = st.multiselect('Selecione as ações', lista_acoes, lista_acoes)
# st.selectbox('Selecione empresas', lista_empresas, lista_empresas)
# st.select_slider('Selecione uma faixa de retorno', np.arange(0,100), 50)

print(d.head(3))


# Controle de erro
if len(acoes)==0:
    st.markdown('`Por favor, selecione uma ação!!!`')
    st.stop()

# Filtro reativo
d = d.query('código.isin(@acoes)')

# Métrica
r = np.abs(d.ret_segunda.sum())/np.abs(d.ret_sexta.sum())
st.metric('Weekend Effect 🏄🏼', np.round(r,2))

# Barra
r = d.groupby('fim_semana').agg(retorno=('retorno', 'sum'))
st.bar_chart(r)

# Área
r = d.groupby('data').agg(segunda=('ret_segunda', 'sum'),
                          sexta=('ret_sexta', 'sum'))
st.area_chart(r)


st.table(d)