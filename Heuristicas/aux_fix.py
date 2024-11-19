from docplex.mp.model import Model

def main():
    T = 4  # Definindo o número de iterações (no caso, o número de variáveis)

    m1 = Model(name="PI ampliado")

    # Criando as variáveis (agora com 4 variáveis: 2 inteiras e 2 binárias)
    x = m1.integer_var_list(4, name='x')  # x[0], x[1], x[2], x[3]
    y = m1.binary_var_list(4,  name='y')  # y[0], y[1], y[2], y[3]

    m1.maximize(10*x[0] + 6*x[1] + 3*y[0] - 2*y[1] + 5*x[2] - 4*y[2] + 7*x[3] + 3*y[3])

    m1.add_constraint(9*x[0] + 5*x[1] + 4*x[2] + 3*x[3] <= 45)
    m1.add_constraint(-4*x[0] + 5*x[1] + 2*x[2] - 3*x[3] <= 50)
    m1.add_constraint(y[0] + y[1] + y[2] + y[3] >= 3)  # Restrição de soma das variáveis binárias
    m1.add_constraint(x[0] + x[1] >= 3)  # Nova restrição: soma das variáveis inteiras deve ser maior ou igual a 10
    m1.add_constraint(x[2] - x[3] <= 10)  # Nova restrição: diferença entre x[2] e x[3] deve ser menor ou igual a 3

    # Resolver o modelo inicialmente
    solucao = m1.solve(log_output=True)
    print("\n===================== SOLUCAO INICIAL =========================\n")
    print(solucao)

    def fixar_variaveis(fixar_indices):
        for var in m1.iter_variables():
            if var.index in fixar_indices:
                var.lb = var.ub = solucao.get_value(var)

    def desfixar_variaveis(desfixar_indices):
        for var in m1.iter_variables():
            if var.index in desfixar_indices:
                var.lb = var.ub = None #Tirar os limitantes não alteram o domínio binário dela.

    fixar_variaveis(range(T))  # Fixando todas as variáveis inicialmente

    for t in range(T):
        desfixar_variaveis([t])  # Desfixando a variável t
        print(f"\nSolução para iteração {t+1} com índices fixados: {[t]}")
        solucao = m1.solve()
        print(solucao)
        fixar_variaveis([t])  # Fixando a variável t após resolver

main()
