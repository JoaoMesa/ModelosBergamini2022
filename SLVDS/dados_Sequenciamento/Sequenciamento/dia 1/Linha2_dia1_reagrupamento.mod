#Indice
set produto;
set modelos;
#Parametros
param setup{produto,produto};
param tempo_processamento{produto};
param takt_time{produto};
param M;
param MapaProdGrupo{produto,modelos};
param NumeroProdNoGrupo{modelos};
#Variaveis
var x{produto,produto} binary;
var instante_final{produto} >= 0;
var instante_max >= 0;

#Funcao objetivo
minimize instante_maximo: instante_max;
#Restricoes
tempo_total{j in produto, i in produto: i!=j and j!=0}: instante_final[j] >= instante_final[i] + (tempo_processamento[j] + setup[i,j])*x[i,j] - M*(1 - x[i,j]);
sucessor{i in produto}: sum{j in produto: i!=j} x[i,j] = 1;
antecessor{j in produto}: sum{i in produto: j!=i} x[i,j] = 1;
def_instante_max{j in produto}: instante_max >= instante_final[j];
c0: instante_final[0]=0;
agrupe{k in modelos}:sum{i in produto, j in produto:MapaProdGrupo[i,k]==1 and MapaProdGrupo[j,k]==1 and i!=j}x[i,j] >=NumeroProdNoGrupo[k]-1;
#forca1{i in produto: i>0}: x[i-1,i]=1;

solve;
display instante_final,instante_max,instante_maximo;
#display{i in produto, j in produto} x[i,j];
printf{i in produto, j in produto: x[i,j]>0} "Produto %s precede %s\n", i,j;

data;

set produto := 0 1 2 3 4 5 6 7 8 9 10 11;
set modelos := 1 2 3;
param setup: 0 1 2 3 4 5 6 7 8 9 10 11:=
0	0	0	0	0	0	0	0	0	0	0	0	0
1	0	0.00	156.39	156.39	210.53	210.53	210.53	0.00	0.00	156.39	156.39	210.53
2	0	156.39	0.00	0.00	54.14	54.14	54.14	156.39	156.39	0.00	0.00	54.14
3	0	156.39	0.00	0.00	54.14	54.14	54.14	156.39	156.39	0.00	0.00	54.14
4	0	0210.53	54.14	54.14	0.00	0.00	0.00	210.53	210.53	54.14	54.14	0.00
5	0	210.53	54.14	54.14	0.00	0.00	0.00	210.53	210.53	54.14	54.14	0.00
6	0	210.53	54.14	54.14	0.00	0.00	0.00	210.53	210.53	54.14	54.14	0.00
7	0	0.00	156.39	156.39	210.53	210.53	210.53	0.00	0.00	156.39	156.39	210.53
8	0	0.00	156.39	156.39	210.53	210.53	210.53	0.00	0.00	156.39	156.39	210.53
9	0	156.39	0.00	0.00	54.14	54.14	54.14	156.39	156.39	0.00	0.00	54.14
10	0	156.39	0.00	0.00	54.14	54.14	54.14	156.39	156.39	0.00	0.00	54.14
11	0	210.53	54.14	54.14	0.00	0.00	0.00	210.53	210.53	54.14	54.14	0.00;


param tempo_processamento :=
0	0
1	5894
2	4113.6
3	4113.6
4	3789.6
5	3789.6
6	3789.6
7	5052
8	5052
9	4113.6
10	4113.6
11	3789.6;


param M := 100000;

param MapaProdGrupo default 0:=
[1,1] 1
[2,2] 1
[3,2] 1
[4,3] 1
[5,3] 1
[6,3] 1
[7,1] 1
[8,1] 1
[9,2] 1
[10,2] 1
[11,3] 1;

param NumeroProdNoGrupo :=
1	3
2	4
3	4;

end;