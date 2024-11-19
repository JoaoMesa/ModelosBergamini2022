# INDICES

set modelos;
set recursos;
set linhas;

param T;
set periodos :=  0 .. T;

# PARAMETROS (DADOS DE ENTRADA)

param demanda{modelos} default 0;
param capacidade{recursos} default 0;
param C{linhas,periodos} default 0;
param tprocessamento{modelos, linhas} default 0;
param MapaModeloRecurso{modelos, recursos} default 0;
param MapaLinhaModelo{linhas, modelos} default 0;
#param MapaLinhaRecurso{linhas, recursos} default 0;
param capacidadediaria{recursos} default 0;

param Q;
param q;

# OBTER DADOS A PARTIR DAS PLANILHAS

#table tabmodelos IN "CSV" "modelos.csv":
#modelos <- [modelos];

table tabdemanda IN "CSV" "demanda.csv":
modelos <- [modelos], demanda;

table tabcapacidade IN "CSV" "capacidade.csv":
recursos <- [recursos], capacidade;

table tabtprocessamento IN "CSV" "tprocessamento.csv":
[modelos,linhas], tprocessamento;

table tabC IN "CSV" "C.csv":
[linhas, periodos], C;

table tabmapalinhamodelo IN "CSV" "mapalinhamodelo.csv":
[linhas, modelos], MapaLinhaModelo;

table tabmapamodelorecurso IN "CSV" "mapamodelorecurso.csv":
[modelos, recursos], MapaModeloRecurso;

table tabcapacidadediaria IN "CSV" "capacidadediaria.csv":
[recursos], capacidadediaria;

# VARIAVEIS DE DECISAO

var x{modelos, linhas, periodos} >= 0, integer;
var y{modelos, linhas, periodos} binary;
var z{modelos, linhas, periodos} binary;
var parcial{modelos, linhas, periodos} >= 0, <=Q-q, integer;
var soluc;
var fobj;
#var excesso{recursos, periodos} >= 0, integer;

# FUNCAO OBJETIVO

minimize tempo: sum{i in modelos, k in linhas, t in periodos: t>0} ((tprocessamento[i,k])*Q*x[i,k,t] + (tprocessamento[i,k])*(demanda[i] mod Q)*y[i,k,t] + z[i,k,t]) ;

#FUNCAO-OBJETIVO-REAL
restr_fobj:
	fobj = sum{i in modelos, k in linhas, t in periodos: t>0} ((tprocessamento[i,k])*Q*x[i,k,t] + (tprocessamento[i,k])*(demanda[i] mod Q)*y[i,k,t]) ;

# RESTRICOES
#x deve ser igual ao numero de lotes inteiros
restr_x{i in modelos}: 
	sum{k in linhas,  t in periodos: t>0} x[i,k,t] = demanda[i] div Q;

#limitar o y a apenas uma quebra para cada modelo 
restr_y{i in modelos}: 
	sum{k in linhas, t in periodos: t>0} y[i,k,t] <= 1;

#a sobra para o dia seguinte tem tamanho máximo de 240
#restr_parcial{k in linhas, t in periodos}: 
#	sum{i in modelos} parcial[i,k,t] <= Q;

#pode haver fracionamento do lote de um modelo de um periodo para o seguinte, apenas se houver producao desse modelo
restr_parcial2{i in modelos, k in linhas, t in periodos: t>0}: 
	parcial[i,k,t] <= (Q * x[i,k,t] + (demanda[i] mod Q)*y[i,k,t]);

# Relaciona a variavel de tamanho do fracionamento (parcial) com a ocorrência de fracionamento (z)
# A variável parcial pode ser positiva apenas se houver fracionamento no periodo, e está limitada ao tamanho do lote menos o lote minimo
restr_parcial3a{i in modelos, k in linhas, t in periodos: t>0}: 
	parcial[i,k,t] <= (Q-q) * z[i,k,t];

# A variavel parcial deve respeitar o lote minimo de q unidades, se este for fração do ultimo lote do dia
restr_parcial3b{i in modelos, k in linhas, t in periodos: t>0}: 
	q * z[i,k,t] <= parcial[i,k,t];

# Limita o fracionamento de lotes em cada linha e em cada periodo em no máximo 1.
restr_parcial4{k in linhas, t in periodos: t>0}: 
	sum{i in modelos} z[i,k,t] <= 1;

# A soma dos lotes produzidos e do "saldo" dos mesmos tem que ser igual a demanda
restr_atenddemanda{i in modelos}: 
	sum{k in linhas, t in periodos: t>0 and MapaLinhaModelo[k,i]==1}  
		(Q*x[i,k,t] + (demanda[i] mod Q)*y[i,k,t]) = demanda[i];

# A soma de todos os modelos, em todas as linhas e em todos os periodos de um grupo de recursos r não pode exceder a capacidade do mesmo
restr_capacidade{r in recursos}: 
sum{t in periodos: t>0} ( sum{i in modelos, k in linhas: MapaModeloRecurso[i,r]==1 and MapaLinhaModelo[k,i]==1} 
		(Q*x[i,k,t] + (demanda[i] mod Q)*y[i,k,t]) ) <= capacidade[r];

# Em cada dia, a somatoria de todos os modelos deve respeitar a capacidade em segundos de cada linha
restr_tempoproducao{k in linhas, t in periodos: t>0}: 
	sum {i in modelos} tprocessamento[i,k]*(Q*x[i,k,t] + (demanda[i] mod Q)*y[i,k,t] + parcial[i,k,t-1] - parcial[i,k,t]) <= C[k,t];

#definindo parcial no periodo 0 e no ultimo periodo
restr_parcial0{i in modelos, k in linhas}: parcial[i,k,0] = 0;
restr_parcialT{i in modelos, k in linhas}: parcial[i,k,T] = 0;

# O somatorio de todos os modelos, em todas as linhas não deve exceder a capacidade diária dos recursos. 
restr_capacidadediaria{r in recursos, t in periodos: t>0}:
	sum{k in linhas, i in modelos: MapaModeloRecurso[i,r]==1 and MapaLinhaModelo[k,i]==1}
		(Q*x[i,k,t] + (demanda[i] mod Q)*y[i,k,t] + parcial[i,k,t-1] - parcial[i,k,t]) <= capacidadediaria[r];

#restricaodecoisas:
#soluc==sum{i in modelos, k in linhas, t in periodos} ((tprocessamento[i,k])*Q*x[i,k,t] + (tprocessamento[i,k])*(demanda[i] mod Q)*y[i,k,t] + z[i,k,t]) ;


display capacidade,capacidadediaria;

solve;

#display tempo, restr_tempoproducao;

display{i in modelos, k in linhas, t in periodos: x[i,k,t] > 0 or y[i,k,t] > 0} x[i,k,t], y[i,k,t], parcial[i,k,t];

printf{i in modelos, k in linhas, t in periodos : x[i,k,t]>0 or y[i,k,t] > 0}: "Modelo %s (d: %s), linha %s (C: %s), periodo %s: %s lotes + %s itens (%s parcial)\n", i, demanda[i], k, C[k,t], t, x[i,k,t], (demanda[i] mod Q)*y[i,k,t], parcial[i,k,t]; 

printf{t in periodos, k in linhas, i in modelos: x[i,k,t]>0 or y[i,k,t] > 0}: "Periodo %s, linha %s (C: %s), modelo %s (d: %s): %s lotes + %s itens (%s parcial)\n", t, k, C[k,t], i, demanda[i], x[i,k,t], (demanda[i] mod Q)*y[i,k,t], parcial[i,k,t]; 
printf:"Solução %s\n", soluc;


# DADOS DA INSTANCIA
data;

param T := 59;
set linhas := 1 2 3 4 5 6;

param Q := 240;
param q := 20;

end;


