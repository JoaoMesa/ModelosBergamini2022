import pandas as pd
from docplex.mp.model import Model
import re #Manipular as strings do modelo lp


def main():
    
    #============================================================================================================================================
    # Retirando dados das planilhas
    #============================================================================================================================================

    
    read_capacidade = pd.read_csv("DadosBergamini2022/Instancia I/capacidade.csv")
    read_demanda = pd.read_csv("DadosBergamini2022/Instancia I/demanda.csv")
    read_itens = pd.read_csv("DadosBergamini2022/Instancia I/modelos.csv")
    read_mapa_modelo_linha = pd.read_csv("DadosBergamini2022/Instancia I/mapalinhamodelo.csv")
    read_mapa_linha_recurso = pd.read_csv("DadosBergamini2022/Instancia I/mapalinharecurso.csv")
    read_mapa_modelo_recurso = pd.read_csv("DadosBergamini2022/Instancia I/mapamodelorecurso.csv")
    read_C = pd.read_csv("DadosBergamini2022/Instancia I/C.csv")
    read_t_processamento = pd.read_csv("DadosBergamini2022/Instancia I/tprocessamento.csv")
    read_capacidade_diaria = pd.read_csv("DadosBergamini2022/Instancia I/capacidadediaria.csv")


    #============================================================================================================================================
    
    # Lendo modelos e criando um dicionário entre o nome e o número dos modelos
    #============================================================================================================================================


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
    
    
    #============================================================================================================================================
    
    # Lendo a capacidade de linhas por período
    #============================================================================================================================================

    C_list_c = read_C['C'].to_list()
    C_list_linhas = read_C['linhas'].to_list()
    C_list_periodos = read_C['periodos'].to_list()

    num_linhas = max(C_list_linhas) + 1
    num_periodos = max(C_list_periodos) + 1
    
    matriz_lin_per = [[0] * num_periodos for i in range(num_linhas)]
    
    for c, linha, periodo in zip(C_list_c, C_list_linhas, C_list_periodos):
        matriz_lin_per[linha][periodo] = c


    #============================================================================================================================================
    
    # Lendo o tempo de processamento de cada modelo em cada linha
    #============================================================================================================================================


    list_modelos = read_t_processamento['modelos'].to_list()
    list_linhas = read_t_processamento['linhas'].to_list()
    list_temp = read_t_processamento['tprocessamento'].to_list()
    
    list_modelos_num = []
    for i in list_modelos:
        list_modelos_num.append(dicionario_nome_num[i])
    
    matriz_tempo = {}
    for modelo, linha, t in zip(list_modelos_num, list_linhas, list_temp):
        if modelo not in matriz_tempo:
            matriz_tempo[modelo] = {}
        matriz_tempo[modelo][linha] = t


    
    #============================================================================================================================================
    
    # Lendo os recursos

    #============================================================================================================================================

    recursos_list = read_mapa_linha_recurso['recursos'].tolist()
    print(recursos_list)

    #============================================================================================================================================
    
    # Declarando os conjuntos

    #============================================================================================================================================


    CONJ_P_itens = list(range(0,len(itens_list)))
    CONJ_R_rec = list(range(1, max(recursos_list)+1))
    CONJ_T_per = list(dict.fromkeys(C_list_periodos))
    CONJ_T_per.insert(0,0)
    CONJ_L_lin = list(dict.fromkeys(C_list_linhas))

    #============================================================================================================================================
    
    # Declarando os subconjuntos

    #============================================================================================================================================

	#MAPA MODELO LINHA

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
    

	#MAPA MODELO RECURSO
	
    recursos_MMR = read_mapa_modelo_recurso['recursos'].tolist() 

    SUBCONJ_recurso_modelo = []

    for i in range(max(recursos_MMR)):
        aux = []
        SUBCONJ_recurso_modelo.append(aux)

    contador = 0

    for r in recursos_MMR:
        SUBCONJ_recurso_modelo[r-1].append(CONJ_P_itens[contador])
        contador += 1

    #============================================================================================================================================
    
    # Declarando os limites de cada conjunto

    #============================================================================================================================================


    P = len(CONJ_P_itens)
    R = len(CONJ_R_rec)
    T = len(CONJ_T_per)
    L = len(CONJ_L_lin)


    #============================================================================================================================================
    
    # Declarando as capacidades

    #============================================================================================================================================


    Cr = read_capacidade['capacidade'].tolist()
    Cd = read_capacidade_diaria['capacidadediaria'].tolist()
    Ch = matriz_lin_per
    p = matriz_tempo


    #============================================================================================================================================
    
    # Declarando as demandas
    
    #============================================================================================================================================
    
    Q = 240   #fixo
    q = 20    #fixo
    d = read_demanda['demanda'].to_list()
    
    d_num_lotes = []
    
    for valor in d:
        d_num_lotes.append(int(valor / Q))

    d_tam_residual = []
    
    for valor in d:
        d_tam_residual.append(valor % Q)
    
    H = 1

    print("Itens - P", CONJ_P_itens, "Quantidade: ", P, "\n")
    print("Recursos - R", CONJ_R_rec, "Quantidade: ", R, "\n")
    print("Períodos - T", CONJ_T_per, "Quantidade: ", T, "\n")
    print("Linhas - L", CONJ_L_lin, "Quantidade: ",  L, "\n")
    print("Demanda - d", d, "Quantidade: ", len(d), "\n")
    print("Número de lotes necessários para atender a demanda (d/Q) d_num_lotes", d_num_lotes, "Quantidade: ", len(d_num_lotes), "\n")
    print("Tamanho em unidades do lote com demanda residual (d mod Q) d_tam_residual", d_tam_residual, "Quantidade: ", len(d_tam_residual), "\n")
    print("Linhas por item - Li", SUBCONJ_modelo_linha, "Quantidade: ", len(SUBCONJ_modelo_linha), "\n")
    print("Itens por recurso - Pr", SUBCONJ_recurso_modelo, "Quantidade: ", len(SUBCONJ_recurso_modelo), "\n")
    print("Capacidade por recurso - Cr", Cr, "Quantidade: ", len(Cr), "\n")
    print("Capacidade diaria do recurso - Cd", Cd, "Quantidade: ", len(Cd), "\n")
    print("Capacidade da linha em cada Período - Ch", Ch, "Quantidade: ", len(Ch), "por", len(Ch[0]), "\n")
    print("Tempo de processamento para cada Modelo em cada linha - p", p, '\n')

    
    #============================================================================================================================================
    
    # Criando modelo
    
    #============================================================================================================================================

    model = Model(name = "Modelo DLMPF")
    
    #============================================================================================================================================
    
    # Declarando as variáveis de decisão
    
    #============================================================================================================================================


    x = {}
    y = {}
    z = {}
    w = {}
    
    #============================
    
    #Começar a indexão em 0

    #============================


    x = model.integer_var_cube(keys1=CONJ_P_itens, keys2=CONJ_L_lin, keys3=range(1, T), name="X_%s,%s,%s_")
    y = model.binary_var_cube(keys1=CONJ_P_itens, keys2=CONJ_L_lin, keys3=range(1,T), name='Y_%s,%s,%s_')
    w = model.integer_var_cube(keys1=CONJ_P_itens, keys2=CONJ_L_lin, keys3=CONJ_T_per, name='Parcial_%s,%s,%s_')
    z = model.binary_var_cube(keys1=CONJ_P_itens, keys2=CONJ_L_lin, keys3=range(1,T), name='Z_%s,%s,%s_')

    #============================================================================================================================================
   
    # Declarando as restrições

    #============================================================================================================================================


    # Restricao_2
    for i in CONJ_P_itens:
        model.add_constraint_(model.sum(Q * x[i,k,t] + d_tam_residual[i] * y[i,k,t] for k in SUBCONJ_modelo_linha[i] for t in range(1,T)) == d[i], ctname = 'Restricao_2')
    
    # Restricao_3
    
    for i in CONJ_P_itens:
        model.add_constraint_(model.sum(x[i,k,t] for k in SUBCONJ_modelo_linha[i] for t in range(1,T)) == d_num_lotes[i], ctname = 'Restricao_3')
        
    # Restricao_4
    
    for i in CONJ_P_itens:
        model.add_constraint_(model.sum(y[i, k, t] for k in SUBCONJ_modelo_linha[i] for t in range(1,T)) <= 1, ctname = 'Restricao_4')
    
    # Restricao_5
    
    for i in CONJ_P_itens:
        for k in CONJ_L_lin:
            for t in range(1,T):
                model.add_constraint_(w[i, k, t] <= Q * x[i, k, t] + d_tam_residual[i] * y[i, k, t], ctname = 'Restricao_5')
    
    # Restricao_6
    
    for i in CONJ_P_itens:
        for k in CONJ_L_lin:
            for t in range(1,T):
                model.add_constraint_(w[i, k, t] <= (Q - q) * z[i,k,t], ctname = 'Restricao_6')
               
    # Restricao_7
    
    for i in CONJ_P_itens:
        for k in CONJ_L_lin:
            for t in range(1,T):
                model.add_constraint_(q * z[i,k,t] <= w[i,k,t], ctname = 'Restricao_7')
                
    # Restricao_8

    for k in CONJ_L_lin:
            for t in range(1,T):
                model.add_constraint_(model.sum(z[i,k,t] for i in CONJ_P_itens) <= 1, ctname = 'Restricao_8')
               
    # Restricao_9 - Capacidade horizonte de planejamento
    
    for r in CONJ_R_rec:
        model.add_constraint_(model.sum(Q * x[i,k,t] + d_tam_residual[i] * y[i,k,t] for i in SUBCONJ_recurso_modelo[r-1] for k in SUBCONJ_modelo_linha[i] for t in range(1,T)) <= Cr[r-1], ctname = "Restricao_9")
    
    # Restricao_10 - Capacidade dos recursos período 
    
    for r in CONJ_R_rec:
        for t in range(1,T):
           model.add_constraint_(model.sum(Q * x[i,k,t] + d_tam_residual[i] * y[i,k,t] + w[i, k, t-1] - w[i,k,t] for i in SUBCONJ_recurso_modelo[r-1] for k in SUBCONJ_modelo_linha[i]) <= Cd[r-1], ctname = "Restricao_10")
            	
    # Restricao_11
    for k in CONJ_L_lin:
        for t in range(1,T):
            model.add_constraint_(model.sum(p[i][k] * (Q * x[i,k,t] + d_tam_residual[i] * y[i,k,t] + w[i,k,t-1] - w[i,k,t]) for i in CONJ_P_itens if i in p and k in p[i]) <= Ch[k][t], ctname='Restricao_11')
        
    # Restricao_12
    
    for i in CONJ_P_itens:
        for k in CONJ_L_lin:
            model.add_constraint_(w[i,k,0] == 0, ctname = 'Restricao_12')
            
    # Restricao_13
            
    for i in CONJ_P_itens:
        for k in CONJ_L_lin:
            model.add_constraint_(w[i,k,T-1] == 0, ctname = 'Restricao_13')
    
            
    #Restricao_14
    for i in CONJ_P_itens:
        for k in CONJ_L_lin:
            for t in range(1,T):
                model.add_constraint_(w[i,k,t] >= 0, ctname = 'Restricao_14.1')
                model.add_constraint_(w[i,k,t] <= Q - q, ctname = 'Restricao_14.2')

    #============================================================================================================================================
   
    # Declarando função objetivo
    
    #============================================================================================================================================

                
    objetivo = model.sum(
        p[i][k] * Q * x[i, k, t] + p[i][k] * (d_tam_residual[i]) * y[i, k, t] + H * z[i, k, t] 
        for i in CONJ_P_itens 
        for k in CONJ_L_lin 
        for t in CONJ_T_per 
       if t > 0 and i in p and k in p[i])



    model.minimize(objetivo)

    #============================================================================================================================================
   
    # Tempo limite
    
    #============================================================================================================================================
    
    #model.set_time_limit(300)

    #============================================================================================================================================
   
    # Exportando dados do modelo
    
    #============================================================================================================================================

    #restricoes_string = model.export_as_lp_string() #Modelo bruto

    # Expressão regular para encontrar números decimais e limitar a 4 casas decimais
    #restricoes_string_formatada = re.sub(r'(\d+\.\d{2})\d*', r'\1', restricoes_string)

    #print(restricoes_string_formatada)



    #============================================================================================================================================
   
    # Resolução do modelo
    
    #============================================================================================================================================


    
    solucao_inicial = model.solve(log_output=True)  

    #print("\n===================== DETALHES DA SOLUCAO =========================\n")
    
    #print(objetivo)

    #print(model.solve_details)
    
    #print("\n===================== STATUS DA SOLUCAO =========================\n")

    #print(model.solve_status)

    print("\n===================== SOLUCAO =========================\n")

    print(solucao_inicial)

    #print("\n===================== CPLEX =========================\n")

    #print(model.cplex)

    #print("\n===================== PRINTs AUXILIARES =========================\n")
    
    #print(T)

    #============================================================================================================================================
   
    # Relax and Fix
    
    #============================================================================================================================================

    


    #============================================================================================================================================
   
    # Fix and Optimize
    
    #============================================================================================================================================

    inicio_FO = solucao_inicial

    # Fixando todos os valores no Modelo
    for var in model.iter_variables():
        valor = inicio_FO.get_value(var)
        var.fix(valor)
    
    # Começando a iteração do algoritmo
    for t in CONJ_T_per:
        for i in CONJ_P_itens:
            for k in CONJ_L_lin:  # Desfixando todos os valores em t = 1, na primeira iteração
                x[i, k, t].unfix()
                y[i, k, t].unfix()
                z[i, k, t].unfix()
                w[i, k, t].unfix()
    
        # Nova solução com t = 1 solto
        solucao_parcial = model.solve(logOutput=True)
    
        # Verifica se a solução é factível
        if solucao_parcial:
            for i in CONJ_P_itens:
                for k in CONJ_L_lin:  # Fixando os novos valores de t = 1
                    x[i, k, t].fix(solucao_parcial.get_value(x[i, k, t]))
                    y[i, k, t].fix(solucao_parcial.get_value(y[i, k, t]))
                    z[i, k, t].fix(solucao_parcial.get_value(z[i, k, t]))
                    w[i, k, t].fix(solucao_parcial.get_value(w[i, k, t]))
	
	
main()
