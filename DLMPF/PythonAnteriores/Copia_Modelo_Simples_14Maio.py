import pandas as pd
from docplex.mp.model import Model

def main():

    #============================================================================================================================================
    
    # Declarando os conjuntos

    #============================================================================================================================================


    CONJ_P_itens = [0, 1, 2, 3]
    CONJ_R_rec = [1, 2]
    CONJ_T_per = [1, 2, 3]
    CONJ_T_per.insert(0,0)
    CONJ_L_lin = [1, 2]

    #============================================================================================================================================
    
    # Declarando os subconjuntos

    #============================================================================================================================================

	#MAPA MODELO LINHA

    
    SUBCONJ_modelo_linha = [[1,2], [1], [1], [2]]

    
    SUBCONJ_recurso_modelo = [[0, 1], [1, 2, 3]]

    
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


    Cr = [3000, 4000] # Quantidade de peças
    Cd = [1000, 1000] # Quanto posso gastar por dia
    Ch = [[0,0,0,0], [0,30000,40000], [0,30000,40000]] # Horas da linha
    p = {0: {1: 5, 2: 10}, 1: { 1:10 }, 2: { 1:5 }, 3: {2: 5}} #Segundos para processar cada item


    #============================================================================================================================================
    
    # Declarando as demandas
    
    #============================================================================================================================================
    
    Q = 240   #fixo
    q = 20    #fixo
    d = [480, 500, 240, 500]
    
    d_num_lotes = []
    
    for valor in d:
        d_num_lotes.append(int(valor / Q))

    d_tam_residual = []
    
    for valor in d:
        d_tam_residual.append(valor % Q)
    
    H = 1000

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


    x = model.integer_var_cube(keys1=CONJ_P_itens, keys2=CONJ_L_lin, keys3=range(1,T), name='X')
    y = model.binary_var_cube(keys1=CONJ_P_itens, keys2=CONJ_L_lin, keys3=range(1,T), name='Y')
    w = model.integer_var_cube(keys1=CONJ_P_itens, keys2=CONJ_L_lin, keys3=CONJ_T_per, name='W')
    z = model.binary_var_cube(keys1=CONJ_P_itens, keys2=CONJ_L_lin, keys3=range(1,T), name='Z')
    

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
            if t >= 1:
                model.add_constraint_(model.sum(Q * x[i,k,t] + d_tam_residual[i] * y[i,k,t] + w[i, k, t-1] - w[i,k,t] for i in SUBCONJ_recurso_modelo[r-1] for k in SUBCONJ_modelo_linha[i]) <= Cd[r-1], ctname = "Restricao_10")
            
    # Restricao_11
    for k in CONJ_L_lin:
        for t in range(1,T):
            if t >= 1:
                model.add_constraint_(model.sum(p[i][k] * (Q * x[i,k,t] + (d_tam_residual[i]) * y[i,k,t] + w[i,k,t-1] - w[i,k,t]) for i in CONJ_P_itens if i in p and k in p[i]) <= Ch[k][t-1], ctname='Restricao_11')

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
                model.add_constraint_(w[i,k,t]>= 0, ctname = 'Restricao_14.1')
                model.add_constraint_(w[i,k,t]<= Q - q, ctname = 'Restricao_14.2')
    


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
   
    # Exportando dados do modelo
    
    #============================================================================================================================================


    print(model.export_as_lp_string())

    #============================================================================================================================================
   
    # Resolução do modelo
    
    #============================================================================================================================================


    
    solucao = model.solve(log_output=True)  

    print("\n===================== DETALHES DA SOLUCAO =========================\n")

    print(model.solve_details)
    
    print("\n===================== STATUS DA SOLUCAO =========================\n")

    print(model.solve_status)

    print("\n===================== SOLUCAO =========================\n")

    print(solucao)

    print("\n===================== CPLEX =========================\n")

    print(model.cplex)

    #============================================================================================================================================
   
    # Vendo cada variável
    
    #============================================================================================================================================

    #print("\n===================== TODAS AS VARIÁVEIS =========================\n")

    #for var in model.iter_variables():
    #    print(f'Variável {var} = {var.solution_value} ({var.vartype})')
  


    



    

    
    #print(cplexlog)




main()

