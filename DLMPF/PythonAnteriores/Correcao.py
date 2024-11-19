#Arquivo pra me ajudar a corrigir o erro no subconjunto

#MAPA MODELO LINHA

import pandas as pd
from docplex.mp.model import Model
import re #Manipular as strings do modelo lp


read_capacidade = pd.read_csv("DadosBergamini2022/Instancia I/capacidade.csv")
read_demanda = pd.read_csv("DadosBergamini2022/Instancia I/demanda.csv")
read_itens = pd.read_csv("DadosBergamini2022/Instancia I/modelos.csv")
read_mapa_modelo_linha = pd.read_csv("DadosBergamini2022/Instancia I/mapalinhamodelo.csv")
read_mapa_linha_recurso = pd.read_csv("DadosBergamini2022/Instancia I/mapalinharecurso.csv")
read_mapa_modelo_recurso = pd.read_csv("DadosBergamini2022/Instancia I/mapamodelorecurso.csv")
read_C = pd.read_csv("DadosBergamini2022/Instancia I/C.csv")
read_t_processamento = pd.read_csv("DadosBergamini2022/Instancia I/tprocessamento.csv")
read_capacidade_diaria = pd.read_csv("DadosBergamini2022/Instancia I/capacidadediaria.csv")

itens_list = read_itens['modelos'].tolist()
    
lista_aux = []
for i in range(0, len(itens_list)):
    lista_aux.append(i)
    
dicionario_nome_num = {}
for keys in itens_list:
    for values in lista_aux:
        dicionario_nome_num[keys] = values
        lista_aux.remove(values)
        break
        
CONJ_P_itens = list(range(0,len(itens_list)))

linhas_MLM = read_mapa_modelo_linha['linhas'].tolist()

itens_MLM = read_mapa_modelo_linha['modelos'].tolist()


SUBCONJ_modelo_linha = []

for i in itens_list:
    aux = []
    SUBCONJ_modelo_linha.append(aux)
    
itens_MLM_num = []

for i in itens_MLM:
    itens_MLM_num.append(dicionario_nome_num[i])


contador_novo = 0
for i in itens_MLM_num: 
    SUBCONJ_modelo_linha[i].append(linhas_MLM[contador_novo])
    contador_novo += 1
    
