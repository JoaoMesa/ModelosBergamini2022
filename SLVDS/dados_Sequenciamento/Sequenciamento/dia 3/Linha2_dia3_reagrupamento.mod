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

set produto := 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17;
set modelos := 1 2 3 4;
param setup:  0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 :=
0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0
1	0	0	0	54.1	54.1	54.1	54.1	156.4	54.1	54.1	54.1	54.1	0.0	0.0	0.0	0.0	0.0	54.1
2	0	0	0	54.1	54.1	54.1	54.1	156.4	54.1	54.1	54.1	54.1	0.0	0.0	0.0	0.0	0.0	54.1
3	0	54.13533835	54.13533835	0.0	0.0	0.0	0.0	210.5	0.0	0.0	0.0	0.0	54.1	54.1	54.1	54.1	54.1	0.0
4	0	54.13533835	54.13533835	0.0	0.0	0.0	0.0	210.5	0.0	0.0	0.0	0.0	54.1	54.1	54.1	54.1	54.1	0.0
5	0	54.13533835	54.13533835	0.0	0.0	0.0	0.0	210.5	0.0	0.0	0.0	0.0	54.1	54.1	54.1	54.1	54.1	0.0
6	0	54.13533835	54.13533835	0.0	0.0	0.0	0.0	210.5	0.0	0.0	0.0	0.0	54.1	54.1	54.1	54.1	54.1	0.0
7	0	156.3909774	156.3909774	210.5	210.5	210.5	210.5	0.0	210.5	210.5	210.5	210.5	156.4	156.4	156.4	156.4	156.4	210.5
8	0	54.13533835	54.13533835	0.0	0.0	0.0	0.0	210.5	0.0	0.0	0.0	0.0	54.1	54.1	54.1	54.1	54.1	0.0
9	0	54.13533835	54.13533835	0.0	0.0	0.0	0.0	210.5	0.0	0.0	0.0	0.0	54.1	54.1	54.1	54.1	54.1	0.0
10	0	54.13533835	54.13533835	0.0	0.0	0.0	0.0	210.5	0.0	0.0	0.0	0.0	54.1	54.1	54.1	54.1	54.1	0.0
11	0	54.13533835	54.13533835	0.0	0.0	0.0	0.0	210.5	0.0	0.0	0.0	0.0	54.1	54.1	54.1	54.1	54.1	0.0
12	0	0	0	54.1	54.1	54.1	54.1	156.4	54.1	54.1	54.1	54.1	0.0	0.0	0.0	0.0	0.0	54.1
13	0	0	0	54.1	54.1	54.1	54.1	156.4	54.1	54.1	54.1	54.1	0.0	0.0	0.0	0.0	0.0	54.1
14	0	0	0	54.1	54.1	54.1	54.1	156.4	54.1	54.1	54.1	54.1	0.0	0.0	0.0	0.0	0.0	54.1
15	0	0	0	54.1	54.1	54.1	54.1	156.4	54.1	54.1	54.1	54.1	0.0	0.0	0.0	0.0	0.0	54.1
16	0	0	0	54.1	54.1	54.1	54.1	156.4	54.1	54.1	54.1	54.1	0.0	0.0	0.0	0.0	0.0	54.1
17	0	54.13533835	54.13533835	0.0	0.0	0.0	0.0	210.5	0.0	0.0	0.0	0.0	54.1	54.1	54.1	54.1	54.1	0.0;



param tempo_processamento :=
1	4114.285714
2	4114.285714
3	3789.473684
4	3789.473684
5	3789.473684
6	3789.473684
7	5052.631579
8	3789.473684
9	3789.473684
10	3789.473684
11	3789.473684
12	4114.285714
13	4114.285714
14	4114.285714
15	4114.285714
16	4114.285714
17	3789.473684;

param MapaProdGrupo default 0:=
[1,1] 1
[2,1] 1
[3,2] 1
[4,3] 1
[5,3] 1
[6,3] 1
[7,4] 1
[8,2] 1
[9,2] 1
[10,2] 1
[11,2] 1
[12,1] 1
[13,1] 1
[14,1] 1
[15,1] 1
[16,1] 1
[17,2] 1;

param NumeroProdNoGrupo :=
1	7
2	6
3	3
4	1;

param M := 100000;

end;