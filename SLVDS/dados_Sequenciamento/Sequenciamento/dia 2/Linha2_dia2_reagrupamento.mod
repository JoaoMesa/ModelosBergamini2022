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

set produto := 0 1 2 3 4 5 6 7 8 9 10 11 12;
set modelos := 1 2 3 4;
param setup:  0 1 2 3 4 5 6 7 8 9 10 11 12 :=
0	0	0	0	0	0	0	0	0	0	0	0	0	0
1	0	0	0	0	0.021052632	0.021052632	0.021052632	0.021052632	210.5052632	210.5052632	0.021052632	54.11428571	54.11428571
2	0	0	0	0	0.021052632	0.021052632	0.021052632	0.021052632	210.5052632	210.5052632	0.021052632	54.11428571	54.11428571
3	0	0	0	0	0.021052632	0.021052632	0.021052632	0.021052632	210.5052632	210.5052632	0.021052632	54.11428571	54.11428571
4	0	0.021052632	0.021052632	0.021052632	0	0	0	0	210.5263158	210.5263158	0	54.13533835	54.13533835
5	0	0.021052632	0.021052632	0.021052632	0	0	0	0	210.5263158	210.5263158	0	54.13533835	54.13533835
6	0	0.021052632	0.021052632	0.021052632	0	0	0	0	210.5263158	210.5263158	0	54.13533835	54.13533835
7	0	0.021052632	0.021052632	0.021052632	0	0	0	0	210.5263158	210.5263158	0	54.13533835	54.13533835
8	0	210.5052632	210.5052632	210.5052632	210.5263158	210.5263158	210.5263158	210.5263158	0	0	210.5263158	156.3909774	156.3909774
9	0	210.5052632	210.5052632	210.5052632	210.5263158	210.5263158	210.5263158	210.5263158	0	0	210.5263158	156.3909774	156.3909774
10	0	0.021052632	0.021052632	0.021052632	0	0	0	0	210.5263158	210.5263158	0	54.13533835	54.13533835
11	0	54.11428571	54.11428571	54.11428571	54.13533835	54.13533835	54.13533835	54.13533835	156.3909774	156.3909774	54.13533835	0	0
12	0	54.11428571	54.11428571	54.11428571	54.13533835	54.13533835	54.13533835	54.13533835	156.3909774	156.3909774	54.13533835	0	0
;



param tempo_processamento :=
1	3789.473684
2	3789.473684
3	3789.473684
4	2210.526316
5	3789.473684
6	3789.473684
7	3789.473684
8	5052.631579
9	5052.631579
10	3789.473684
11	4114.285714
12	4114.285714;

param MapaProdGrupo default 0:=
[1,1] 1
[2,1] 1
[3,1] 1
[4,2] 1
[5,2] 1
[6,2] 1
[7,2] 1
[8,3] 1
[9,3] 1
[10,2] 1
[11,4] 1
[12,4] 1;

param NumeroProdNoGrupo :=
1	3
2	5
3	2
4	2;

param M := 100000;

end