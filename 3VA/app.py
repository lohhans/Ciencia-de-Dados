import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import glob
import plotly.express as px
import plotly.graph_objs as go
import locale
from datetime import time, timedelta

# Leitura dos CSV


def ler_CSV():
    lista = []

    csv_concatenados = glob.glob("*.csv")

    for csv in csv_concatenados:
        df = pd.read_csv(csv, sep=';')
        csv_df = df[df['codmun'].isnull()]
        lista.append(csv_df)

    dataframe = pd.concat(lista, axis=0, ignore_index=True)
    dataframe['data'] = pd.to_datetime(dataframe['data'])

    return dataframe


def obter_dados(df, date, dateStart, uf):
    lista = []
    data_formatada = df['data'] == date.strftime('%Y-%m-%d')
    df_auxiliar = df[data_formatada]

    lista.append(date)

    if uf == 76:
        lista.append('➤ BRASIL')
    else:
        lista.append(df['estado'].iloc[0])

    # Casos acumulados
    lista.append(int(df_auxiliar['casosAcumulado'].iloc[0]))
    # Média móvel de casos atual, Média móvel casos anterior, Situação, Porcentagem
    for estado_x in calcular_media_movel(df, date, dateStart, True):
        lista.append(estado_x)

    # Óbitos acumulados
    lista.append(df_auxiliar['obitosAcumulado'].iloc[0])
    # Média móvel de óbitos atual, Média móvel de óbitos anterior, Situação, Porcentagem
    for estado_y in calcular_media_movel(df, date, dateStart, False):
        lista.append(estado_y)

    return lista


def calcular_media_movel(dataframe, data, data_inicial, casos):
    lista = []

    # Obter média móvel do dia selecionado
    media_movel_dia_selecionado = obter_media(
        dataframe, data, data_inicial, casos)

    # Obter média móvel de antes
    media_movel_antes = obter_media(
        dataframe, data - timedelta(days=1), data_inicial, casos)

    lista.append(int(media_movel_dia_selecionado))
    lista.append(int(media_movel_antes))

    # Analisar situação e porcentagem
    if media_movel_antes == 0:
        if media_movel_dia_selecionado != 0:
            lista.append('Aumento')
            lista.append(100)
        else:
            lista.append('Estabilidade')
            lista.append('-')
    elif media_movel_dia_selecionado/media_movel_antes > 1:
        lista.append('Aumento')
        lista.append(
            round(((media_movel_dia_selecionado/media_movel_antes - 1)*100), 4))
    elif media_movel_dia_selecionado/media_movel_antes < 1:
        lista.append('Baixa')
        lista.append(
            round(abs(media_movel_dia_selecionado/media_movel_antes - 1)*100, 4))
    else:
        lista.append('Estabilidade')
        lista.append(
            round((media_movel_dia_selecionado/media_movel_antes - 1)*100, 4))

    return lista


def obter_media(df, data, data_inicial, casos):
    coluna_selecionada = ''
    if casos == True:
        coluna_selecionada = 'casosNovos'
    else:
        coluna_selecionada = 'obitosNovos'

    # Obter dados semanal
    if data.strftime('%Y-%m-%d') < (data_inicial + timedelta(days=7)).strftime('%Y-%m-%d'):
        data_formatada = (df['data'] <= data.strftime('%Y-%m-%d'))
        df_auxiliar = df[data_formatada]
        return df_auxiliar[coluna_selecionada].sum()/7
    else:
        data_formatada = (df['data'] <= data.strftime('%Y-%m-%d')) & (df['data']
                                                                      > (data - timedelta(days=7)).strftime('%Y-%m-%d'))
        df_auxiliar = df[data_formatada]
        return df_auxiliar[coluna_selecionada].mean()


def rodar_ST():
    locale.setlocale(locale.LC_ALL, 'en_US.utf8')

    dataframe_original = ler_CSV()

    data_inicial = dataframe_original['data'].iloc[0].date()
    data_final = dataframe_original['data'].iloc[-1].date()

    # Data - A data escolhida
    data_selecionada = st.date_input('Digite uma data no formato AAAA/MM/DD:',
                                     data_final, data_inicial, data_final)

    # Estado - O código do Estado
    lista_UF = [11, 12, 13, 14, 15, 16, 17, 21, 22, 23, 24, 25, 26,
                27, 28, 29, 31, 32, 33, 35, 41, 42, 43, 50, 51, 53, 76]

    # Dataframe final
    dataframe_analisado = pd.DataFrame(columns=['Data', 'Estado', 'Casos acumulados', 'Média móvel de casos atual', 'Média móvel casos anterior', 'Situação',
                                                'Percentual(%)', 'Óbitos acumulados', 'Média móvel de óbitos atual', 'Média móvel de óbitos anterior', 'Situação', 'Percentual(%)'])

    for UF in lista_UF:
        df_for = dataframe_original['coduf'] == UF
        df_selecionado = dataframe_original[df_for].iloc[:, lambda df: [
            1, 3, 7, 8, 9, 10, 11, 12, 13, 14, 15]]
        list_data = obter_dados(
            df_selecionado, data_selecionada, data_inicial, UF)
        dataframe_analisado.loc[len(dataframe_analisado)] = list_data

    # Índices correspondentes aos casos no dataframe_analisado
    dataframe_de_casos = dataframe_analisado.iloc[:, lambda df: [
        0, 1, 2, 3, 4, 5, 6]]

    # Índices correspondentes aos óbitos no dataframe_analisado
    dataframe_de_obitos = dataframe_analisado.iloc[:, lambda df: [
        0, 1, 7, 8, 9, 10, 11]]

    return dataframe_de_casos, dataframe_de_obitos, data_selecionada


############################################################################


# STREAMLIT CONFIG
st.set_page_config(page_title="Análise de casos do COVID-19 - 3ª VA de Ciência de Dados - Armstrong",
                   page_icon="📊", layout="wide")
st.set_option('deprecation.showPyplotGlobalUse', False)

st.title('Análise de casos do COVID-19 - Armstrong Lohãns')

st.text('\n\n\n\n')
st.markdown(
    'Bem vindo ao **dashboard de análise de casos do COVID-19 no Brasil!**\n\nEscolha uma **data abaixo** para gerar o relatório sobre um perído específico!')

hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Iniciar análise
with st.spinner('Analisando dados...'):
    dataframe_de_casos, dataframe_de_obitos, data_selecionada = rodar_ST()
st.success('Pronto! :)')

st.text('\n\n')

### CASOS ###
st.title('➥ CASOS DE COVID-19 NO BRASIL EM ' + str(data_selecionada.day)+"/" +
         str(data_selecionada.month)+"/"+str(data_selecionada.year))

# Tabela geral de casos
st.table(dataframe_de_casos)

# Casos acumulados de COVID-19 por Estado do Brasil em X:
df_ordenado = dataframe_de_casos.sort_values(
    by=['Casos acumulados'], ascending=True)
df = px.data.tips()
fig_p = px.bar(df, x=df_ordenado['Estado'][:-1],
               y=df_ordenado['Casos acumulados'][:-1],
               labels={"x": "Estado", "y": "Número de casos acumulados",
                       "hover_data_0": "Situação", "hover_data_1": "Percentual(%)", },
               hover_data=[df_ordenado["Situação"][:-1],
                           df_ordenado["Percentual(%)"][:-1]],
               orientation='v', width=1600, height=800,
               title='Casos acumulados de COVID-19 por Estado do Brasil em ' +
               str(data_selecionada.day)+"/"+str(data_selecionada.month)+"/"+str(data_selecionada.year),)
fig_p.update_traces(showlegend=False)
st.plotly_chart(fig_p)

# Média móvel de casos por Estado do Brasil em  X:
df_ordenado = dataframe_de_casos.sort_values(
    by=['Média móvel de casos atual'], ascending=True)
df = px.data.tips()
fig_p = px.bar(df, x=df_ordenado['Estado'][:-1],
               y=df_ordenado['Média móvel de casos atual'][:-1],
               labels={"x": "Estado", "y": "Média móvel de casos atual",
                       "hover_data_0": "Situação", "hover_data_1": "Percentual(%)", },
               hover_data=[df_ordenado["Situação"][:-1],
                           df_ordenado["Percentual(%)"][:-1]],
               orientation='v', width=1600, height=800,
               title='Média móvel de casos por Estado do Brasil em ' +
               str(data_selecionada.day)+"/"+str(data_selecionada.month)+"/"+str(data_selecionada.year),)
st.plotly_chart(fig_p)


### ÓBITOS ###
st.title('➥ ÓBITOS POR COVID-19 NO BRASIL EM ' + str(data_selecionada.day)+"/" +
         str(data_selecionada.month)+"/"+str(data_selecionada.year))

# Tabela geral de óbitos
st.table(dataframe_de_obitos)

# Óbitos acumulados por COVID-19 por Estado do Brasil em X:
df_ordenado = dataframe_de_obitos.sort_values(
    by=['Óbitos acumulados'], ascending=True)
df = px.data.tips()
fig_p = px.bar(df, x=df_ordenado['Estado'][:-1],
               y=df_ordenado['Óbitos acumulados'][:-1],
               labels={"x": "Estado", "y": "Óbitos acumulados",
                       "hover_data_0": "Situação", "hover_data_1": "Percentual(%)", },
               hover_data=[df_ordenado["Situação"][:-1],
                           df_ordenado["Percentual(%)"][:-1]],
               orientation='v', width=1600, height=800,
               title='Óbitos acumulados por COVID-19 por Estado do Brasil em ' +
               str(data_selecionada.day)+"/"+str(data_selecionada.month)+"/"+str(data_selecionada.year),)
st.plotly_chart(fig_p)

# Média móvel de óbitos por Estado do Brasil em X:
df_ordenado = dataframe_de_obitos.sort_values(
    by=['Média móvel de óbitos atual'], ascending=True)
df = px.data.tips()
fig_p = px.bar(df, x=df_ordenado['Estado'][:-1],
               y=df_ordenado['Média móvel de óbitos atual'][:-1],
               labels={"x": "Estado", "y": "Média móvel de óbitos atual",
                       "hover_data_0": "Situação", "hover_data_1": "Percentual(%)", },
               hover_data=[df_ordenado["Situação"][:-1],
                           df_ordenado["Percentual(%)"][:-1]],
               orientation='v', width=1600, height=800,
               title='Média móvel de óbitos por Estado do Brasil em ' +
               str(data_selecionada.day)+"/"+str(data_selecionada.month)+"/"+str(data_selecionada.year),)
st.plotly_chart(fig_p)

### GERAL SOBRE O BRASIL ###
st.title('NO DIA ' + str(data_selecionada.day)+"/" +
         str(data_selecionada.month)+"/"+str(data_selecionada.year) +
         ' O BRASIL ACUMULA UM TOTAL DE: ' +
         locale.format_string("%d", dataframe_de_casos.loc[dataframe_de_casos['Estado'] == '➤ BRASIL']['Casos acumulados'].values[0], grouping=True).replace(",", ".") +
         ' CASOS CONFIRMADOS DE COVID-19 E ' + locale.format_string("%d", dataframe_de_obitos.loc[dataframe_de_obitos['Estado'] == '➤ BRASIL']['Óbitos acumulados'].values[0], grouping=True).replace(",", ".") +
         ' ÓBITOS PELA DOENÇA')

# CASOS
if dataframe_de_casos.loc[dataframe_de_casos['Estado'] == '➤ BRASIL']['Situação'].values[0] == 'Baixa':
    st.write('➥ Com um média móvel de casos atual de: ' +
             locale.format_string("%d", dataframe_de_casos.loc[dataframe_de_casos['Estado'] == '➤ BRASIL']['Média móvel de casos atual'].values[0], grouping=True).replace(",", ".") +
             ' casos, estando assim em situação de ' +
             dataframe_de_casos.loc[dataframe_de_casos['Estado'] == '➤ BRASIL']['Situação'].values[0] +
             ' visto que a diferença na porcentagem de casos é de ' +
             '-' +
             locale.format_string("%.2f", dataframe_de_casos.loc[dataframe_de_casos['Estado']
                                                                 == '➤ BRASIL']['Percentual(%)'].values[0], grouping=True).replace(",", ".")
             + '%' + ' se comparado com a média móvel da semana anterior (' +
             locale.format_string("%d", dataframe_de_casos.loc[dataframe_de_casos['Estado'] == '➤ BRASIL']['Média móvel casos anterior'].values[0], grouping=True).replace(",", ".") + ');')
else:
    st.write('➥ Com um média móvel de casos atual de: ' +
             locale.format_string("%d", dataframe_de_casos.loc[dataframe_de_casos['Estado'] == '➤ BRASIL']['Média móvel de casos atual'].values[0], grouping=True).replace(",", ".") +
             ' casos, estando assim em situação de ' +
             dataframe_de_casos.loc[dataframe_de_casos['Estado'] == '➤ BRASIL']['Situação'].values[0] +
             ' visto que a diferença na porcentagem de casos é de ' +
             '+' +
             locale.format_string("%.2f", dataframe_de_casos.loc[dataframe_de_casos['Estado']
                                                                 == '➤ BRASIL']['Percentual(%)'].values[0], grouping=True).replace(",", ".")
             + '%' + ' se comparado com a média móvel da semana anterior (' +
             locale.format_string("%d", dataframe_de_casos.loc[dataframe_de_casos['Estado'] == '➤ BRASIL']['Média móvel casos anterior'].values[0], grouping=True).replace(",", ".") + ');')

# ÓBITOS
if dataframe_de_casos.loc[dataframe_de_casos['Estado'] == '➤ BRASIL']['Situação'].values[0] == 'Baixa':
    st.write('➥ E com uma média móvel de óbitos atual de: ' +
             locale.format_string("%d", dataframe_de_obitos.loc[dataframe_de_obitos['Estado'] == '➤ BRASIL']['Média móvel de óbitos atual'].values[0], grouping=True).replace(",", ".") +
             ' óbitos, estando assim em situação de ' +
             dataframe_de_obitos.loc[dataframe_de_obitos['Estado'] == '➤ BRASIL']['Situação'].values[0] +
             ' visto que a diferença na porcentagem de casos é de ' +
             '-' +
             locale.format_string("%.2f", dataframe_de_obitos.loc[dataframe_de_obitos['Estado']
                                                                  == '➤ BRASIL']['Percentual(%)'].values[0], grouping=True).replace(",", ".")
             + '%' + ' se comparado com a média móvel da semana anterior (' +
             locale.format_string("%d", dataframe_de_obitos.loc[dataframe_de_obitos['Estado'] == '➤ BRASIL']['Média móvel de óbitos anterior'].values[0], grouping=True).replace(",", ".") + ');')
else:
    st.write('➥ E com uma média móvel de óbitos atual de: ' +
             locale.format_string("%d", dataframe_de_obitos.loc[dataframe_de_obitos['Estado'] == '➤ BRASIL']['Média móvel de óbitos atual'].values[0], grouping=True).replace(",", ".") +
             ' óbitos, estando assim em situação de ' +
             dataframe_de_obitos.loc[dataframe_de_obitos['Estado'] == '➤ BRASIL']['Situação'].values[0] +
             ' visto que a diferença na porcentagem de casos é de ' +
             '+' +
             locale.format_string("%.2f", dataframe_de_obitos.loc[dataframe_de_obitos['Estado']
                                                                  == '➤ BRASIL']['Percentual(%)'].values[0], grouping=True).replace(",", ".")
             + '%' + ' se comparado com a média móvel da semana anterior (' +
             locale.format_string("%d", dataframe_de_obitos.loc[dataframe_de_obitos['Estado'] == '➤ BRASIL']['Média móvel de óbitos anterior'].values[0], grouping=True).replace(",", ".") + ');')
