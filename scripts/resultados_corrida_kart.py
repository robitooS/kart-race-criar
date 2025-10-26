import pandas as pd

# Carregar o arquivo csv contendo os dados da corrida de kart
df_race_kart_logs = pd.read_csv("data\log_kart.csv", delimiter=";") # Utilizar ; como delimitador

df_results_columns = [
    "Posição de chegada",
    "Código do piloto",
    "Nome do piloto", 
    "Quantidade de voltas completadas",
    "Tempo total de prova"
] # Colunas do df resultante
df_results_race_kart = pd.DataFrame(columns=df_results_columns) # Instanciando df resultante

# === 1. Lógica para código do piloto e seu respectivo nome ===
piloto_col = list(df_race_kart_logs["Piloto"])
cod_piloto = {}

for p in piloto_col:
    piloto = p.split("-")
    cod_piloto[piloto[0].strip()] = piloto[-1].strip()

df_results_race_kart["Código do piloto"] = cod_piloto.keys()
df_results_race_kart["Nome do piloto"] = cod_piloto.values()
print(df_results_race_kart)

# === 2. Contar voltas por piloto ===
qtd_voltas_series = df_race_kart_logs["Piloto"].value_counts()
qtd_voltas_dict = {indice.split("-")[0].strip() : valor for indice, valor in qtd_voltas_series.items()}
print(qtd_voltas_dict)

# Inserir no df resultante
df_results_race_kart["Quantidade de voltas completadas"] = df_results_race_kart["Código do piloto"].map(qtd_voltas_dict) # O map aplica sozinho p cada linha
print(df_results_race_kart)
