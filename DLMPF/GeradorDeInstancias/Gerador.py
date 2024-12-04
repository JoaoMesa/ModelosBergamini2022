import pandas as pd
import random

read_demanda = pd.read_csv("../DadosBergamini2022/Instancia I/demanda.csv")

print(read_demanda)

d = read_demanda['demanda'].to_list()

print(d)

demanda_max = max(d)
demanda_min = min(d)

print(demanda_max)
print(demanda_min)

with open("demanda.csv", "w") as demanda_csv:
	demanda_csv.write("modelos,demanda\n")
	for modelo in read_demanda['modelos']:
		demanda_sorteada = random.randint(demanda_min, demanda_max)
		demanda_csv.write(str(modelo)+','+str(demanda_sorteada)+"\n")
	

