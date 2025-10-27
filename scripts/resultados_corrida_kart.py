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
qtd_voltas_dict = {
    piloto_str.split("-")[0].strip(): qtd
    for piloto_str, qtd in qtd_voltas_series.items()
}

# Inserir quantidade de voltas no DF de resultados
df_results_race_kart["Quantidade de voltas completadas"] = (
    df_results_race_kart["Código do piloto"].map(qtd_voltas_dict)
)

print(f"\n************** DF RESULTANTE APÓS QTD DE VOLTAS **************\n{df_results_race_kart}\n")

# === 3. Tempo total de prova ===
df_race_kart_logs['Tempo_Volta_td'] = pd.to_timedelta(
    '00:' + df_race_kart_logs['Tempo_Volta']
) # Transformar em timedelta p calcular as durações, vem como object no df

# Retorna uma serie com o valor somado por cada cod. de piloto
tempo_por_piloto_series = df_race_kart_logs.groupby("Cod_Piloto")["Tempo_Volta_td"].sum()
df_results_race_kart["Tempo total de prova"] = df_results_race_kart["Código do piloto"].map(tempo_por_piloto_series)

print(f"\n************** DF RESULTANTE APÓS TEMPO TOTAL DE PROVA **************\n{df_results_race_kart}\n")

# Formatar a coluna para tornar mais legível
df_results_race_kart["Tempo total de prova"] = df_results_race_kart["Tempo total de prova"].astype(str).apply(lambda x: x.split(" ")[2])

print(f"\n************** DF RESULTANTE APÓS FORMATAÇÃO DA DURAÇÃO **************\n{df_results_race_kart}\n")

# === 3. Posição de chegada dos pilotos ===
df_results_race_kart = df_results_race_kart.sort_values(by=["Quantidade de voltas completadas", "Tempo total de prova"], ascending=[False, True]).reset_index(drop=True)

# Como resetamos o index, a posição vai ser o index + 1
df_results_race_kart["Posição de chegada"] = df_results_race_kart.index + 1

print(f"\n************** DF FINAL **************\n{df_results_race_kart}\n")
