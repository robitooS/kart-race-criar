import pandas as pd

# Carregar o arquivo csv contendo os dados da corrida de kart
df_race_kart_logs = pd.read_csv("data/log_kart.csv", delimiter=";")
print(f"\n************** KART LOG INICIAL **************\n{df_race_kart_logs}\n")

# Instanciando df resultante com as respectivas colunas
df_results_columns = [
    "Posição de chegada",
    "Código do piloto",
    "Nome do piloto",
    "Quantidade de voltas completadas",
    "Tempo total de prova"
]
df_results_race_kart = pd.DataFrame(columns=df_results_columns)

# === 1. Extrair código e nome do piloto ===
cod_pilotos = {}
for piloto_bruto in df_race_kart_logs["Piloto"]:
    partes = piloto_bruto.split("-")
    cod = partes[0].strip()
    nome = partes[-1].strip()
    cod_pilotos[cod] = nome

# Criar coluna auxiliar no DF original com apenas o código do piloto
df_race_kart_logs["Cod_Piloto"] = df_race_kart_logs["Piloto"].apply(
    lambda p: p.split("-")[0].strip()
)

# Inserir no df resultante o código e nome do piloto
df_results_race_kart["Código do piloto"] = list(cod_pilotos.keys())
df_results_race_kart["Nome do piloto"] = list(cod_pilotos.values())

print(f"\n************** DF RESULTANTE APÓS NOME E CÓDIGO DO PILOTO **************\n{df_results_race_kart}\n")
print(f"\n************** DF INICIAL **************\n{df_race_kart_logs}\n")

# === 2. Contar voltas por piloto ===
qtd_voltas_series = df_race_kart_logs["Piloto"].value_counts()
qtd_voltas_dict = {indice.split("-")[0].strip() : valor for indice, valor in qtd_voltas_series.items()}
print(qtd_voltas_dict)

# Inserir no df resultante
df_results_race_kart["Quantidade de voltas completadas"] = df_results_race_kart["Código do piloto"].map(qtd_voltas_dict) # O map aplica sozinho p cada linha
print(df_results_race_kart)
