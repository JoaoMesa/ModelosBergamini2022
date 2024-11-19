import pandas as pd
from docplex.mp.model import Model

read_tempo = pd.read_csv("planilhas/Dia_1/tprocessamento.csv")
read_setup = pd.read_csv("planilhas/Dia_1/setup.csv")
read_produtos = pd.read_csv("planilhas/Dia_1/produtos.csv")
read_mapa_prod_grupo = pd.read_csv("planilhas/Dia_1/MapaProdGrupo.csv")
read_M = pd.read_csv("planilhas/Dia_1/M.csv")
read_modelos = pd.read_csv("planilhas/Dia_1/modelos.csv")
read_num_prod_grupo = pd.read_csv("planilhas/Dia_1/NumProdutosNoGrupo.csv")

#============================================================================================================================================
    
# TEMPO PROCESSAMENTO
    
#============================================================================================================================================


t = read_tempo['tempo_processamento'].tolist()

#print(t)

#============================================================================================================================================
    
# GRUPOS
    
#============================================================================================================================================


CONJ_G = read_modelos['modelo'].tolist()
CONJ_G.insert(0,0)

#print(CONJ_G)

#============================================================================================================================================
    
# MODELOS
    
#============================================================================================================================================


CONJ_J = read_produtos['produto'].tolist()

#print(CONJ_J)

#============================================================================================================================================
    
# VALOR M
    
#============================================================================================================================================


M = read_M['M'].tolist()[0]

#print(M)

#============================================================================================================================================
    
# QUANTIDADE DE PRODUTOS EM CADA GRUPO
    
#============================================================================================================================================


QTD_GRUPOS = read_num_prod_grupo['NumeroProdNoGrupo'].tolist()
QTD_GRUPOS.insert(0,0)
#print(QTD_GRUPOS)

#============================================================================================================================================
    
# SUBCONJUNTO DE PRODUTOS EM CADA GRUPO
    
#============================================================================================================================================


aux_produtos = read_mapa_prod_grupo['produto'].tolist()
aux_grupos = read_mapa_prod_grupo['grupo'].tolist()
SUBCONJ_Jn = []

for grupo in CONJ_G:
	SUBCONJ_Jn.append([])
	
for produto, grupo in zip(aux_produtos, aux_grupos):
    SUBCONJ_Jn[grupo].append(produto)	


#print(aux_produtos, len(aux_produtos))
#print(aux_grupos, len(aux_grupos))
#print(SUBCONJ_Jn)

#============================================================================================================================================
    
# SETUP
    
#============================================================================================================================================

aux_i = read_setup['i'].tolist()
aux_j = read_setup['j'].tolist()
aux_setup = read_setup['setup'].tolist()

s = []

for prod in range(len(CONJ_J)):
    s.append([[] for prod in range(len(CONJ_J))])
    
for i, j, valor in zip(aux_i, aux_j, aux_setup):
    s[i][j].append(valor)



#print(aux_i, len(aux_i))
#print(aux_j, len(aux_j))
#print(aux_setup, len(aux_setup))
#print(s, len(s), len(s[0]))

for i in s[8]:
	print(i)

