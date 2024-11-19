import re

# Suponha que 'restricoes_string' seja o resultado da função export_as_lp_string
restricoes_string = "Restricao_11: 5236.800000000000 X_18_1_1 + 5236.800000000000 X_19_1_1 + 5236.800000000000 X_20_1_1 + 4548 X_21_1_1 + 5236.800000000000 X_22_1_1 + 5236.800000000000 X_23_1_1+ 5236.800000000000 X_24_1_1 + 5236.800000000000 X_25_1_1+ 5236.800000000000 X_26_1_1 + 5236.800000000000 X_27_1_1+ 5236.800000000000 X_28_1_1 + 4908 X_29_1_1 + 4908 X_30_1_1+ 5236.800000000000 X_31_1_1 + 5236.800000000000 X_32_1_1+ 87.280000000000 Y_23_1_1 + 414.580000000000 Y_24_1_1 + 370.940000000000 Y_25_1_1 + 2007.440000000000 Y_27_1_1+ 2454 Y_30_1_1 + 1418.300000000000 Y_31_1_1 + 1483.760000000000 Y_32_1_1 + 196.380000000000 Y_34_1_1 - 21.820000000000 W_20_1_1 + 18.950000000000 W_21_1_0- aux_1_1 <= 30960"

# Expressão regular para encontrar números decimais e limitar a 4 casas decimais
restricoes_string_formatada = re.sub(r'(\d+\.\d{4})\d*', r'\1', restricoes_string)

print(restricoes_string_formatada)


