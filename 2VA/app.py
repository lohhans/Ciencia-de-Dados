import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import pyplot
import numpy as np

#ok
@st.cache
def load_data():

    dataset = pd.read_csv("Vendas.csv",encoding = 'iso-8859-1', sep=";")

    anosSet = set()
    datas = dataset["Data Venda"]
    anos = {"ano":[]}
    meses = {"Mes":[]}

    for k in range(len(datas)):
        d = int(datas[k][6::])
        anos["ano"].append(int(datas[k][6::]))
        meses["Mes"].append(int(datas[k][3:5]))
        anosSet.add(d)

    anosDic = anos
    anos = pd.DataFrame(anos)
    meses = pd.DataFrame(meses)

    dataset.insert(0, "Ano", anos, allow_duplicates=False)
    dataset.insert(0, "Mes", meses, allow_duplicates=False)

    return dataset

#ok
def valorVendasAno(data):

    datRank = data
    dic = {"Ano":[],"ValorVenda":[]}
    anosSet = [2014,2015,2016,2017,2018,2019]
    for i in anosSet:
        dat = datRank.loc[datRank["Ano"] == int(i)]
        dic["Ano"].append(i)
        valores = dat["ValorVenda"]
        valores = valores.values.tolist()
        for v in range(len(valores)):
            valores[v] = float(valores[v].replace(",", "."))

        soma = sum(valores)
        dic["ValorVenda"].append(soma)

    dic = pd.DataFrame(dic)

    dats = dic
    fig, ax = plt.subplots()
    sns.barplot(data = dats, x="Ano", y="ValorVenda", palette="Set1")
    #dic.hist(column="Ano",bins = 11)
    plt.title("Vendas por Ano (Em Reais)")

    st.pyplot()
    return dic

#ok
def valorVendasCategoria(data):

    dic = {"Ano":data["Ano"],"ValorVenda":[],"Categoria":data["Categoria"]}

    valores = data["ValorVenda"]
    valores = valores.values.tolist()
    for v in range(len(valores)):
        valores[v] = float(valores[v].replace(",", "."))

    dic["ValorVenda"] = valores
    dats = pd.DataFrame(dic)

    sns.barplot(data = dats, x="Categoria", y="ValorVenda", estimator = np.sum, palette="Set2")
    plt.title("Vendas por Categoria (Em Reais)")

    st.pyplot()

#ok
def valorVendasCategoriaAno(data):
        dic = {"Ano":data["Ano"],"ValorVenda":[],"Categoria":data["Categoria"]}

        valores = data["ValorVenda"]
        valores = valores.values.tolist()
        for v in range(len(valores)):
            valores[v] = float(valores[v].replace(",", "."))

        dic["ValorVenda"] = valores
        dats = pd.DataFrame(dic)

        sns.barplot(data = dats, x="Categoria", y="ValorVenda", hue = "Ano", estimator = np.sum, palette="Set2")
        plt.title("Vendas por Categoria por Ano (Em Reais)")

        st.pyplot()

#ok
def valorVendasAnoCategoria(data):
    dic = {"Ano":data["Ano"],"ValorVenda":[],"Categoria":data["Categoria"]}

    valores = data["ValorVenda"]
    valores = valores.values.tolist()
    for v in range(len(valores)):
        valores[v] = float(valores[v].replace(",", "."))

    dic["ValorVenda"] = valores
    dats = pd.DataFrame(dic)

    sns.barplot(data = dats, x="Ano", y="ValorVenda", hue = "Categoria", estimator = np.sum, palette="Set2")
    plt.title("Vendas por Ano por Categoria (Em Reais)")

    st.pyplot()

#ok
def valorVendasMes(data):

    dic = {"Ano":data["Ano"],"ValorVenda":[],"Categoria":data["Categoria"],"Mes":data["Mes"]}

    valores = data["ValorVenda"]
    valores = valores.values.tolist()
    for v in range(len(valores)):
        valores[v] = float(valores[v].replace(",", "."))

    dic["ValorVenda"] = valores
    dats = pd.DataFrame(dic)
    anosSet = [2014,2015,2016,2017,2018,2019]

    for ano in anosSet:
        datsA = dats.loc[dats["Ano"] == ano]
        sns.barplot(data = datsA, x="Mes", y="ValorVenda", hue = "Categoria", estimator = np.sum, palette="bright")
        plt.title("Vendas por Categoria por Mes de cada Ano (Em Reais) -> "+str(ano))

        st.pyplot()

#ok
def valorVendasProdutoFabricante(data):
    st.write("Vendas de Produtos por Fabricante (Em Reais) ")
    dic = {"Ano":data["Ano"],"ValorVenda":[],"Categoria":data["Categoria"],"Mes":data["Mes"],"Produto":data["Produto"],"Fabricante":data["Fabricante"],"Loja":data["Loja"]}

    valores = data["ValorVenda"]
    valores = valores.values.tolist()
    for v in range(len(valores)):
        valores[v] = float(valores[v].replace(",", "."))

    dic["ValorVenda"] = valores
    dats = pd.DataFrame(dic)
    fabris = ["Motorola", "Samsung", "LG", "Sony", "Consul", "Brastemp", "Panasonic", "Electrolux", "HP", "Dell", "Epson", "Britânia", "Arno", "Philco"]
    a4_dims = (35, 15)

    fig, ax = pyplot.subplots(figsize=a4_dims)
    sns.barplot(data = dats, x="Fabricante", y="ValorVenda", hue = "Produto", estimator = np.sum, palette="tab20", ax = ax)
    plt.title("Vendas de Produtos por Fabricante (Em Reais)")

    st.pyplot()

    for fabricante in fabris:
        datF = dats.loc[dats["Fabricante"] == fabricante]
        st.write("Vendas de Produtos por Fabricante (Em Reais) "+str(fabricante))
        a4_dims = (12, 9)
        fig, ax = pyplot.subplots(figsize=a4_dims)
        sns.barplot(data = datF, x="Fabricante", y="ValorVenda", hue = "Produto", estimator = np.sum, palette="tab20", ax = ax)
        plt.title("Vendas de Produtos por Fabricante (Em Reais) "+str(fabricante))
        st.pyplot()

#ok
def valorVendasLojaCategoria(data):
    st.write("Vendas das lojas por categoria (Em Reais)")
    dic = {"Ano":data["Ano"],"ValorVenda":[],"Categoria":data["Categoria"],"Mes":data["Mes"],"Produto":data["Produto"],"Fabricante":data["Fabricante"],"Loja":data["Loja"]}

    valores = data["ValorVenda"]
    valores = valores.values.tolist()
    for v in range(len(valores)):
        valores[v] = float(valores[v].replace(",", "."))

    dic["ValorVenda"] = valores
    dats = pd.DataFrame(dic)
    #fabris = ["Motorola", "Samsung", "LG", "Sony", "Consul", "Brastemp", "Panasonic", "Electrolux", "HP", "Dell", "Epson", "Britânia", "Arno", "Philco"]
    #a4_dims = (10,7)
    loj = ["R1296", "BA7783", "JP8825", "RG7742", "AL1312", "GA7751", "JB6325"]
    #fig, ax = pyplot.subplots(figsize=a4_dims)
    sns.barplot(data = dats, x="Loja", y="ValorVenda", hue = "Categoria", estimator = np.sum, palette="tab10")
    plt.title("Vendas das lojas por categoria (Em Reais)")

    st.pyplot()

    for loja in loj:
        datL = dats.loc[dats["Loja"] == loja]
        sns.barplot(data = datL, x="Categoria", y="ValorVenda", estimator = np.sum, palette="tab10")
        plt.title("Vendas das lojas por categoria (Em Reais) -> Loja:"+str(loja))
        st.pyplot()

####################### Rankings #############################
#ok
def rankingProdutos(data):
    st.write("Ranking Produtos Geral")
    dic = {"Produto":data["Produto"], "Ano":data["Ano"],"ValorVenda":[],"Fabricante":data["Fabricante"],"Loja":data["Loja"]}

    valores = data["ValorVenda"]
    valores = valores.values.tolist()
    for v in range(len(valores)):
        valores[v] = float(valores[v].replace(",", "."))

    dic["ValorVenda"] = valores
    dats = pd.DataFrame(dic)
    #dats = dats.sort_values(['ValorVenda','Produto'], ascending=False)
    produtos = set()
    for p in range(len(dats["Produto"])):
        prod = dic["Produto"][p]
        produtos.add(prod)

    valVendas = []
    for prod in produtos:
        datP = dats.loc[dats["Produto"] == prod]
        lista = datP["ValorVenda"].values.tolist()
        soma = sum(lista)
        valVendas.append(soma)

    dataFrame = pd.DataFrame({"Produto":list(produtos),"Valor Vendas":valVendas})
    dataFrame = dataFrame.sort_values(['Valor Vendas','Produto'], ascending=False)

    st.write("Ranking Geral (Maior para o Menor)")
    sns.barplot(data = dataFrame, x="Valor Vendas", y="Produto", estimator = np.sum, palette="tab10")
    st.pyplot()
    st.write(dataFrame)

    loj = ["R1296", "BA7783", "JP8825", "RG7742", "AL1312", "GA7751", "JB6325"]
    for loja in loj:
        datL = dats.loc[dats["Loja"] == loja]

        valVendas = []
        for prod in produtos:
            datP = datL.loc[datL["Produto"] == prod]
            lista = datP["ValorVenda"].values.tolist()
            soma = sum(lista)
            valVendas.append(soma)

        st.write("Raanking Loja -> ",str(loja))
        dataFrame = pd.DataFrame({"Produto":list(produtos),"Valor Vendas":valVendas})
        dataFrame = dataFrame.sort_values(['Valor Vendas','Produto'], ascending=False)
        sns.barplot(data = dataFrame, x="Valor Vendas", y="Produto", estimator = np.sum, palette="tab10")
        plt.title("Ranking Loja -> "+str(loja))
        st.pyplot()
        st.write(dataFrame)

#ok
def rankingProdutosMenor(data):
    st.write("Ranking Produtos Geral")
    dic = {"Produto":data["Produto"], "Ano":data["Ano"],"ValorVenda":[],"Fabricante":data["Fabricante"],"Loja":data["Loja"]}

    valores = data["ValorVenda"]
    valores = valores.values.tolist()
    for v in range(len(valores)):
        valores[v] = float(valores[v].replace(",", "."))

    dic["ValorVenda"] = valores
    dats = pd.DataFrame(dic)
    #dats = dats.sort_values(['ValorVenda','Produto'], ascending=False)
    produtos = set()
    for p in range(len(dats["Produto"])):
        prod = dic["Produto"][p]
        produtos.add(prod)

    valVendas = []
    for prod in produtos:
        datP = dats.loc[dats["Produto"] == prod]
        lista = datP["ValorVenda"].values.tolist()
        soma = sum(lista)
        valVendas.append(soma)

    dataFrame = pd.DataFrame({"Produto":list(produtos),"Valor Vendas":valVendas})
    dataFrame = dataFrame.sort_values(['Valor Vendas','Produto'], ascending=True)

    st.write("Ranking Geral (Maior para o Menor)")
    sns.barplot(data = dataFrame, x="Valor Vendas", y="Produto", estimator = np.sum, palette="tab10")
    st.pyplot()
    st.write(dataFrame)

    loj = ["R1296", "BA7783", "JP8825", "RG7742", "AL1312", "GA7751", "JB6325"]
    for loja in loj:
        datL = dats.loc[dats["Loja"] == loja]

        valVendas = []
        for prod in produtos:
            datP = datL.loc[datL["Produto"] == prod]
            lista = datP["ValorVenda"].values.tolist()
            soma = sum(lista)
            valVendas.append(soma)

        st.write("Raanking Loja -> ",str(loja))
        dataFrame = pd.DataFrame({"Produto":list(produtos),"Valor Vendas":valVendas})
        dataFrame = dataFrame.sort_values(['Valor Vendas','Produto'], ascending=True)
        sns.barplot(data = dataFrame, x="Valor Vendas", y="Produto", estimator = np.sum, palette="tab10")
        plt.title("Ranking Loja -> "+str(loja))
        st.pyplot()
        st.write(dataFrame)

#ok
def valorVendasLoja(data):
    st.write("Ranking Vendas por Loja (Em reais)")

    dic = {"Produto":data["Produto"], "Ano":data["Ano"],"ValorVenda":[],"Fabricante":data["Fabricante"],"Loja":data["Loja"]}

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

    dataFrame = pd.DataFrame({"Loja":loj,"Valor Vendas":valVendas})
    dataFrame = dataFrame.sort_values(['Valor Vendas'], ascending=False)
    sns.barplot(data = dataFrame, x="Loja", y="Valor Vendas", estimator = np.sum, palette="pastel")
    plt.title("Ranking Vendas por Loja (Em reais)")
    st.pyplot()
    st.write(dataFrame)

def valorVendasVendedor(data):
    dic = {"Ano":data["Ano"],"ValorVenda":[],"Categoria":data["Categoria"],"Mes":data["Mes"],"Produto":data["Produto"],"Fabricante":data["Fabricante"],"Loja":data["Loja"],"Vendedor":data["Vendedor"]}

    valores = data["ValorVenda"]
    valores = valores.values.tolist()
    for v in range(len(valores)):
        valores[v] = float(valores[v].replace(",", "."))

    dic["ValorVenda"] = valores
    dats = pd.DataFrame(dic)
    st.write("Ranking de Vendedores por Ano")
    anosSet = [2014,2015,2016,2017,2018,2019]
    for ano in anosSet:
        datA = dats.loc[dats["Ano"] == ano]
        sns.barplot(data = dats,  y="Vendedor", x="ValorVenda", estimator = np.sum, palette="tab20")
        plt.title("Ranking Vendedores "+str(ano))

        st.pyplot()

    vendedorLoja(dats)

def vendedorLoja(data):
    dats = data
    loj = ["R1296", "BA7783", "JP8825", "RG7742", "AL1312", "GA7751", "JB6325"]
    st.write("Ranking de Vendedores para Cada Loja (Geral e por Ano)")
    for loja in loj:
        datP = dats.loc[dats["Loja"] == loja]

        sns.barplot(data = datP, y="Vendedor", x="ValorVenda", hue = "Ano", estimator = np.sum, palette="bright")
        plt.title("Ranking Vendedores Loja -> "+str(loja)+" por Ano")
        st.pyplot()

        sns.barplot(data = datP, y="Vendedor", x="ValorVenda", estimator = np.sum, palette="Set2")
        plt.title("Ranking Geral Vendedores Loja -> "+str(loja))
        st.pyplot()

#ok
def rankingRentaveis(data):
    st.write("Ranking Rentáveis (Valor Venda - Preço Custo)")

    dic = {"Produto":data["Produto"], "Ano":data["Ano"],"ValorVenda":[],"Fabricante":data["Fabricante"],"Loja":data["Loja"],"Custo":[],"Rentabilidade":[]}

    valores = data["ValorVenda"]
    valores = valores.values.tolist()
    custos = data["preço Custo"]
    custos = custos.values.tolist()
    for v in range(len(valores)):
        valores[v] = float(valores[v].replace(",", "."))
        custos[v] = float(custos[v].replace(",","."))
        dic["Rentabilidade"].append(valores[v]-custos[v])

    dic["ValorVenda"] = valores
    dic["Custo"] = custos
    dats = pd.DataFrame(dic)
    #dats = dats.sort_values(['ValorVenda','Produto'], ascending=False)
    valVendas = []
    loj = ["R1296", "BA7783", "JP8825", "RG7742", "AL1312", "GA7751", "JB6325"]
    st.write("Ranking Rentáveis (Geral)")
    #
    pset = set()
    produtos = data["Produto"]
    produtos = produtos.values.tolist()
    for k in range(len(produtos)):
        pset.add(produtos[k])

    rent = {"Produto":[] , "Rentabilidade":[]}
    for prod in pset:
        df = dats.loc[dats["Produto"] == prod]
        soma = df["Rentabilidade"].sum()
        rent["Produto"].append(prod)
        rent["Rentabilidade"].append(soma)

    rentDic = rent
    rent = pd.DataFrame(rent)
    rent = rent.sort_values(['Rentabilidade','Produto'], ascending=False)

    sns.barplot(data = rent, x="Rentabilidade", y="Produto", estimator = np.sum, palette="Set1")
    plt.title("Ranking Rentáveis (Geral)")
    st.pyplot()
    st.write(rent)
    #

    for loja in loj:
        datP = dats.loc[dats["Loja"] == loja]
        st.write("Ranking Rentáveis Loja -> "+str(loja))

        rent = {"Produto":[] , "Rentabilidade":[]}
        for prod in pset:
            df = datP.loc[datP["Produto"] == prod]
            soma = df["Rentabilidade"].sum()
            rent["Produto"].append(prod)
            rent["Rentabilidade"].append(soma)

        rentDic = rent
        rent = pd.DataFrame(rent)
        rent = rent.sort_values(['Rentabilidade','Produto'], ascending=False)

        sns.barplot(data = rent, x="Rentabilidade", y="Produto", estimator = np.sum, palette="pastel")
        plt.title("Ranking Rentáveis Loja --> "+str(loja))
        st.pyplot()
        st.write(rent)

        ##sns.barplot(data = datP, x="Rentabilidade", y="Produto", estimator = np.sum, palette="pastel")
        ##plt.title("Ranking Rentáveis Loja -> "+str(loja))
        ##st.pyplot()


###################
st.set_option('deprecation.showPyplotGlobalUse', False)
# carregar os dados
dataset = load_data()

#Padrão Geral
st.title('Dashboard para Análise de Vendas')


# SIDEBAR

st.sidebar.header("Opções")

if st.sidebar.button("Total de Vendas (Valor) por Ano"):
    dats = valorVendasAno(dataset)
if st.sidebar.button("Total de Vendas (Valor) por Categoria"):
    valorVendasCategoria(dataset)
if st.sidebar.button("Total de Vendas (Valor) por Categoria por Ano"):
    valorVendasCategoriaAno(dataset)
if st.sidebar.button("Total de Vendas (Valor) por Ano por Categoria"):
    valorVendasAnoCategoria(dataset)

if st.sidebar.button("Total de vendas por categoria pelos meses para cada ano (Em Reais)"):
    valorVendasMes(dataset)
if st.sidebar.button("Total Vendas de Produtos por Fabricante (Em Reais)"):
    valorVendasProdutoFabricante(dataset)
if st.sidebar.button("Vendas das lojas por categoria (Em Reais)"):
    valorVendasLojaCategoria(dataset)
if st.sidebar.button("Rankings Maiores Vendas dos Produtos (Em Reais)"):
    rankingProdutos(dataset)
if st.sidebar.button("Rankings Menores Vendas dos Produtos (Em Reais)"):
    rankingProdutosMenor(dataset)

if st.sidebar.button("Ranking dos produtos mais rentáveis"):
    rankingRentaveis(dataset)
    #no geral e por loja
if st.sidebar.button("Ranking de vendas por lojas (Em Reais)"):
    valorVendasLoja(dataset)
if st.sidebar.button("Rankings dos vendedores com maior valor de vendas (Em Reais)"):
    valorVendasVendedor(dataset)
    #por loja e ano

