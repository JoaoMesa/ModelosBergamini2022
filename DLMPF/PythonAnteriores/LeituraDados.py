#============================================================================================================================================
# Retirando dados das planilhas
#============================================================================================================================================

import pandas as pd

def leituraDados(instancia, P, R, L, T, CONJ_P_itens, CONJ_R_rec, CONJ_T_per, CONJ_L_lin, SUBCONJ_modelo_linha, SUBCONJ_recurso_modelo, Cr, Cd, Ch, p, Q, q, d, d_num_lotes, d_tam_residual, H):
    caminho = "DadosBergamini2022/Instancia " + instancia + "/"

    print("CAMINHO: ", caminho, "\n\n")



    read_capacidade = pd.read_csv(caminho + "capacidade.csv")
    read_demanda = pd.read_csv(caminho + "demanda.csv")
    read_itens = pd.read_csv(caminho + "modelos.csv")
    read_mapa_modelo_linha = pd.read_csv(caminho + "mapalinhamodelo.csv")
    read_mapa_linha_recurso = pd.read_csv(caminho + "mapalinharecurso.csv")
    read_mapa_modelo_recurso = pd.read_csv(caminho + "mapamodelorecurso.csv")
    read_C = pd.read_csv(caminho + "C.csv")
    read_t_processamento = pd.read_csv(caminho + "tprocessamento.csv")
    read_capacidade_diaria = pd.read_csv(caminho + "capacidadediaria.csv")

    #============================================================================================================================================
    # Lendo modelos e criando um dicionário entre o nome e o número dos modelos
    #============================================================================================================================================

    itens_list = read_itens['modelos'].tolist()

    lista_aux = []
    for i in range(len(itens_list)):
        lista_aux.append(i)

    dict_aux = {}
    for keys in itens_list:
        for values in lista_aux:
            dict_aux[keys] = values
            lista_aux.remove(values)
            break

    #============================================================================================================================================
    # Lendo a capacidade de linhas por período
    #============================================================================================================================================

    C_list_c = read_C['C'].tolist()
    C_list_linhas = read_C['linhas'].tolist()
    C_list_periodos = read_C['periodos'].tolist()

    num_linhas = max(C_list_linhas) + 1
    num_periodos = max(C_list_periodos) + 1

    matriz_lin_per = [[0] * num_periodos for _ in range(num_linhas)]

    for c, linha, periodo in zip(C_list_c, C_list_linhas, C_list_periodos):
        matriz_lin_per[linha][periodo] = c

    #============================================================================================================================================
    # Lendo o tempo de processamento de cada modelo em cada linha
    #============================================================================================================================================

    list_modelos = read_t_processamento['modelos'].tolist()
    list_linhas = read_t_processamento['linhas'].tolist()
    list_temp = read_t_processamento['tprocessamento'].tolist()

    list_modelos_num = [dict_aux[i] for i in list_modelos]

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

    CONJ_P_itens = list(range(len(itens_list)))
    CONJ_R_rec = list(range(1, max(recursos_list) + 1))
    CONJ_T_per = list(dict.fromkeys(C_list_periodos))
    CONJ_T_per.insert(0, 0)
    CONJ_L_lin = list(dict.fromkeys(C_list_linhas))

    #============================================================================================================================================
    # Declarando os subconjuntos
    #============================================================================================================================================

    # MAPA MODELO LINHA

    linhas_MLM = read_mapa_modelo_linha['linhas'].tolist()

    SUBCONJ_modelo_linha = [[] for _ in itens_list]

    contador = 0
    for i in CONJ_P_itens:
        SUBCONJ_modelo_linha[i].append(linhas_MLM[contador])
        contador += 1

    # MAPA MODELO RECURSO

    recursos_MMR = read_mapa_modelo_recurso['recursos'].tolist()

    SUBCONJ_recurso_modelo = [[] for _ in range(max(recursos_MMR))]

    contador = 0
    for r in recursos_MMR:
        SUBCONJ_recurso_modelo[r - 1].append(CONJ_P_itens[contador])
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

    Q = 240  # fixo
    q = 20  # fixo
    d = read_demanda['demanda'].tolist()

    d_num_lotes = [int(valor / Q) for valor in d]

    d_tam_residual = [valor % Q for valor in d]

    H = 1000

    print("Itens - P", CONJ_P_itens, "Quantidade: ", P, "\n")
    print("Recursos - R", CONJ_R_rec, "Quantidade: ", R, "\n")
    print("Períodos - T", CONJ_T_per, "Quantidade: ", T, "\n")
    print("Linhas - L", CONJ_L_lin, "Quantidade: ", L, "\n")
    print("Demanda - d", d, "Quantidade: ", len(d), "\n")
    print("Número de lotes necessários para atender a demanda (d/Q) d_num_lotes", d_num_lotes, "Quantidade: ", len(d_num_lotes), "\n")
    print("Tamanho em unidades do lote com demanda residual (d mod Q) d_tam_residual", d_tam_residual, "Quantidade: ", len(d_tam_residual), "\n")
    print("Linhas por item - Li", SUBCONJ_modelo_linha, "Quantidade: ", len(SUBCONJ_modelo_linha), "\n")
    print("Itens por recurso - Pr", SUBCONJ_recurso_modelo, "Quantidade: ", len(SUBCONJ_recurso_modelo), "\n")
    print("Capacidade por recurso - Cr", Cr, "Quantidade: ", len(Cr), "\n")
    print("Capacidade diária do recurso - Cd", Cd, "Quantidade: ", len(Cd), "\n")
    print("Capacidade da linha em cada Período - Ch", Ch, "Quantidade: ", len(Ch), "por", len(Ch[0]), "\n")
    print("Tempo de processamento para cada Modelo em cada linha - p", p, '\n')
