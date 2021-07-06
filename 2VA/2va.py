import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st
import plotly.graph_objects as go


def gerar_dataset():
    dataset_original = pd.read_csv(
        "Vendas.csv", encoding='iso-8859-1', sep=";")  # dataset

    temp_anos = set()  # temporário
    datas = dataset_original["Data Venda"]  # datas brutas

    meses = {"Mes": []}
    anos = {"Ano": []}

    for k in range(len(datas)):
        d = int(datas[k][6::])
        meses["Mes"].append(int(datas[k][3:5]))
        anos["Ano"].append(int(datas[k][6::]))
        temp_anos.add(d)

    meses = pd.DataFrame(meses)  # meses obtidos
    anos = pd.DataFrame(anos)  # anos abotidos

    dataset_original.insert(
        0, "Mes", meses, allow_duplicates=False)  # meses tratados
    dataset_original.insert(
        0, "Ano", anos, allow_duplicates=False)  # anos tratados

    return dataset_original

# A - Faça um gráfico do total de vendas por ano


def total_vendas_por_ano(data):

    dic = {"Ano": [], "ValorVenda": []}
    anosSet = [2014, 2015, 2016, 2017, 2018, 2019]

    for i in anosSet:
        dat = data.loc[data["Ano"] == int(i)]
        dic["Ano"].append(i)
        valores = dat["ValorVenda"]
        valores = valores.values.tolist()
        for v in range(len(valores)):
            valores[v] = float(valores[v].replace(",", "."))
        soma = sum(valores)
        dic["ValorVenda"].append(soma)

    dataset = pd.DataFrame(dic)

    st.write(dataset)

    sns.catplot(x="Ano", y="ValorVenda", kind="bar", data=dataset, estimator=np.sum).set(
        title="Gráfico do total de vendas por ano").fig.set_figwidth(16)
    st.pyplot()

    layout = go.Layout(title="A - Gráfico do total de vendas por ano", barmode="group",
                       xaxis=dict(title="Ano"), yaxis=dict(title="Valor total de vendas"))

    fig = go.Figure(data=go.Bar(
        x=dataset["Ano"], y=dataset["ValorVenda"]), layout=layout)
    fig

# B - Faça um gráfico do total de vendas por categoria


def total_vendas_por_categoria(data):

    dic = {"Ano": data["Ano"], "ValorVenda": [],
           "Categoria": data["Categoria"]}

    valores = data["ValorVenda"].values.tolist()

    for v in range(len(valores)):
        valores[v] = float(valores[v].replace(",", "."))

    dic["ValorVenda"] = valores
    dataset = pd.DataFrame(dic)

    sns.catplot(x="Categoria", y="ValorVenda", kind="bar", data=dataset, estimator=np.sum).set(
        title="Total de vendas por categoria").fig.set_figwidth(16)
    st.pyplot()

    layout = go.Layout(title="B - Gráfico do total de vendas por categoria", barmode="group",
                       xaxis=dict(title="Categoria"), yaxis=dict(title="Valor total de vendas"))

    fig = go.Figure(data=go.Bar(
        x=dataset["Categoria"], y=dataset["ValorVenda"]), layout=layout)
    fig

# C - Faça um gráfico do total de vendas por categoria por ano


def total_vendas_por_categoria_por_ano(data):

    dic = {"Ano": data["Ano"], "ValorVenda": [],
           "Categoria": data["Categoria"]}

    valores = data["ValorVenda"]
    valores = valores.values.tolist()
    for v in range(len(valores)):
        valores[v] = float(valores[v].replace(",", "."))

    dic["ValorVenda"] = valores
    dataset = pd.DataFrame(dic)

    sns.catplot(x="Categoria", y="ValorVenda", kind="bar", hue="Ano", data=dataset, estimator=np.sum).set(
        title="Total de vendas por categoria por ano").fig.set_figwidth(16)
    st.pyplot()
# D - Faça um gráfico do total de vendas por ano e categoria


def total_vendas_por_ano_e_categoria(data):

    dic = {"Ano": data["Ano"], "ValorVenda": [],
           "Categoria": data["Categoria"]}

    valores = data["ValorVenda"]
    valores = valores.values.tolist()
    for v in range(len(valores)):
        valores[v] = float(valores[v].replace(",", "."))

    dic["ValorVenda"] = valores
    dataset = pd.DataFrame(dic)

    sns.catplot(x="Ano", y="ValorVenda", kind="bar", hue="Categoria", data=dataset, estimator=np.sum).set(
        title="Total de vendas por categoria por ano").fig.set_figwidth(16)
    st.pyplot()
# E - Faça um gráfico do total de vendas por categoria pelos meses para cada ano


def total_vendas_por_categoria_pelos_meses_para_cada_ano(data):

    dic = {"Ano": data["Ano"], "ValorVenda": [],
           "Categoria": data["Categoria"], "Mes": data["Mes"]}
    anosSet = [2014, 2015, 2016, 2017, 2018, 2019]

    valores = data["ValorVenda"]
    valores = valores.values.tolist()
    for v in range(len(valores)):
        valores[v] = float(valores[v].replace(",", "."))

    dic["ValorVenda"] = valores
    dataset = pd.DataFrame(dic)

    for ano in anosSet:
        dataset_for = dataset.loc[dataset["Ano"] == ano]
        sns.catplot(x="Mes", y="ValorVenda", kind="bar", hue="Categoria", data=dataset_for, estimator=np.sum).set(
            title="Total de vendas por categoria pelos meses para o ano de "+str(ano)).fig.set_figwidth(16)
    st.pyplot()
# F - Faça um gráfico dos produto mais vendido por cada fabricante


def produto_mais_vendido_por_cada_fabricante(data):

    dic = {"Ano": data["Ano"], "ValorVenda": [], "Categoria": data["Categoria"], "Mes": data["Mes"],
           "Produto": data["Produto"], "Fabricante": data["Fabricante"], "Loja": data["Loja"]}

    valores = data["ValorVenda"].values.tolist()
    for v in range(len(valores)):
        valores[v] = float(valores[v].replace(",", "."))

    dic["ValorVenda"] = valores
    dataset = pd.DataFrame(dic)
    fabricantes = ["Motorola", "Samsung", "LG", "Sony", "Consul", "Brastemp",
                   "Panasonic", "Electrolux", "HP", "Dell", "Epson", "Britânia", "Arno", "Philco"]

    for fabricante in fabricantes:
        dataset_for = dataset.loc[dataset["Fabricante"] == fabricante]
        sns.catplot(x="Fabricante", y="ValorVenda", kind="bar", hue="Produto", data=dataset_for, estimator=np.sum).set(
            title="Produto mais vendido para o fabricante "+str(fabricante)).fig.set_figwidth(8)
    st.pyplot()
# G - Faça um gráfico das vendas das lojas por categoria


def vendas_das_lojas_por_categoria(data):

    dic = {"Ano": data["Ano"], "ValorVenda": [], "Categoria": data["Categoria"], "Mes": data["Mes"],
           "Produto": data["Produto"], "Fabricante": data["Fabricante"], "Loja": data["Loja"]}
    lojas = ["R1296", "BA7783", "JP8825",
             "RG7742", "AL1312", "GA7751", "JB6325"]

    valores = data["ValorVenda"].values.tolist()

    for v in range(len(valores)):
        valores[v] = float(valores[v].replace(",", "."))

    dic["ValorVenda"] = valores
    dataset = pd.DataFrame(dic)

    sns.catplot(x="Loja", y="ValorVenda", kind="bar", hue="Categoria", data=dataset, estimator=np.sum).set(
        title="Vendas das lojas por categoria (geral)").fig.set_figwidth(16)

    for loja in lojas:
        dataset_for = dataset.loc[dataset["Loja"] == loja]
        sns.catplot(x="Categoria", y="ValorVenda", kind="bar", hue="Categoria", data=dataset_for, estimator=np.sum).set(
            title="Vendas das lojas por categoria para a loja "+str(loja)).fig.set_figwidth(8)
    st.pyplot()
# H - Faça um Ranking dos produtos com maiores vendas no geral e por loja


def ranking_dos_produtos_com_maiores_venda_geral(data):
    dataFrame = data
    sns.catplot(x="Valor Vendas", y="Produto", kind="bar", data=dataFrame, estimator=np.sum, palette="tab10").set(
        title="Ranking dos produtos com maiores vendas no geral").fig.set_figwidth(8)
    st.pyplot()


def ranking_dos_produtos_com_maiores_venda_por_loja(data, produtos):
    dataFrame = data
    produtos_set = produtos
    lojas = ["R1296", "BA7783", "JP8825",
             "RG7742", "AL1312", "GA7751", "JB6325"]
    for loja in lojas:
        dataset_for_loja = dataset.loc[dataset["Loja"] == loja]

        valor_das_vendas = []
        for produto in produtos_set:
            dataset_for_produto = dataset_for_loja.loc[dataset_for_loja["Produto"] == produto]
            lista = dataset_for_produto["ValorVenda"].values.tolist()

            soma = 0
            for k in lista:
                soma += float(k.replace(",", "."))

            valor_das_vendas.append(soma)

        dataFrame = pd.DataFrame(
            {"Produto": list(produtos), "Valor Vendas": valor_das_vendas})
        dataFrame = dataFrame.sort_values(
            ['Valor Vendas', 'Produto'], ascending=False)

        sns.catplot(x="Valor Vendas", y="Produto", kind="bar", data=dataFrame, estimator=np.sum, palette="tab10").set(
            title="Ranking dos produtos com maiores vendas para a loja "+str(loja)).fig.set_figwidth(8)
        st.pyplot()


def ranking_dos_produtos_com_maiores_venda_geral_e_por_loja(data):

    dic = {"Produto": data["Produto"], "Ano": data["Ano"], "ValorVenda": [
    ], "Fabricante": data["Fabricante"], "Loja": data["Loja"]}
    valores = data["ValorVenda"].values.tolist()

    for v in range(len(valores)):
        valores[v] = float(valores[v].replace(",", "."))

    dic["ValorVenda"] = valores

    dataset = pd.DataFrame(dic)

    produtos_set = set()

    for p in range(len(dataset["Produto"])):
        produto = dic["Produto"][p]
        produtos_set.add(produto)

    valor_das_vendas = []
    for produto in produtos_set:
        dataset_for_produto_geral = dataset.loc[dataset["Produto"] == produto]
        lista = dataset_for_produto_geral["ValorVenda"].values.tolist()
        soma = sum(lista)
        valor_das_vendas.append(soma)

    dataFrame = pd.DataFrame(
        {"Produto": list(produtos_set), "Valor Vendas": valor_das_vendas})
    dataFrame = dataFrame.sort_values(
        ['Valor Vendas', 'Produto'], ascending=False)

    ranking_dos_produtos_com_maiores_venda_geral(dataFrame)
    ranking_dos_produtos_com_maiores_venda_por_loja(dataFrame, produtos_set)

# I - Faça um Ranking dos produtos com menores vendas no geral e por loja


def ranking_dos_produtos_com_menores_venda_geral(data):
    dataFrame = data
    sns.catplot(x="Valor Vendas", y="Produto", kind="bar", data=dataFrame, estimator=np.sum, palette="tab10").set(
        title="Ranking dos produtos com menores vendas no geral").fig.set_figwidth(8)
    st.pyplot()


def ranking_dos_produtos_com_menores_venda_por_loja(data, produtos):
    dataFrame = data
    produtos_set = produtos
    lojas = ["R1296", "BA7783", "JP8825",
             "RG7742", "AL1312", "GA7751", "JB6325"]
    for loja in lojas:
        dataset_for_loja = dataset.loc[dataset["Loja"] == loja]

        valor_das_vendas = []
        for produto in produtos_set:
            dataset_for_produto = dataset_for_loja.loc[dataset_for_loja["Produto"] == produto]
            lista = dataset_for_produto["ValorVenda"].values.tolist()

            soma = 0
            for k in lista:
                soma += float(k.replace(",", "."))

            valor_das_vendas.append(soma)

        dataFrame = pd.DataFrame(
            {"Produto": list(produtos), "Valor Vendas": valor_das_vendas})
        dataFrame = dataFrame.sort_values(
            ['Valor Vendas', 'Produto'], ascending=True)

        sns.catplot(x="Valor Vendas", y="Produto", kind="bar", data=dataFrame, estimator=np.sum, palette="tab10").set(
            title="Ranking dos produtos com menores vendas para a loja "+str(loja)).fig.set_figwidth(8)
        st.pyplot()


def ranking_dos_produtos_com_menores_venda_geral_e_por_loja(data):

    dic = {"Produto": data["Produto"], "Ano": data["Ano"], "ValorVenda": [
    ], "Fabricante": data["Fabricante"], "Loja": data["Loja"]}
    valores = data["ValorVenda"].values.tolist()

    for v in range(len(valores)):
        valores[v] = float(valores[v].replace(",", "."))

    dic["ValorVenda"] = valores

    dataset = pd.DataFrame(dic)

    produtos_set = set()

    for p in range(len(dataset["Produto"])):
        produto = dic["Produto"][p]
        produtos_set.add(produto)

    valor_das_vendas = []
    for produto in produtos_set:
        datP = dataset.loc[dataset["Produto"] == produto]
        lista = datP["ValorVenda"].values.tolist()
        soma = sum(lista)
        valor_das_vendas.append(soma)

    dataFrame = pd.DataFrame(
        {"Produto": list(produtos_set), "Valor Vendas": valor_das_vendas})
    dataFrame = dataFrame.sort_values(
        ['Valor Vendas', 'Produto'], ascending=True)

    ranking_dos_produtos_com_menores_venda_geral(dataFrame)
    ranking_dos_produtos_com_menores_venda_por_loja(dataFrame, produtos_set)

# J - Faça um ranking dos produtos mais rentáveis no geral e por loja


def ranking_dos_produtos_mais_rentaveis_no_geral(data):
    dataset_ranking = data
    sns.catplot(x="Rentabilidade", y="Produto", kind="bar", data=dataset_ranking, estimator=np.sum,
                palette="tab10").set(title="Ranking dos produtos mais rentáveis no geral").fig.set_figwidth(8)
    st.pyplot()


def ranking_dos_produtos_mais_rentaveis_por_loja(data, lojas, produtos):
    dataset = data

    for loja in lojas:
        datP = dataset.loc[dataset["Loja"] == loja]

        rentabilidade = {"Produto": [], "Rentabilidade": []}
        for prod in produtos:
            df = datP.loc[datP["Produto"] == prod]
            soma = df["Rentabilidade"].sum()
            rentabilidade["Produto"].append(prod)
            rentabilidade["Rentabilidade"].append(soma)

        rentabilidade = pd.DataFrame(rentabilidade).sort_values(
            ['Rentabilidade', 'Produto'], ascending=False)

        sns.catplot(x="Rentabilidade", y="Produto", kind="bar", data=rentabilidade, estimator=np.sum, palette="tab10").set(
            title="Ranking dos produtos mais rentáveis para a loja "+str(loja)).fig.set_figwidth(8)
        st.pyplot()


def ranking_dos_produtos_mais_rentaveis_no_geral_e_por_loja(data):

    dic = {"Produto": data["Produto"], "Ano": data["Ano"], "ValorVenda": [
    ], "Fabricante": data["Fabricante"], "Loja": data["Loja"], "Custo": [], "Rentabilidade": []}
    lojas = ["R1296", "BA7783", "JP8825",
             "RG7742", "AL1312", "GA7751", "JB6325"]

    valores = data["ValorVenda"].values.tolist()
    custos = data["preço Custo"].values.tolist()

    for a in range(len(valores)):
        valores[a] = float(valores[a].replace(",", "."))
        custos[a] = float(custos[a].replace(",", "."))
        dic["Rentabilidade"].append(valores[a]-custos[a])

    dic["ValorVenda"] = valores
    dic["Custo"] = custos

    dataset = pd.DataFrame(dic)

    valVendas = []

    produtos_set = set()
    produtos = data["Produto"].values.tolist()

    for k in range(len(produtos)):
        produtos_set.add(produtos[k])

    rentabilidade = {"Produto": [], "Rentabilidade": []}
    for prod in produtos_set:
        df = dataset.loc[dataset["Produto"] == prod]
        soma = df["Rentabilidade"].sum()
        rentabilidade["Produto"].append(prod)
        rentabilidade["Rentabilidade"].append(soma)

    rentabilidade = pd.DataFrame(rentabilidade).sort_values(
        ['Rentabilidade', 'Produto'], ascending=False)

    ranking_dos_produtos_mais_rentaveis_no_geral(rentabilidade)
    ranking_dos_produtos_mais_rentaveis_por_loja(dataset, lojas, produtos_set)

# K - Faça um Ranking de vendas por lojas


def ranking_de_vendas_por_lojas(data):
    dic = {"Produto": data["Produto"], "Ano": data["Ano"], "ValorVenda": [
    ], "Fabricante": data["Fabricante"], "Loja": data["Loja"]}

    valores = data["ValorVenda"]
    valores = valores.values.tolist()
    for v in range(len(valores)):
        valores[v] = float(valores[v].replace(",", "."))

    dic["ValorVenda"] = valores
    dats = pd.DataFrame(dic)
    #dats = dats.sort_values(['ValorVenda','Produto'], ascending=False)
    valVendas = []
    loj = ["R1296", "BA7783", "JP8825", "RG7742", "AL1312", "GA7751", "JB6325"]

    for loja in loj:
        datP = dats.loc[dats["Loja"] == loja]
        lista = datP["ValorVenda"].values.tolist()
        soma = sum(lista)
        valVendas.append(soma)

    dataFrame = pd.DataFrame({"Loja": loj, "Valor Vendas": valVendas})
    dataFrame = dataFrame.sort_values(['Valor Vendas'], ascending=False)

    sns.catplot(x="Loja", y="Valor Vendas", kind="bar", data=dataFrame, estimator=np.sum).set(
        title="Ranking de vendas por lojas").fig.set_figwidth(8)
    st.pyplot()
# L - Faça um ranking dos vendedores com maior valor de vendas por loja e ano
# Não consegui :(


############################################################################


# STREAMLIT CONFIG
st.set_option('deprecation.showPyplotGlobalUse', False)
dataset = gerar_dataset()

# print(dataset)


st.title('Análise das vendas')
st.sidebar.header('Escolha a opção do relatório')


# A - Faça um gráfico do total de vendas por ano
if st.sidebar.button("Gráfico do total de vendas por ano"):
    total_vendas_por_ano(dataset)

# B - Faça um gráfico do total de vendas por categoria
if st.sidebar.button("Gráfico do total de vendas por categoria"):
    total_vendas_por_categoria(dataset)

# C - Faça um gráfico do total de vendas por categoria por ano
if st.sidebar.button("Gráfico do total de vendas por categoria por ano"):
    total_vendas_por_categoria_por_ano(dataset)

# D - Faça um gráfico do total de vendas por ano e categoria
if st.sidebar.button("Gráfico do total de vendas por ano e categoria"):
    total_vendas_por_ano_e_categoria(dataset)

# E - Faça um gráfico do total de vendas por categoria pelos meses para cada ano
if st.sidebar.button("Gráfico do total de vendas por categoria pelos meses para cada ano"):
    total_vendas_por_categoria_pelos_meses_para_cada_ano(dataset)

# F - Faça um gráfico dos produto mais vendido por cada fabricante
if st.sidebar.button("Gráfico dos produto mais vendido por cada fabricante"):
    produto_mais_vendido_por_cada_fabricante(dataset)

# G - Faça um gráfico das vendas das lojas por categoria
if st.sidebar.button("Gráfico das vendas das lojas por categoria"):
    vendas_das_lojas_por_categoria(dataset)

# H - Faça um Ranking dos produtos com maiores vendas no geral e por loja
if st.sidebar.button("Ranking dos produtos com maiores vendas no geral e por loja"):
    ranking_dos_produtos_com_maiores_venda_geral_e_por_loja(dataset)

# I - Faça um Ranking dos produtos com menores vendas no geral e por loja
if st.sidebar.button("Ranking dos produtos com menores vendas no geral e por loja"):
    ranking_dos_produtos_com_menores_venda_geral_e_por_loja(dataset)

# J - Faça um ranking dos produtos mais rentáveis no geral e por loja
if st.sidebar.button("Ranking dos produtos mais rentáveis no geral e por loja"):
    ranking_dos_produtos_mais_rentaveis_no_geral_e_por_loja(dataset)

# K - Faça um Ranking de vendas por lojas
if st.sidebar.button("Ranking de vendas por lojas"):
    ranking_de_vendas_por_lojas(dataset)

# L - Faça um ranking dos vendedores com maior valor de vendas por loja e ano
# if st.sidebar.button("Ranking dos vendedores com maior valor de vendas por loja e ano"):
    # Não consegui :(
